from datetime import datetime
import socket
import os
import json
import argparse
import time

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = ("", 0)


def send(input_file, output_file):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"[TIME] CONVERSION STARTED AT: {current_time}")

    print(input_file)
    filesize = os.path.getsize(input_file)
    input_name, input_extension = os.path.splitext(input_file)
    output_name, output_extension = os.path.splitext(output_file)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[CLIENT] connecting to {ADDR}")
    client.connect(ADDR)

    print(f"[CLIENT] connected :)")
    my_json = {
        "input_name": input_name,
        "input_extension": input_extension,
        "output_name": output_name,
        "output_extension": output_extension,
        "filesize": filesize
    }

    print(my_json)
    json_response = bytes(json.dumps(my_json), "utf-8")
    client.sendall(json_response)

    res = client.recv(BUFFER_SIZE).decode("utf-8")
    print(res)

    with open(input_file, "rb") as file:
        bytes_read = file.read(BUFFER_SIZE)
        while bytes_read:
            client.sendall(bytes_read)
            bytes_read = file.read(BUFFER_SIZE)
        file.close()

    time.sleep(2)

    # Server info
    res = client.recv(BUFFER_SIZE).decode("utf-8")
    print(f"res: {res}")

    
    status, size = res.split(SEPARATOR)
    size = int(size)
    print(f"[CLIENT] res -> Status: {status} / size: {size}")

    if status:
        with open(output_file, "wb") as file:
            data = 0
            while data < size:
                bytes_read = client.recv(BUFFER_SIZE)
                file.write(bytes_read)
                data += len(bytes_read)
            file.close()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"[TIME] CONVERSION ENDED AT: {current_time}")

    client.close()


if __name__ == "__main__":
    extensions = [".avi", ".gif", ".mov", ".mp4", ".rawvideo", ".webm", ".aac", ".ac3", ".flac", ".mp3", ".wav"]
    print(f"[FFMPEG] File extensions supported: {extensions}")


    parser = argparse.ArgumentParser(description="Converter FFMPEG")
    parser.add_argument("-i", "--input", help="Input file route", required=True)
    parser.add_argument("-o", "--output", help="Output file route", required=True)
    parser.add_argument("-host", "--host", help="The host/IP address of the receiver", required=True)
    parser.add_argument("-p", "--port", help="Port to use, default is 5052", default=5052)
    args = parser.parse_args()


    input_args = args.input
    output_args = args.output
    host = args.host
    port = args.port

    my_ip = socket.gethostbyname(socket.gethostname())
    print(f"[CLIENT] IP AND PORT: {my_ip} / 5052")

    print(f"input: {input_args} output: {output_args} host: {host} port: {port}")
    port = int(port)
    ADDR = (host, port)

    # print(f"[CLIENT IP AND PORT] {ADDR}")

    send(input_args, output_args)










