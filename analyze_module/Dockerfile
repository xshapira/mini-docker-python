FROM python:3.10
COPY analyze_module/ /
COPY requirements.txt messageBroker.py config.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
