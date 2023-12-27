import json
import os
import sys
import time

import pika
from producer import queue_email
from models import Contact


def main():
    credentials = pika.PlainCredentials(username="guest", password="guest")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=queue_email, durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()

        contact = Contact.objects(id=pk, is_delivery=False).first()

        if contact:
            print(f" [x] Received {pk}")
            time.sleep(1)
            contact.update(set__is_delivery=True)
            print(f" [x] Completed {method.delivery_tag} task")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_email,
        on_message_callback=callback,
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
