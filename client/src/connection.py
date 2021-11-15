import serial
import serial.tools.list_ports
import sys
import xmltodict
import json
from collections import defaultdict

COM_PORT = ""
ports = list(serial.tools.list_ports.comports())
for port in ports:
    if "Arduino" in port.description:
        COM_PORT = port.device

if not COM_PORT:
    sys.exit("Can't find Arduino COM port.")

BOUDRATE = 115200
SERIAL_TIMEOUT = 0.1
SERIAL_PORT = serial.Serial(port=COM_PORT, baudrate=BOUDRATE, timeout=SERIAL_TIMEOUT)

SERVER_ROOT = {"start": "<server>", "end": "</server>"}

def get_serial_message(start, end, prev_message):
    serial_message = SERIAL_PORT.readline().decode("UTF-8").strip()
    if prev_message == "":
        message_list=[]
        flow_status = False
        while True:
            serial_message = SERIAL_PORT.readline().decode("UTF-8")

            if start in serial_message:
                message_list.append(serial_message)
                flow_status = True

            if (flow_status == True) and (end in serial_message):
                message_list.append(serial_message)
                message_str = "".join(message_list)
                return message_str[message_str.index(start) : message_str.index(end) + len(end)]

            if flow_status == True:
                message_list.append(serial_message)
    elif serial_message == "":
            return prev_message
    else:
        return serial_message

def xml_to_dict(xml_string):
    def default_value():
        return "ERROR"
    xml_message_dict = json.loads(json.dumps(xmltodict.parse(xml_string)))["server"]
    xml_message_default_dict = defaultdict(default_value, xml_message_dict)
    return xml_message_default_dict

def send_serial_message(message):
    SERIAL_PORT.write(message.encode("UTF-8"))