from mqtt_data_types import *
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class UnsubscribeVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header: MQTTFixedHeader, stream: StreamReader):
        length_before = stream.tell()

        self.packet_identifier = TwoByteInteger(stream)

        self.length = stream.tell() - length_before

    def init_from_args(self, **kwargs):
        self.packet_identifier = kwargs[Literals.PACKET_IDENTIFIER]
        self.length = kwargs[Literals.LENGTH]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tPacket Identifier:{self.packet_identifier}\n"
        return return_string
    
    def to_bytes(self):
        attributes = ['packet_identifier']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])

    @classmethod
    def from_args(cls, packet_identifier : int):
        identifier = TwoByteInteger.from_args(packet_identifier)
        length = len(identifier.to_bytes())
        kwargs = {
            Literals.PACKET_IDENTIFIER : identifier,
            Literals.LENGTH : length
        }
        return cls(fixed_header=None, stream=None, **kwargs)
    
class UnsubscribePayload(MQTTPayload):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : UnsubscribeVariableHeader, stream : StreamReader):
        payload_length = fixed_header.remaining_length.value - variable_header.length
        
        self.topics = []
        number_of_bytes_read = stream.tell()
        while (stream.tell() - number_of_bytes_read) < payload_length:
            topic = Utf8EncodedString(stream)
            self.topics.append(topic)

    def init_from_args(self, **kwargs):
        self.topics = kwargs[Literals.TOPICS]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tTopics :{[','.join([topic.__str__() for topic in self.topics])]}\n"
        return return_string

    def to_bytes(self):
        return b''.join([topic.to_bytes() for topic in self.topics])

    @classmethod
    def from_args(cls, topics : list[str]):
        kwargs = {
            Literals.TOPICS : [Utf8EncodedString.from_args(topic) for topic in topics]
        }
        return cls(fixed_header=None, variable_header=None, stream=None, **kwargs)
    
class UnsubscribePacket(Packet):
    VARIABLE_HEADER_CLASS = UnsubscribeVariableHeader
    PAYLOAD_CLASS = UnsubscribePayload
    NAME = "Unsubscribe"
    
    @classmethod
    def from_args(cls, packet_identifier : int, topics : list[str]):
        variable_header = UnsubscribeVariableHeader.from_args(packet_identifier)
        payload = UnsubscribePayload.from_args(topics)

        type_and_flags = PacketFixedHeaderFlags.UNSUBSCRIBE
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)