from praknet import messages
import struct

connected_ping = {
    "id": messages.ID_CONNECTED_PING,
    "time": None
}

unconnected_ping = {
    "id": messages.ID_UNCONNECTED_PING,
    "time": None,
    "magic": None,
    "client_guid": None
}

unconnected_ping_open_connections = {
    "id": messages.ID_UNCONNECTED_PING_OPEN_CONNECTIONS,
    "time": None,
    "magic": None,
    "client_guid": None
}

connected_pong = {
    "id": messages.ID_CONNECTED_PONG,
    "ping_time": None,
    "pong_time": None
}

open_connection_request_1 = {
    "id": messages.ID_OPEN_CONNECTION_REQUEST_1,
    "magic": None,
    "protocol_version": None,
    "mtu_size": None
}

open_connection_reply_1 = {
    "id": messages.ID_OPEN_CONNECTION_REPLY_1,
    "magic": None,
    "server_guid": None,
    "use_security": None,
    "mtu_size": None
}

open_connection_request_2 = {
    "id": messages.ID_OPEN_CONNECTION_REQUEST_2,
    "magic": None,
    "server_address": None,
    "mtu_size": None,
    "client_guid": None
}

open_connection_reply_2 = {
    "id": messages.ID_OPEN_CONNECTION_REPLY_2,
    "magic": None,
    "server_guid": None,
    "client_address": None,
    "mtu_size": None,
    "use_security": None
}

connection_request = {
    "id": messages.ID_CONNECTION_REQUEST,
    "client_guid": None,
    "request_time": None,
    "use_security": None
}

connection_request_accepted = {
    "id": messages.ID_CONNECTION_REQUEST_ACCEPTED,
    "client_address": None,
    "system_index": None,
    "system_addresses": [],
    "request_time": None,
    "time": None
}

connection_reply_accepted = {
    "id": messages.ID_CONNECTION_REPLY_ACCEPTED,
    "address": None,
    "system_addresses": [],
    "ping_time": None,
    "pong_time": None
}

connection_reply_canceled = {
    "id": messages.ID_CONNECTION_REPLY_CANCELED
}

unconnected_pong = {
    "id": messages.ID_UNCONNECTED_PONG,
    "time": None,
    "server_guid": None,
    "magic": None,
    "data": None
}

advertise_system = {
    "id": messages.ID_ADVERTISE_SYSTEM,
    "time": None,
    "server_guid": None,
    "magic": None,
    "data": None
}

nack = {
    "id": messages.ID_NACK,
    "packets": [],
}

ack = {
    "id": messages.ID_ACK,
    "packets": []
}

encapsulated = {
    "iteration": None,
    "encapsulation": None,
    "length": None,
    "id": None,
    "data": None
}

def read_address(data):
    version = data[0]
    if version == 4:
        addr = ".".join([
            str((~struct.unpack(">B", data[1:1 + 1])[0]) & 0xff),
            str((~struct.unpack(">B", data[2:2 + 1])[0]) & 0xff),
            str((~struct.unpack(">B", data[3:3 + 1])[0]) & 0xff),
            str((~struct.unpack(">B", data[4:4 + 1])[0]) & 0xff)
        ])
        port = struct.unpack(">H", data[5:5 + 2])[0]
        return addr, port, version
    else:
        raise Exception(f"Unknown address version {version}")
        
def write_address(address):
    addr, port, version = address
    buffer = b""
    buffer += struct.pack(">B", version)
    if version == 4:
        parts = addr.split(".")
        parts_count = len(parts)
        assert parts_count == 4, f"Expected address length: 4, got {parts_count}"
        for part in parts:
            buffer += struct.pack(">B", (~(int(part))) & 0xff)
        buffer += struct.pack(">H", port)
        return buffer
    else:
        raise Exception(f"Unknown address version {version}")

def read_unconnected_ping(data):
    unconnected_ping["id"] = data[0]
    unconnected_ping["time"] = struct.unpack(">Q", data[1:1 + 8])[0]
    unconnected_ping["magic"] = data[9:9 + 16]
    try:
        unconnected_ping["client_guid"] = struct.unpack(">Q", data[25:25 + 8])[0]
    except:
        unconnected_ping["client_guid"] = 12345678
    
def write_unconnected_ping():
    buffer = b""
    buffer += struct.pack(">B", unconnected_ping["id"])
    buffer += struct.pack(">Q", unconnected_ping["time"])
    buffer += unconnected_ping["magic"]
    buffer += struct.pack(">Q", unconnected_ping["client_guid"])
    return buffer

