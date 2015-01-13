# Docker Rabbit MQ Demo

This project is a simple example of microservices running on docker to produce and consume jobs from a queue.

# Prerequesites

* docker host (boot2docker on osx works great)
* fig (brew install fig)

# Running the demo

`fig up`

Then once things appear to be working, visit the following url:

http://[your docker host]:15672

And use username/password: admin/mypass

## What is happening?

When you run `fig up`, the following happens:

1. Three images are built
 * tutum/rabbitmq
 * producer (based on python:2.7), check out Dockerfile in the producer directory
 * worker (based on python:2.7), check out Dockerfile in the worker directory
1. Three containers are started, as defined in `fig.yml`
 * a rabbitmq container
 * a worker container, linked to the rabbit container
 * a producer container, linked to the rabbit container
1. The worker and producer containers attempt to connect to the rabbitmq container. If the connection fails, they try again every 5 seconds for a minute before giving up.
1. The producer starts producing jobs as rabbitmq messages.
1. The worker will operate on those jobs when made aware of them by the queue.

# Starting multiple producers/workers

`fig scale rabbitmq=1 producer=[num producers] worker=[num workers]`
