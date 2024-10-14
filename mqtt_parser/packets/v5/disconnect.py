from mqtt_data_types import *
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class DisconnectVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header: MQTTFixedHeader, stream : StreamReader):
        match fixed_header.remaining_length.value:
            case 0:
                self.reason_code = ReasonCode.from_args(0)
                self.properties = Properties(None)
            case 1:
                self.reason_code = ReasonCode(stream)
                self.properties = Properties(None)
            case _:
                self.reason_code = ReasonCode(stream)
                self.properties = Properties(stream)

    def init_from_args(self, **kwargs):
        self.reason_code = kwargs[Literals.REASON_CODE]
        self.properties = kwargs[Literals.PROPERTIES]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tReason Code :{self.reason_code}\n"
        return_string += f"\t\tProperties:{self.properties}\n"
        return return_string
    
    def to_bytes(self):
        attributes = ['reason_code', 'properties']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])
    
    @classmethod
    def from_args(cls, reason_code : int, properties : list[Property]):
        kwargs = {
            Literals.REASON_CODE : ByteInteger.from_args(reason_code),
            Literals.PROPERTIES : Properties.from_args(properties)
        }
        return cls(fixed_header=None, stream=None, **kwargs)

class DisconnectPayload(MQTTPayload):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : DisconnectVariableHeader, stream : StreamReader):
        pass

    def init_from_args(self, **kwargs):
        pass
    
    def __str__(self):
        return super().__str__()

    def to_bytes(self):
        return b''
    
    @classmethod
    def from_args(cls):
        return cls(fixed_header = None, variable_header=None, stream=None, **{})
    
class DisconnectPacket(Packet):
    VARIABLE_HEADER_CLASS =  DisconnectVariableHeader
    PAYLOAD_CLASS = DisconnectPayload
    NAME = "Disconnect"

    @classmethod
    def from_args(cls, reason_code : int, properties : list[Property]):

        variable_header = DisconnectVariableHeader.from_args(reason_code, properties)
        payload = DisconnectPayload.from_args()

        type_and_flags = PacketFixedHeaderFlags.DISCONNECT
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)