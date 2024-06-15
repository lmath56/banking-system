# Lucas Mathews - Fontys Student ID: 5023572
# Banking System DockerFile

FROM python:3.12.3-slim as base

WORKDIR /server

COPY server/ /server/
COPY requirements.txt /server/

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

EXPOSE 8066

ENTRYPOINT ["python"]
CMD ["api.py"]