FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y python3 python3-pip


COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install awscli --upgrade --user
RUN python3 -m pip install pymongo[srv]
RUN python3 -m pip install boto3 s3fs

COPY ./Modules   ./Modules

ENV AWS_ACCESS_KEY_ID=AKIAVTWL6PT5PMSLZ6KP
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_DEFAULT_REGION=sa-east-1

COPY modelo3.py   ./
# CMD ["modelo2.train"]      