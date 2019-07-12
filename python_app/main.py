import time

import pika
from celery import Celery, shared_task

from backend import ProgressRecorder


app = Celery('tasks', broker='amqp://guest@localhost//')

@shared_task(bind=True)
def progress_setting_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='example')

def callback(ch, method, properties, body):
    body = json.loads(body)
    progress_setting_task.apply_async(task_id=)
    print(" [x] Received %r" % body)

channel.basic_consume(on_message_callback=callback,
                      queue='example',
                      auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()