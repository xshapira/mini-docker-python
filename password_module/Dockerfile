FROM python:3.8
COPY password_module/ /
COPY requirements.txt /
COPY messageBroker.py /
COPY hostConfig.json /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
