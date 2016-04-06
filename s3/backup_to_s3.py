import boto3

s3 = boto3.resource('s3')

data = open('test.jpg', 'rb')
s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)

'''


pip install awscli

aws s3 cp from s3://tweetsfortommy/yahoonews