def read_unconnected_ping_open_connections(data):
    unconnected_ping_open_connections["id"] = data[0]
    unconnected_ping_open_connections["time"] = struct.unpack(">Q", data[1:1 + 8])[0]
    unconnected_ping_open_connections["magic"] = data[9:9 + 16]
    try:
        unconnected_ping_open_connections["client_guid"] = struct.unpack(">Q", data[25:25 + 8])[0]
    except:
        unconnected_ping_open_connections["client_guid"] = 12345678
    
    
def write_unconnected_ping_open_connections():
    buffer = b""
    buffer += struct.pack(">B", unconnected_ping_open_connections["id"])
    buffer += struct.pack(">Q", unconnected_ping_open_connections["time"])
    buffer += unconnected_ping_open_connections["magic"]
    buffer += struct.pack(">Q", unconnected_ping_open_connections["client_guid"])
    return buffer

def read_unconnected_pong(data):
    unconnected_pong["id"] = data[0]
    unconnected_pong["time"] = struct.unpack(">Q", data[1:1 + 8])[0]
    unconnected_pong["server_guid"] = struct.unpack(">Q", data[9:9 + 8])
    unconnected_pong["magic"] = data[17:17 + 16]
    unconnected_pong["data"] = data[35:35 + struct.unpack(">H", data[33:33 + 2])[0]].decode()
    
def write_unconnected_pong():
    buffer = b""
    buffer += struct.pack(">B", unconnected_pong["id"])
    buffer += struct.pack(">Q", unconnected_pong["time"])
    buffer += struct.pack(">Q", unconnected_pong["server_guid"])
    buffer += unconnected_pong["magic"]
    buffer += struct.pack(">H", len(unconnected_pong["data"]))
    buffer += unconnected_pong["data"].encode()
    return buffer

def read_open_connection_request_1(data):
    open_connection_request_1["id"] = data[0]
    open_connection_request_1["magic"] = data[1:1 + 16]
    open_connection_request_1["protocol_version"] = struct.unpack(">B", data[17:17 + 1])[0]
    open_connection_request_1["mtu_size"] = len(data)
    
def write_open_connection_request_1():
    buffer = b""
    buffer += struct.pack(">B", open_connection_request_1["id"])
    buffer += open_connection_request_1["magic"]
    buffer += struct.pack(">B", open_connection_request_1["protocol_version"])
    for i in range(0, open_connection_request_1["mtu_size"] - len(buffer)):
        buffer += b"\x00"
    return buffer

def read_open_connection_reply_1(data):
    open_connection_reply_1["id"] = data[0]
    open_connection_reply_1["magic"] = data[1:1 + 16]
    open_connection_reply_1["server_guid"] = struct.unpack(">Q", data[17:17 + 8])[0]
    open_connection_reply_1["use_security"] = struct.unpack(">B", data[25:25 + 1])[0]
    open_connection_reply_1["mtu_size"] = struct.unpack(">H", data[26:26 + 2])[0]
    
def write_open_connection_reply_1():
    buffer = b""
    buffer += struct.pack(">B", open_connection_reply_1["id"])
    buffer += open_connection_reply_1["magic"]
    buffer += struct.pack(">Q", open_connection_reply_1["server_guid"])
    buffer += struct.pack(">B", open_connection_reply_1["use_security"])
    buffer += struct.pack(">H", open_connection_reply_1["mtu_size"])
    return buffer
        
def read_open_connection_request_2(data):
    open_connection_request_2["id"] = data[0]
    open_connection_request_2["magic"] = data[1:1 + 16]
    open_connection_request_2["server_address"] = read_address(data[17:17 + 7])
    open_connection_request_2["mtu_size"] = struct.unpack(">H", data[24:24 + 2])[0]
    open_connection_request_2["client_guid"] = struct.unpack(">Q", data[26:26 + 8])[0]

def write_open_connection_request_2():
    server_address = open_connection_request_2["server_address"]
    buffer = b""
    buffer += struct.pack(">B", open_connection_request_2["id"])
    buffer += open_connection_request_2["magic"]
    buffer += write_address(server_address[0], server_address[1], server_address[2])
    buffer += struct.pack(">H", open_connection_request_2["mtu_size"])
    buffer += struct.pack(">Q", open_connection_request_2["client_guid"])
    return buffer

def read_open_connection_reply_2(data):
    open_connection_reply_2["id"] = data[0]
    open_connection_reply_2["magic"] = data[1:1 + 16]
    open_connection_reply_2["server_guid"] = struct.unpack(">Q", data[17:17 + 8])[0]
    open_connection_reply_2["client_address"] = read_address(data[25:25 + 7])
    open_connection_reply_2["mtu_size"] = struct.unpack(">H", data[32:32 + 2])[0]
    open_connection_reply_2["use_security"] = struct.unpack(">B", data[34:34 + 1])[0]
    
