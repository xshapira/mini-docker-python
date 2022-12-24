FROM python:3.11
COPY password_module/ /
COPY requirements.txt messageBroker.py config.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
