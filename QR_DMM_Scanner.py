data_bytes= bytes([0xAA,0xFF,0xAA,0x5E,0x00,0x0C,0x02,0x0,0x3C,0x01,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x02,0xAA,0xFF,0xAA,0xFF])

#while True:
print(data_bytes)
print("len data_bytes: ",len(data_bytes))

def read_uart():
    global start_frame
    global test_id
    global test_id_int
    global end_frame
    global Received_flag
    if len(data_bytes)==24:
        start_frame = data_bytes[0:4]
        print("start_frame",start_frame)
        end_frame = data_bytes[20:24]
        print("end_frame",end_frame)
        identifier = bytes(data_bytes[4:5])
        print("identifier",identifier)
        dot = data_bytes[5:7]
        print("dot",dot)
        test_id = data_bytes[7:8]
        print("test_id: ",test_id)
        test_id_int = data_bytes[7]
        status = data_bytes[8:9]
        print("status",status)
        upper_limit = data_bytes[9:10]
        print("upper_limit",upper_limit)
        lower_limit = data_bytes[10:11]
        print("lower_limit",lower_limit)
        recieved_data = data_bytes[11:19]
        print("recieved_data",recieved_data)
        checksum = data_bytes[19:20]
        print("checksum",checksum)
        end_frame = data_bytes[20:24]
        print("end_frame",end_frame)
        Received_flag = 1
    else:
        print("Data frame is not complete")
        Received_flag = 0

def collect_data():
    global transmit_data_bytes
    global transmit_status
    if Received_flag ==1:
        if test_id_int == 1:
            data = bytes([0x14,0x50])
            transmit_data_bytes = data.rjust(10, b'\x00')
            print("transmit_data_bytes",transmit_data_bytes)
        elif(test_id_int==2):
            data = bytes([0x14,0x50])
            transmit_data_bytes = data.rjust(10, b'\x00')
            print("transmit_data_bytes",transmit_data_bytes)
            if len(transmit_data_bytes)!=0:
                transmit_status = bytes([0xED])
            else:
                transmit_status = bytes([0xEA])
    else:
        print("No data to send")

def calculate_checksum():
    global transmit_checksum_int
    transmit_checksum_int = sum(transmit_data_bytes)
    print("transmit_checksum_int",transmit_checksum_int)

def send_response():
    if send_flag == 1:
        transmit_frame = start_frame
        transmit_frame += bytes([0x5F])
        transmit_frame += bytes([0x00,0x0C])
        transmit_frame += test_id
        transmit_frame += transmit_status
        transmit_frame += transmit_data_bytes
        calculate_checksum()
        transmit_checksum = transmit_checksum_int.to_bytes(1,byteorder='big')
        #transmit_checksum = bytes(transmit_checksum_int.encode().hex())
        print('transmit_checksum',transmit_checksum)
        print(len(transmit_checksum))
        transmit_frame += transmit_checksum
        transmit_frame += end_frame
        print("transmit_frame",transmit_frame)
        print("len transmit_data_bytes",len(transmit_frame))


def get_command():
    print("Waiting for command")
    
    print("command received")

def process_command():
    read_uart()
    collect_data()
    send_response()

Received_flag =0
send_flag = 0

while True:
    get_command()

