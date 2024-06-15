# Lucas Mathews - Fontys Student ID: 5023572
# Banking System DockerFile

FROM python:3.12.3

LABEL maintainer="522499@student.fontys.nl"

WORKDIR /server

COPY server/ /server/

EXPOSE 80

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

ENTRYPOINT ["python", "/server/api.py"]
