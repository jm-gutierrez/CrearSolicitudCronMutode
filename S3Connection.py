import boto3
import botocore
import Settings


class S3Connection:
    s3c = boto3.client('s3',
                       aws_access_key_id=Settings.AWS_ACCESS_KEY_ID_S3,
                       aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY_S3,
                       )
    s3r = boto3.resource('s3',
                         aws_access_key_id=Settings.AWS_ACCESS_KEY_ID_S3,
                         aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY_S3,
                         )

    def __init__(self):
        return None

    def read(self, key, download_key):
        try:
            print('inicia descarga')
            print(key)
            print(download_key)
            self.bucket.download_file(key, download_key)
            print('termina descarga')

        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            print (e)
            if error_code == '404':
                self.exists = False

        except Exception as e:
            print('Error Leyendo')

    def upload(self, file, key):
        try:
            # self.bucket.upload_file(filename=file, key=key, ExtraArgs={'ACL': 'public-read'})
            print('File: ' + file)
            bucket_name = 'apks-pruebas-automaticas'
            print('bucket_name ' + bucket_name)
            print('key ' + key)
            self.s3c.upload_file(file, bucket_name, key, ExtraArgs={'ACL': 'public-read'})

        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                self.exists = False

        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("S3 Terminada exit")


