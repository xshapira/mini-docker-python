FROM python:3.11
COPY analyze_module/ /
COPY requirements.txt messageBroker.py config.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
