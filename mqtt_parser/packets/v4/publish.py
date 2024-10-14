from mqtt_parser.mqtt_data_types import *
from mqtt_parser.packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from mqtt_parser.StreamReader import StreamReader
from mqtt_parser.utils import update_flag_byte

class PublishVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header: MQTTFixedHeader, stream: StreamReader):
        length_before = stream.tell()
        
        self.packet_identifier = None
        self.topic_name = Utf8EncodedString(stream)

        # if the QOS flag is 1/2
        if ((fixed_header.flags >> 1) & 0b11) > 0:
            self.packet_identifier = TwoByteInteger(stream)

        self.length = stream.tell() - length_before

    def init_from_args(self, **kwargs):
        self.packet_identifier = kwargs[Literals.PACKET_IDENTIFIER]
        self.topic_name = kwargs[Literals.TOPIC_NAME]
        self.length = kwargs[Literals.LENGTH]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tTopic Name:{self.topic_name}\n"
        return_string += f"\t\tPacket Identifier:{self.packet_identifier}\n"
        return return_string
    
    def to_bytes(self):
        attributes = ['topic_name', 'packet_identifier']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])
    
    @classmethod
    def from_args(cls, packet_identifier : int, topic_name : str):
        identifier = TwoByteInteger.from_args(packet_identifier)
        topic = Utf8EncodedString.from_args(topic_name)
        length = len(identifier.to_bytes()) + len(topic.to_bytes())
        kwargs = {
            Literals.PACKET_IDENTIFIER : identifier,
            Literals.TOPIC_NAME : topic,
            Literals.LENGTH : length
        }
        return cls(fixed_header=None, stream=None, **kwargs)

class PublishPayload(MQTTPayload):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : PublishVariableHeader, stream : StreamReader):
        payload_length = fixed_header.remaining_length.value - variable_header.length
        self.data = stream.read(payload_length)

    def init_from_args(self, **kwargs):
        self.data = kwargs[Literals.DATA]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tData :{self.data}\n"
        return return_string

    def to_bytes(self):
        return self.data

    def as_json(self):
        string_value = self.data.decode('utf-8', 'latin1').replace('\"', "\\")
        return {"data": string_value}

    @classmethod
    def from_args(cls, data :  bytes):
        kwargs = {
            Literals.DATA : data
        }
        return cls(fixed_header=None, variable_header=None, stream=None, **kwargs)
    
class PublishPacket(Packet):
    VARIABLE_HEADER_CLASS = PublishVariableHeader
    PAYLOAD_CLASS = PublishPayload
    NAME = "Publish"

    @classmethod
    def from_args(cls, dup : bool, qos : int, retain : bool,  packet_indentifier : int, topic_name : str, properties : list[Property], data :  bytes ):
        variable_header = PublishVariableHeader.from_args(packet_indentifier, topic_name, properties)
        payload = PublishPayload.from_args(data)

        publish_flags = update_flag_byte(0,dup, 3,3)
        publish_flags = update_flag_byte(publish_flags, qos, 1, 2)
        publish_flags = update_flag_byte(publish_flags, retain, 0, 0)

        type_and_flags = MQTTFixedHeader.build_type_and_flags_byte(PacketType.PUBLISH, publish_flags) 
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)