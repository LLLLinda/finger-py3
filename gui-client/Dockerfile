FROM python:3

RUN apt-get update && apt-get install -y python3-tk

RUN pip install requests

RUN pip install git+git://github.com/broadinstitute/cromwell-tools.git@v0.3.1

ADD z.py /

CMD [ "python3", "./z.py" ]

