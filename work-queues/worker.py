#!/usr/bin/env python
import pika
import sys
import os
import time


def main():
    # connect to the broker and receive the message
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # create a queue if it doesn't exist
    # Note: Creating a queue using queue_declare is idempotent ‒ we can run the command as many times as we like, and only one will be created.
    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # subscribe a callback function to the queue task_queue
    # Note: The callback function is called every time a message is received on the queue.

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode('utf-8'))
        # sleep for 1 second for every dot in the message
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # use basic.quos protocol to send message only if worker is available
    channel.basic_qos(prefetch_count=1)
    # subscribe the callback function to the queue task_queue
    channel.basic_consume(
        queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


# main loop until CTRL+C
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
