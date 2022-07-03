#!/usr/bin/env python
import pika
import sys
import os


def main():
    # connect to the broker and receive the message
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # create a queue if it doesn't exist
    # Note: Creating a queue using queue_declare is idempotent ‒ we can run the command as many times as we like, and only one will be created.
    channel.queue_declare(queue='hello')

    # subscribe a callback function to the queue hello
    # Note: The callback function is called every time a message is received on the queue.
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # subscribe the callback function to the queue hello
    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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
