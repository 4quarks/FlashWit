import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd


data = pd.read_csv('credentials_flashwit.csv')

ACCESS_KEY = data['Access key ID'].values[0]
SECRET_KEY = data['Secret access key'].values[0]


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


if __name__ == "__main__":
    uploaded = upload_to_aws('downloads/test_file', 'flashwit', 'archivo_de_test')





