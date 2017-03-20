import time

from node_manager.consumer import NodeManager

time.sleep(4) # debug waiting for rabbitmq init
NodeManager().start()
