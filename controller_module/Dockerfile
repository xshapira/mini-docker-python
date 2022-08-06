FROM python:3.8
COPY controller_module/ /
COPY requirements.txt messageBroker.py host_config.json /
COPY theHarvester/ /theHarvester/
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
