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

# Starting multiple producers/workers

`fig scale rabbitmq=1 producer=[num producers] worker=[num workers]`
