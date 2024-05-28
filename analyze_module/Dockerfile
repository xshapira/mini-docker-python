FROM python:3.12-slim-bookworm
COPY analyze_module/ /
COPY requirements.txt messageBroker.py config.py logger.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
