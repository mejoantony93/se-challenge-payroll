FROM python:3.12-slim

ENV FLASK_APP=/files/main.py

COPY ./files /files

WORKDIR /files

RUN pip install --no-cache-dir -r settings/requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=7100"]
