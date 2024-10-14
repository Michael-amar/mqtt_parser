from mqtt_data_types import *
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class PubcompVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header: MQTTFixedHeader, stream: StreamReader):
        self.packet_identifier = TwoByteInteger(stream)
        match fixed_header.remaining_length.value:
            case 2:
                self.reason_code = ReasonCode.from_args(0)
                self.properties = Properties.from_args(None)
            case 3:
                self.reason_code = ReasonCode(stream)
                self.properties = Properties.from_args(None)
            case _:
                self.reason_code = ReasonCode(stream)
                self.properties = Properties(stream)
    
    def init_from_args(self, **kwargs):
        self.packet_identifier = kwargs[Literals.PACKET_IDENTIFIER]
        self.reason_code = kwargs[Literals.REASON_CODE]
        self.properties = kwargs[Literals.PROPERTIES]
        

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tPacket Identifier:{self.packet_identifier}\n"
        return_string += f"\t\tReason Code:{self.reason_code}\n"
        return_string += f"\t\tProperties:{self.properties}\n"
        return return_string
    
    def to_bytes(self):
        attributes = ['packet_identifier', 'reason_code', 'properties']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])
    
    @classmethod
    def from_args(cls, packet_identifer : int, reason_code : int, properties : list[Property]):
        kwargs = {
            Literals.PACKET_IDENTIFIER : TwoByteInteger.from_args(packet_identifer),
            Literals.REASON_CODE : ByteInteger.from_args(reason_code),
            Literals.PROPERTIES : Properties.from_args(properties)
        }
        return cls(fixed_header=None, stream=None, **kwargs)
    
class PubcompPayload(MQTTPayload):

    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : PubcompVariableHeader, stream : StreamReader):
        pass

    def init_from_args(self, **kwargs):
        pass

    def __str__(self):
        return super().__str__()

    def to_bytes(self):
        return b''
    
    @classmethod
    def from_args(cls):
        return cls(None, None, None,  **{})
    
class PubcompPacket(Packet):
    VARIABLE_HEADER_CLASS = PubcompVariableHeader
    PAYLOAD_CLASS = PubcompPayload
    NAME = "Pubcomp"

    @classmethod
    def from_args(cls, packet_identifier : int,  reason_code : int, properties : list[Property]):
        variable_header = PubcompVariableHeader.from_args(packet_identifier, reason_code, properties)
        payload = PubcompPayload.from_args()
        

        type_and_flags = PacketFixedHeaderFlags.PUBCOMP
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)