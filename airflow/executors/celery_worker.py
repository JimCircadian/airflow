import subprocess
import logging

from airflow.configuration import conf
from celery import Celery

# to start the celery worker, run the command:
# "celery -A airflow.executors.celery_worker worker --loglevel=info"

# app = Celery('airflow.executors.celery_worker', backend='amqp', broker='amqp://')

app = Celery(
    conf.get('celery', 'CELERY_APP_NAME'),
    backend=conf.get('celery', 'CELERY_BROKER'),
    broker=conf.get('celery', 'CELERY_RESULTS_BACKEND'))

@app.task(name='airflow.executors.celery_worker.execute_command')
def execute_command(command):
    logging.info("Executing command in Celery " + command)
    try:
        subprocess.Popen(command, shell=True).wait()
    except Exception as e:
        raise e
    return True
