import json

import time

from node import NODE_ID
from node.consumer import Node

time.sleep(4)  # debug waiting for rabbitmq init
node = Node()

# init Node in node manager
node.publish(
    payload=json.dumps({'id': NODE_ID}),
    queue_name='node__init',
)


node.start()