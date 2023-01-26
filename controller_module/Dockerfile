FROM python:3.11
RUN mkdir /data
COPY controller_module/ /
COPY requirements.txt message_broker.py config.py /
# COPY theHarvester/ /theHarvester/
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 5672

ENTRYPOINT ["python","main.py"]
