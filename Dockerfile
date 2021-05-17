FROM python:3

WORKDIR /usr/src/app/

RUN mkdir ./data

COPY ./requirements.txt ./

COPY ./scripts/greenpeace_spider_full.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "greenpeace_spider_full.py"]
