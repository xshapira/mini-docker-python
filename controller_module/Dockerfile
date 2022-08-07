FROM python:3.8
RUN mkdir /data
COPY controller_module/ /
COPY requirements.txt messageBroker.py host_config.json /
# COPY theHarvester/ /theHarvester/
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 5672

ENTRYPOINT ["python","main.py"]
