# Lucas Mathews - Fontys Student ID: 5023572
# Banking System DockerFile

FROM python:3.12.3

LABEL maintainer="522499@student.fontys.nl"

WORKDIR /banking-system

COPY / /banking-system/

EXPOSE 81

RUN pip install --no-cache-dir --upgrade -r /banking-system/requirements.txt

ENTRYPOINT ["python", "./api.py", "--host", "0.0.0.0", "--port", "81"]
