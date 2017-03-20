import asyncio
import uuid

import asynqp
import pika

rabbit_host = 'mario_rabbitmq'  # from docker-composer link

rabbit_url = f'amqp://guest:guest@{rabbit_host}:5672//'


class BaseMarioMixin:
    """
    Can consume and publish
    """
    def __init__(self, channel=None):
        if channel:
            self.channel = channel
        else:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
            self.channel = connection.channel()
            self.channel.basic_qos(prefetch_count=1)
            self.channel.exchange_declare(exchange='mario', type='direct', durable=True)

    def consume(self, queue_name, cb):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(
            exchange='mario',
            queue=queue_name,
        )
        self.channel.basic_consume(cb, queue=queue_name, no_ack=True)

    def publish(self, queue_name, payload, reply_to=None):
        self.channel.basic_publish(
            exchange='mario',
            routing_key=queue_name,
            properties=reply_to and pika.BasicProperties(reply_to=reply_to) or None,
            body=payload
        )


class BaseMario(BaseMarioMixin):
    """
    With start_consuming
    """
    queue_callbacks = None

    def __init__(self):
        super().__init__()

        if self.queue_callbacks:
            for queue_name, cb in self.queue_callbacks:
                self.consume(queue_name, cb)

    def start(self):
        self.channel.start_consuming()


async def make_request(data, request_queue_name, nowait=False):
    """
    Send data to queue and waiting for result
    :param data:
    :param request_queue_name:
    :param nowait:
    :return:
    """
    result_queue_name = str(uuid.uuid4())
    connection = await asynqp.connect(rabbit_host)

    channel = await connection.open_channel()
    exchange = await channel.declare_exchange('mario', 'direct')

    request_queue = await channel.declare_queue(request_queue_name, durable=True)
    result_queue = await channel.declare_queue(result_queue_name, durable=True)

    await request_queue.bind(exchange, request_queue_name)
    if not nowait:
        await result_queue.bind(exchange, result_queue_name)

    msg = asynqp.Message(data, reply_to=result_queue_name)
    exchange.publish(msg, request_queue_name)

    if not nowait:
        future = asyncio.Future()

        def future_proxy(_data):
            future.set_result(_data)

        await result_queue.consume(future_proxy, no_ack=True)

        result = await future

        return result.body.decode()
    else:
        return ""
