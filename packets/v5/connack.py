from mqtt_data_types import *
from mqtt_data_types import Literals
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

from utils import update_flag_byte

class ConnackVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, stream : StreamReader):
        self.connect_acknowledge_flags = ByteInteger(stream)
        self.connect_reason_code = ByteInteger(stream)
        self.properties = Properties(stream)
    
    def init_from_args(self, **kwargs):
        self.connect_acknowledge_flags = kwargs[Literals.CONNECT_ACKNOWLEDGE_FLAGS]
        self.connect_reason_code = kwargs[Literals.CONNECT_REASON_CODE]
        self.properties = kwargs[Literals.PROPERTIES]
        

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tConnect Acknowledge Flags:{self.connect_acknowledge_flags}\n"
        return_string += f"\t\tConnect Reason Code:{self.connect_reason_code}\n"
        return_string += f"\t\tProperties:{self.properties}\n"
        return return_string
    
    def to_bytes(self):
        attributes = ['connect_acknowledge_flags', 'connect_reason_code', 'properties']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])
    
    @classmethod
    def from_args(cls, session_present : bool, connect_reason_code : int, properties : list[Property]):
        connect_acknowledge_flags = update_flag_byte(0,session_present, 0,0)
        kwargs = {
            Literals.CONNECT_ACKNOWLEDGE_FLAGS : ByteInteger.from_args(connect_acknowledge_flags),
            Literals.CONNECT_REASON_CODE : ByteInteger.from_args(connect_reason_code),
            Literals.PROPERTIES : Properties.from_args(properties)
        }

        return cls(None, None, **kwargs)
    
class ConnackPayload(MQTTPayload):
    """
    Connack packet has no payload
    """
    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : ConnackVariableHeader, stream : StreamReader):
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
    
class ConnackPacket(Packet):
    VARIABLE_HEADER_CLASS = ConnackVariableHeader
    PAYLOAD_CLASS = ConnackPayload
    NAME = "Connack"

    @classmethod
    def from_args(cls, session_present : bool, connect_reason_code : int, properties : list[Property]):
        variable_header = ConnackVariableHeader.from_args(session_present, connect_reason_code, properties)
        payload = ConnackPayload.from_args()
        
        type_and_flags = PacketFixedHeaderFlags.CONNACK
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.FIXED_HEADER : fixed_header,
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
        }

        return cls(None, None, **kwargs)
