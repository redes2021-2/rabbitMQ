#!/usr/bin/env python
import pika

# if you want to connect to a broker on another machine, change the host to another IP address
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create a queue if it doesn't exist
channel.queue_declare(queue='hello')

# send message 'Hello World!' to a 'direct' exchange with routing key 'hello'
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")

# close the connection
connection.close()
