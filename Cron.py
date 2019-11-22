from time import sleep
import datetime
import Settings
import json
import subprocess
from Email import Email
from SQSConnection import SQSConnection
from S3Connection import S3Connection
from threading import Thread


def execute_test(git_url, test_id):
    suffix = git_url.index('.git')
    last_slash = git_url.rindex('/') + 1
    path = git_url[last_slash:suffix]

    dir_name = test_id + path
    # dir_name2 = dir_name + '/' + path
    output = subprocess.call(['sh', 'script.sh', dir_name, git_url, path])
    mutode_path = './' + dir_name + '/' + path +'/.mutode'
    subprocess.call(['zip', '-r', '-X', dir_name+'.zip', mutode_path])

    if output < 0:
        print('error en ejecucion de prueba')

    try:
        s3_connection = S3Connection()
        # with s3_connection:
        s3_connection.upload('./' + dir_name + '.zip', dir_name + '.zip')
    except Exception as e:
        print(e)

def process():
    try:
        sqs_connection = SQSConnection(Settings.AWS_QUEUE_URL_OUT_MUTODE)

        with sqs_connection:
            sqs_connection.receive()
            if sqs_connection.message is not '':
                message_attributes = sqs_connection.message.get('MessageAttributes')
                git_url = message_attributes['script']['StringValue']
                test_id = message_attributes['Id']['StringValue']
                #Aqui va la conversion del json
                # sqs_connection.delete()
                execute_test(git_url, test_id)
                # if Settings.EMAIL_SEND == 'Y':
                #     Email.send_email(email=email, tittle=tittle, name=user_first_name)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    #while True:
        Thread(target=process).start()
        st = str(datetime.datetime.now())
        print(st + ' : alive')
        sleep(Settings.SLEEP_TIME)
