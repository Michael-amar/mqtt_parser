from mqtt_data_types import Literals, PacketFixedHeaderFlags, PacketType
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class PingreqVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, stream : StreamReader):
        pass

    def init_from_args(self, **kwargs):
        pass

    def __str__(self):
        return super().__str__()
    
    def to_bytes(self):
        return b''
    
    @classmethod
    def from_args(cls):
        return cls(fixed_header=None, stream=None, **{})
    
class PingreqPayload(MQTTPayload):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : PingreqVariableHeader, stream : StreamReader):
        pass

    def init_from_args(self, **kwargs):
        pass

    def __str__(self):
        return super().__str__()

    def to_bytes(self):
        return b''
    
    @classmethod
    def from_args(cls):
        return cls(fixed_header=None, variable_header=None, stream=None, **{})

class PingreqPacket(Packet):
    VARIABLE_HEADER_CLASS = PingreqVariableHeader
    PAYLOAD_CLASS = PingreqPayload
    NAME = "Pingreq"

    @classmethod
    def from_args(cls):
        variable_header = PingreqVariableHeader.from_args()
        payload = PingreqPayload.from_args()

        type_and_flags = PacketFixedHeaderFlags.PINGREQ
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)