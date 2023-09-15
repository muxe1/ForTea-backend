import os

from sqlmodel import create_engine, SQLModel
import boto3

engine = create_engine(os.environ.get("DATABASE_URL"))

s3 = boto3.client(
        service_name='s3',
        endpoint_url='https://s3.storage.selcloud.ru',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

def init_db():
    SQLModel.metadata.create_all(engine)




