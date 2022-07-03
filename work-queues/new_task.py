#!/usr/bin/env python
import pika
import sys
import os

# if you want to connect to a broker on another machine, change the host to another IP address
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create a queue if it doesn't exist
channel.queue_declare(queue='task_queue', durable=True)

# receive the message in call parameter 'body'
message = ' '.join(sys.argv[1:]) or "Hello World!"

# persistently send message to a 'direct' exchange with routing key 'task_queue'
channel.basic_publish(exchange='', routing_key='task_queue', body=message,
                      properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

print(" [x] Sent %r" % message)
# close the connection
connection.close()
