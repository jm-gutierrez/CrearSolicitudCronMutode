from time import sleep
import datetime
import Settings
import json
import subprocess
from Email import Email
from SQSConnection import SQSConnection
from threading import Thread


def execute_test(git_url):
    print('Se ejecuta la prueba')
    subprocess.call(['cd', '/home/ubuntu'])
    subprocess.call(['git', 'clone', git_url])

    suffix = git_url.index('.git')
    last_slash = git_url.rindex('/') + 1
    path = git_url[last_slash:suffix]

    subprocess.call(['cd', path])
    output = subprocess.call(['mutode', '-c', '1', './'])
    if output < 0:
        print('error en ejecucion de prueba')

def process():
    try:
        sqs_connection = SQSConnection(Settings.AWS_QUEUE_URL_OUT_MUTODE)

        with sqs_connection:
            sqs_connection.receive()
            if sqs_connection.message is not '':
                message_body = sqs_connection.message.get('Body')
                msg = json.loads(message_body)
                #Aqui va la conversion del json
                git_url = msg['script']
                sqs_connection.delete()
                execute_test(git_url)
                # if Settings.EMAIL_SEND == 'Y':
                #     Email.send_email(email=email, tittle=tittle, name=user_first_name)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        Thread(target=process).start()
        st = str(datetime.datetime.now())
        print(st + ' : alive')
        sleep(Settings.SLEEP_TIME)
