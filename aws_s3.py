import boto3
from boto3.session import Session


class Aws_S3:
    __Access_key_ID = '*****************'

    __Secret_access_key = '****************************'

    def upload_file(self,filename = '/home/pi/Documents/Projects/code/input.csv'):
	    _session = boto3.Session(aws_access_key_id= self.__Access_key_ID ,
    	                        aws_secret_access_key= self.__Secret_access_key,)
	    s3 = _session.resource('s3')
        # Filename - File to upload
	    # Bucket - Bucket to upload to (the top level directory under AWS S3)
	    # Key - S3 object name (can contain subdirectories). If not specified 	then file_name is used
	    s3.meta.client.upload_file(Filename=filename,
                                             Bucket='automation-specimen-data', Key=filename)
	    print("succesfull uploaded the file")
    


    #not a good way to use secret keys in scripts
    # create class and add get method to return private variavles ie secret keys
    def download_file(self):
        bucket_name = 'automation-input-data' #same name as given in aws_s3
        _session = Session(aws_access_key_id= self.__Access_key_ID,
                 aws_secret_access_key= self.__Secret_access_key)
        s3 = _session.resource('s3')
        my_bucket = s3.Bucket(bucket_name)
        for s3_file in my_bucket.objects.all():
    	    print(s3_file.key) # prints the contents of bucket

	    #s3 = boto3.client ('s3')
        my_bucket.download_file('media/private/input.csv','/home/pi/Documents/Projects/code/input.csv')
        print("downloaded successfully")

        
if __name__ == "__main__":
    s3_obj = Aws_S3()
    s3_obj.upload_file()
    s3_obj.download_file()
