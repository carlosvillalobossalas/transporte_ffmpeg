# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "Server.py", "172.17.0.1:5000", "app\Server:app"]

# set base image (host OS)
# FROM python:3.9-slim

FROM alpine:3.10

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# RUN apt install ffmpeg
RUN apk add --no-cache ffmpeg

# copy the content of the local src directory to the working directory
COPY . .

EXPOSE 5052

# command to run on container start
ENTRYPOINT [ "python", "./Server.py" ]