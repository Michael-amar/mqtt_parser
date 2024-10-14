from mqtt_data_types import *
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader

class SubackVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header: MQTTFixedHeader, stream: StreamReader):
        length_before = stream.tell()

        self.packet_identifier = TwoByteInteger(stream)
        self.properties = Properties(stream)

        self.length = stream.tell() - length_before

    def init_from_args(self, **kwargs):
        self.packet_identifier = kwargs[Literals.PACKET_IDENTIFIER]
        self.properties = kwargs[Literals.PROPERTIES]
        self.value = kwargs[Literals.LENGTH]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tPacket Identifier:{self.packet_identifier}\n"
        return_string += f"\t\tProperties:{self.properties}\n"
        return return_string
    
    def to_bytes(self):
        attributes = ['packet_identifier', 'properties']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])
   
    @classmethod
    def from_args(cls, packet_identifier : int, properties : list[Properties]):
        identifier = TwoByteInteger.from_args(packet_identifier)
        props = Properties.from_args(properties)
        length = len(identifier.to_bytes()) + len(props.to_bytes())
        kwargs = {
            Literals.PACKET_IDENTIFIER : identifier,
            Literals.PROPERTIES : props,
            Literals.LENGTH : length
        }
        return cls(fixed_header=None, stream=None, **kwargs)
    
class SubackPayload(MQTTPayload):

    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : SubackVariableHeader, stream : StreamReader):
        payload_length = fixed_header.remaining_length.value - variable_header.length

        self.reason_codes : list[ReasonCode] = []
        number_of_bytes_read = stream.tell()
        while (stream.tell() - number_of_bytes_read) < payload_length:
            reason_code = ReasonCode(stream)
            self.reason_codes.append(reason_code)

    def init_from_args(self, **kwargs):
        self.reason_codes = kwargs[Literals.REASON_CODES]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tReason Codes :[{','.join([reason_code.__str__() for reason_code in self.reason_codes])}]\n"
        return return_string

    def to_bytes(self):
        return b''.join([reason_code.to_bytes() for reason_code in self.reason_codes])
    
    @classmethod
    def from_args(cls, reason_codes : list[int]):
        r_codes : list[ByteInteger] = [ByteInteger.from_args(reason_code) for reason_code in reason_codes]
        kwargs = {
            Literals.REASON_CODES : r_codes
        }
        return cls(fixed_header=None, variable_header=None, stream=None, **kwargs)
    
class SubackPacket(Packet):
    VARIABLE_HEADER_CLASS = SubackVariableHeader
    PAYLOAD_CLASS = SubackPayload
    NAME = "Suback"

    @classmethod
    def from_args(cls, packet_identifier : int, properties : list[Properties], reason_codes : list[int]):
        variable_header = SubackVariableHeader.from_args(packet_identifier, properties)
        payload = SubackPayload.from_args(reason_codes)

        type_and_flags = PacketFixedHeaderFlags.SUBACK
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)