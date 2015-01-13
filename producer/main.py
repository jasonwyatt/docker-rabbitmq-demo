import pika
import os
import logging
import json
import time
import random
import sys

RABBIT_MQ_HOST = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR')
RABBIT_MQ_PASS = os.environ.get('RABBITMQ_PASS')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug(os.environ)

def start_producing():
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

    channel.queue_declare('jobs_queue', durable=True)
    while True:
        job = {
            'operation': random.choice(['add', 'subtract', 'multiply', 'divide']),
            'left': random.choice(range(1000)),
            'right': random.choice(range(1,1000)),
        }
        channel.basic_publish(exchange='',
                      routing_key='jobs_queue',
                      body=json.dumps(job),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, 
                      ))
        logger.info("published job: %s" % job)
        time.sleep(5)


if __name__ == "__main__":
    start_producing()