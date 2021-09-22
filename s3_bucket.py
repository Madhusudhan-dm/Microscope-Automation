import boto3
import pandas

bucket_name = 'input-csv-data'
file_name = 'input.csv'
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

# Create the S3 object
obj = client.get_object(
    Bucket = bucket_name,
    Key = file_name
)
    
# Read data from the S3 object
data = pandas.read_csv(obj['Body'])
    
# Print the data frame
print('Printing the data frame...')
print(data)
