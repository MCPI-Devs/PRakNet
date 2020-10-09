from praknet import handler
from praknet import messages
from praknet import socket

options = {
    "name": "",
    "ip": "0.0.0.0",
    "port": 19132,
    "custom_handler": lambda data, addr, socket: 0,
    "custom_packets": [0x84]
}

def packet_handler(data, address):
    id = data[0]
    if id == messages.ID_UNCONNECTED_PING:
        socket.sendBuffer(handler.handle_unconnected_ping(data), address)

def run():
    socket.create_socket((options["ip"], options["port"]))
    while True:
        recv = socket.receive_buffer()
        if recv != None:
            data, addr = recv
            packet_handler(data, addr)
