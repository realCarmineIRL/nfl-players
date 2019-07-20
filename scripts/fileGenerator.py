import requests
from datetime import datetime
import sys
import os
import boto3


s3 = boto3.client("s3", aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
bucket_resource = s3

url = sys.argv[1]


def get_sleeper_data(url):
    type = url.split('/')[-1]
    date = datetime.today().strftime('%Y%m%d')
    req = requests.get(url)
    file = "nflPlayers_{}_{}.json".format(type, date)
    key = "{}/{}/{}/{}/{}".format(date[0:4], date[4:6], date[6:8], type, file)

    if req.status_code == 200:
        print('200 OK')
        with open(file, 'w+') as f:
            f.write(req.text)
        bucket_resource.upload_file(
            Bucket='nfl-players-data',
            Filename=file,
            Key=key
        )
    else:
        print('error getting players')


get_sleeper_data(url)
