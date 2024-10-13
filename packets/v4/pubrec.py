from mqtt_data_types import *
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class PubrecVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header: MQTTFixedHeader, stream: StreamReader):
        self.packet_identifier = TwoByteInteger(stream)

    def init_from_args(self, **kwargs):
        self.packet_identifier = kwargs[Literals.PACKET_IDENTIFIER]


    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tPacket Identifier:{self.packet_identifier}\n"

        return return_string
    
    def to_bytes(self):
        attributes = ['packet_identifier']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])
    
    @classmethod
    def from_args(cls, packet_identifier : int):
        kwargs = {
            Literals.PACKET_IDENTIFIER : TwoByteInteger.from_args(packet_identifier),
        }
        return cls(fixed_header=None, stream=None, **kwargs)
    
class PubrecPayload(MQTTPayload):

    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : PubrecVariableHeader, stream : StreamReader):
        pass

    def init_from_args(self, **kwargs):
        pass

    def __str__(self):
        return super().__str__()

    def to_bytes(self):
        return b''
   
    @classmethod
    def from_args(cls):
        return cls(None, None, None, **{})
    
class PubrecPacket(Packet):
    VARIABLE_HEADER_CLASS = PubrecVariableHeader
    PAYLOAD_CLASS = PubrecPayload
    NAME = "Pubrec"

    @classmethod
    def from_args(cls,  packet_identifier : int):
        variable_header = PubrecVariableHeader.from_args(packet_identifier)
        payload = PubrecPayload.from_args()
        

        type_and_flags = PacketFixedHeaderFlags.PUBREC
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)