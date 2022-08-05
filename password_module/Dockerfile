FROM python:3.8
COPY password_module/ /
COPY requirements.txt /
COPY messageBroker.py /
COPY hostConfig.json /
COPY theHarvester/ /theHarvester/
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