def write_open_connection_reply_2():
    buffer = b""
    buffer += struct.pack(">B", open_connection_reply_2["id"])
    buffer += open_connection_reply_2["magic"]
    buffer += struct.pack(">Q", open_connection_reply_2["server_guid"])
    buffer += write_address(open_connection_reply_2["client_address"])
    buffer += struct.pack(">H", open_connection_reply_2["mtu_size"])
    buffer += struct.pack(">B", open_connection_reply_2["use_security"])
    return buffer
    
def read_nack(data):
    nack["id"] = data[0]
    nack["packets"] = []
    count = struct.unpack(">H", data[1:1 + 2])[0]
    offset = 3
    for i in range(0, count):
        range = struct.unpack(">B", data[offset:offset + 1])
        offset += 1
        if range == 0:
            start_index = struct.unpack('<L', data[offset:offset + 3] + b'\x00')[0]
            offset += 3
            end_index = struct.unpack('<L', data[offset:offset + 3] + b'\x00')[0]
            offset += 3
            index = start_index
            while index <= end_index:
                nack["packets"].append(index)
                if len(nack["packets"]) > 4096:
                    raise Exception("Max acknowledgement packet count exceed")
        else:
            index = struct.unpack('<L', data[offset:offset + 3] + b'\x00')[0]
            offset += 3
            nack["packets"].append(index)

def write_nack():
    buffer = b""
    buffer += struct.pack(">B", nack["id"])
    records = 0
    nack["packets"].sorted()
    if len(nack["packets"]) > 0:
        pointer = 1
        start_index = nack["packets"][0]
        end_index = nack["packets"][0]
        while pointer < len(nack["packets"]):
            index = nack["packets"][pointer]
            pointer += 1
            diff = index - end_index
            if diff == 1:
                end_index = index
            elif diff > 1:
                if start_index == end_index:
                    buffer += struct.pack(">B", 1)
                    buffer += struct.pack("<L", start_index)[0:-1]
                    start_index = end_index = index
                else:
                    buffer += struct.pack(">B", 0)
                    buffer += struct.pack("<L", start_index)[0:-1]
                    buffer += struct.pack("<L", end_index)[0:-1]
                    start_index = end_index = index
                records += 1
        if start_index == last_index:
            buffer += struct.pack(">B", 1)
            buffer += struct.pack("<L", start_index)[0:-1]
        else:
            buffer += struct.pack(">B", 0)
            buffer += struct.pack("<L", start_index)[0:-1]
            buffer += struct.pack("<L", end_index)[0:-1]
        records += 1
    buffer = buffer[0:1] + struct.pack(">H", records) + buffer[1:]
    return buffer

def read_ack(data):
    ack["id"] = data[0]
    ack["packets"] = []
    count = struct.unpack(">H", data[1:1 + 2])[0]
    offset = 3
    for i in range(0, count):
        range = struct.unpack(">B", data[offset:offset + 1])
        offset += 1
        if range == 0:
            start_index = struct.unpack('<L', data[offset:offset + 3] + b'\x00')[0]
            offset += 3
            end_index = struct.unpack('<L', data[offset:offset + 3] + b'\x00')[0]
            offset += 3
            index = start_index
            while index <= end_index:
                ack["packets"].append(index)
                if len(ack["packets"]) > 4096:
                    raise Exception("Max acknowledgement packet count exceed")
        else:
            index = struct.unpack('<L', data[offset:offset + 3] + b'\x00')[0]
            offset += 3
            ack["packets"].append(index)

def write_ack():
    buffer = b""
    buffer += struct.pack(">B", ack["id"])
    records = 0
    ack["packets"].sorted()
    if len(ack["packets"]) > 0:
        pointer = 1
        start_index = ack["packets"][0]
        end_index = ack["packets"][0]
        while pointer < len(ack["packets"]):
            index = ack["packets"][pointer]
            pointer += 1
            diff = index - end_index
            if diff == 1:
                end_index = index
            elif diff > 1:
                if start_index == end_index:
                    buffer += struct.pack(">B", 1)
                    buffer += struct.pack("<L", start_index)[0:-1]
                    start_index = end_index = index
                else:
                    buffer += struct.pack(">B", 0)
                    buffer += struct.pack("<L", start_index)[0:-1]
                    buffer += struct.pack("<L", end_index)[0:-1]
                    start_index = end_index = index
                records += 1
        if start_index == last_index:
            buffer += struct.pack(">B", 1)
            buffer += struct.pack("<L", start_index)[0:-1]
        else:
            buffer += struct.pack(">B", 0)
            buffer += struct.pack("<L", start_index)[0:-1]
            buffer += struct.pack("<L", end_index)[0:-1]
        records += 1
    buffer = buffer[0:1] + struct.pack(">H", records) + buffer[1:]
    return buffer
