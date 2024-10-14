from mqtt_data_types import Literals, PacketFixedHeaderFlags
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class PingrespVariableHeader(MQTTVariableHeader):
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

class PingrespPayload(MQTTPayload):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : PingrespVariableHeader, stream : StreamReader):
        pass

    def init_from_args(self, **kwargs):
        pass

    def __str__(self):
        return super().__str__()

    def to_bytes(self):
        return b''

    @classmethod
    def from_args(cls):
        return cls(fixed_header=None, variable_header=None,  stream=None, **{})

class PingrespPacket(Packet):
    VARIABLE_HEADER_CLASS = PingrespVariableHeader
    PAYLOAD_CLASS = PingrespPayload
    NAME = "Pingresp"

    @classmethod
    def from_args(cls):
        variable_header = PingrespVariableHeader.from_args()
        payload = PingrespPayload.from_args()

        type_and_flags = PacketFixedHeaderFlags.PINGRESP
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)