FROM python:3.11

COPY password_module/ /
COPY requirements.txt message_broker.py config.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
