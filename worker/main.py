import pika
import time
import logging
import os
import sys
import json

RABBIT_MQ_HOST = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR')
RABBIT_MQ_PASS = os.environ.get('RABBITMQ_PASS')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def start_consuming():
    logger.info("Connecting to %s:%s" % (RABBIT_MQ_HOST, 5672))
    credentials = pika.PlainCredentials('admin', RABBIT_MQ_PASS)
    parameters = pika.ConnectionParameters(RABBIT_MQ_HOST,
                                       5672,
                                       '/',
                                       credentials)
    start_time = time.time()

    while True:
        # wait for rabbitmq
        try:
            connection = pika.BlockingConnection(parameters)
            break
        except pika.exceptions.AMQPConnectionError:
            logger.warn('Cannot connect yet, sleeping 5 seconds.')
            time.sleep(5)
        if time.time() - start_time > 60:
            logger.error('Could not connect after 30 seconds.')
            exit(1)

    channel = connection.channel()
    channel.queue_declare(queue='jobs_queue', durable=True)

    logger.info("Waiting for jobs.")

    # handle jobs
    def my_callback(ch, method, properties, body):
        json_body = json.loads(body)
        logger.info("Received %s" % (json_body))

        left = json_body['left']
        right = json_body['right']

        operation = json_body['operation']
        if operation == 'add':
            result = left + right
        elif operation == 'subtract':
            result = left - right
        elif operation == 'multiply':
            result = left * right
        elif operation == 'divide':
            result = left / right

        time.sleep(2)

        logger.info('Result: %s' % result)
        # acknowledge job completion
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(my_callback,
                          queue='jobs_queue',)

    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()
