import shutil
import socket
import threading
import os
import ffmpeg._ffmpeg as ffmpeg_load
import ffmpeg._run as ffmpeg_run
from datetime import datetime
import json
# from flask import Flask
# serverFlask = Flask(__name__)

# important const
HEADER = 64
PORT = 5052
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def convert_video(input_file, output_file):

    filesize = 0
    try:
        with open(input_file) as f:
            stream = ffmpeg_load.input(input_file)
            stream = ffmpeg_load.output(stream, output_file)
            ffmpeg_run.run(stream)
        filesize = os.path.getsize(output_file)
        f.close()
        return [True, filesize]
    except NameError:
        print(NameError)
        return [False, filesize]


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    res = conn.recv(BUFFER_SIZE).decode("utf-8")
    header = json.loads(res)

    # print(f"[SERVER] Header: {header}")

    conn.send(bytes("... Por favor espere ...", "utf-8"))
    # conn.send(bytes("[WAITING] In case this is getting so long, press CTRL+C","utf-8"))

    threading.current_thread().setName(header['input_name'])
    filesize = int(header['filesize'])

    os.makedirs("conversion")
    input_file = f"conversion/a{header['input_extension']}"
    print(f"[SERVER] New input route: {input_file}")
    output_file = f"conversion/b{header['output_extension']}"
    print(f"[SERVER] New output route: {output_file}")
    try:
        with open(input_file, "wb") as file:
            data = 0
            while data < filesize:
                bytes_read = conn.recv(BUFFER_SIZE)
                file.write(bytes_read)
                data += len(bytes_read)
            file.close()

        result, size = convert_video(input_file, output_file)
        print(size)

        if not result:
            # conn.sendall(f"False{SEPARATOR}{size}")
            # conn.send("Hola Mundo")
            # conn.send(bytes(f"False{SEPARATOR}{size}", "utf-8"))
            my_json = {
                "status": False,
                "size" : size,
            }
            json_response = bytes(json.dumps(my_json), "utf-8")

        else:
            conn.send(bytes(f"True{SEPARATOR}{size}", "utf-8"))

            with open(output_file, "rb") as file:
                bytes_read = file.read(BUFFER_SIZE)
                while bytes_read:
                    # print(f"bytes read: {bytes_read}")
                    conn.sendall(bytes_read)
                    bytes_read = file.read(BUFFER_SIZE)
                file.close()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()
    fi
        shutil.rmtree(f"./conversion")
        print('Carpeta eliminada')

# @serverFlask.route("/")
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    no now.strftime("%H:%M:%S")
    print(f"[TIME] Server Time: {current_time}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



# print("[STARTING] server is starting...")
# start()

if __name__ == '__main__':
    # serverFlask.run(host='0.0.0.0')
    print("[STARTING] server is starting...")
    start()