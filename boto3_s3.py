from flask import Flask, request
import boto3
import pandas

Access_key_ID = 'AKIAZKY2ODI62VBNKCWB'

Secret_access_key = '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'

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = Access_key_ID,
    aws_secret_access_key = Secret_access_key,
    region_name = 'ap-south-1'
)
    
# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = Access_key_ID,
    aws_secret_access_key = Secret_access_key,
    region_name = 'ap-south-1'
)

app = Flask(__name__)


@app.route('/')
def index():
    return '''<form method = POST enctype = multipart/form-data action  = 'upload'
    <input type = file name = myfile>
    <input type = submit>
    </form>'''

@app.route('/upload', methods = ['POST'])
def upload():
    s3 = boto3.resource('s3')
    s3.Bucket('bucket_name').put_object(Key = 'file_name', Body = request.files['myfile'])

    return '<h1> file savedto s3 </h1>'

if __name__ == '__main__':
    app.run(debug = True)