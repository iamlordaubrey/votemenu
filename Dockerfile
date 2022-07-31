FROM python:3.10-slim

COPY requirements.txt /votemenu/requirements.txt
RUN pip3 install -r /votemenu/requirements.txt

WORKDIR /votemenu

COPY .env /votemenu/.env
COPY app /votemenu/app

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--reload"]
