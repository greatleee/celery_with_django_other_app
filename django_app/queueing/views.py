import json

import pika
from django.http import HttpResponse
from django.shortcuts import render



def push(request, task_id, seconds):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='example')
    body = {
        'task_id': task_id,
        'seconds': seconds,
    }
    channel.basic_publish(
        exchange='',
        routing_key='example',
        body=json.dumps(body),
    )
    connection.close()

    return HttpResponse('ok', content_type='text/plain', status=200)
