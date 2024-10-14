
from .StreamReader import BytesStreamReader, StreamReader
from .packets.packet import  MQTTFixedHeader, Packet
from .packets.connect import ConnectPacket
import importlib

from .mqtt_data_types import PacketType

import json

MQTT_VERSION = None

# MQTT_VERSION is either 4 or 5
# upon connect packet this variable will be initialized
# but if you want to parse packets individually and not as a part of an mqtt session you can use this field
def parse_mqtt(stream : StreamReader, Mqtt_version = None):
    """
        parses mqtt packets sent from stream and returns a json of the packet,
    """
    global MQTT_VERSION

    if MQTT_VERSION == None:
        MQTT_VERSION = 4 # default parser version

    if Mqtt_version != None:
        MQTT_VERSION = Mqtt_version



    mqtt_version = importlib.import_module(f".packets.v{MQTT_VERSION}", package="mqtt_parser")

    packet = None

    try:
        fixed_header = MQTTFixedHeader(stream)
    except Exception as e:
        print(e)
        exit()
    match fixed_header.packet_type:
        case PacketType.CONNECT:
            packet = ConnectPacket(fixed_header, stream)
            MQTT_VERSION = packet.variable_header.protocol_version.value
        case PacketType.CONNACK:
            packet =  mqtt_version.connack.ConnackPacket(fixed_header, stream)
        case PacketType.PUBLISH:
            packet =  mqtt_version.publish.PublishPacket(fixed_header, stream)
        case PacketType.PUBACK:
            packet =  mqtt_version.puback.PubackPacket(fixed_header, stream)
        case PacketType.PUBREC:
            packet =  mqtt_version.pubrec.PubrecPacket(fixed_header, stream)
        case PacketType.PUBREL:
            packet =   mqtt_version.pubrel.PubrelPacket(fixed_header, stream)
        case PacketType.PUBCOMP:
            packet =   mqtt_version.pubcomp.PubcompPacket(fixed_header, stream)
        case PacketType.SUBSCRIBE:
            packet =  mqtt_version.subscribe.SubscribePacket(fixed_header, stream)
        case PacketType.SUBACK:
            packet =   mqtt_version.suback.SubackPacket(fixed_header, stream)
        case PacketType.UNSUBSCRIBE:
            packet =   mqtt_version.unsubscribe.UnsubscribePacket(fixed_header, stream)
        case PacketType.UNSUBACK:
            packet =   mqtt_version.unsuback.UnsubackPacket(fixed_header, stream)
        case PacketType.PINGREQ:
            packet =   mqtt_version.pingreq.PingreqPacket(fixed_header, stream)
        case PacketType.PINGRESP:
            packet =   mqtt_version.pingresp.PingrespPacket(fixed_header, stream)
        case PacketType.DISCONNECT:
            packet =   mqtt_version.disconnect.DisconnectPacket(fixed_header, stream)
        case PacketType.AUTH:
            # only v5 have auth packet
            packet =  mqtt_version.auth.Authpacket(fixed_header, stream)
    
    try:
        extra_bytes = None
        extra_bytes = stream.read(1)
    except:
        # exception here is good because no bytes should be left in the stream after the parsing of a packet is done
        pass 

    if extra_bytes != None:
        raise Exception(f"Finished parsing a packet and stream wasn't empty\n {packet}")


    return json.loads(packet.as_json())

def parse(hex_bytes : bytearray, version = None):
    bytesStream = BytesStreamReader(hex_bytes)
    return parse_mqtt(bytesStream, version)

    