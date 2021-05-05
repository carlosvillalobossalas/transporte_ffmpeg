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
ENTRYPOINT [ "python3","-u","Server.py" ]