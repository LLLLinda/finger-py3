FROM python:3

RUN pip install requests

RUN pip install git+git://github.com/broadinstitute/cromwell-tools.git@v0.3.1

ADD wrap.py /

CMD [ "python3", "./wrap.py" ]

