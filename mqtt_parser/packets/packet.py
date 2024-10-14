from mqtt_data_types import ByteInteger, Literals, PacketType, VariableByteInteger
from StreamReader import StreamReader
from utils import split_byte, update_flag_byte

class MQTTFixedHeader:
    def __init__(self, stream : StreamReader, **kwargs):
        if stream is None:
            self.init_from_args(**kwargs)
        else:
            self.init_from_stream(stream)

    def init_from_stream(self, stream : StreamReader):
        self.type_and_flags = ByteInteger(stream, **{'timeout' : None})
        self.packet_type, self.flags = split_byte(self.type_and_flags.value)
        self.remaining_length = VariableByteInteger(stream)

    def init_from_args(self, **kwargs):
        self.type_and_flags = kwargs[Literals.TYPE_AND_FLAGS]
        self.packet_type, self.flags = split_byte(self.type_and_flags.value)
        self.remaining_length = kwargs[Literals.REMAINING_LENGTH]
       
    def __str__(self):
        return_string = "\t********* Fixed Header *********\n"
        return_string += f"\t\tPacket Type:{self.packet_type}\n"
        return_string += f"\t\tRemaining Length:{self.remaining_length}\n"
        return_string += f"\t\tFlags:{self.flags}\n"
        return return_string

    def to_bytes(self):
        attributes = ['type_and_flags', 'remaining_length']
        return b''.join([getattr(self, attr).to_bytes() for attr in attributes if attr is not None])


    @classmethod
    def from_args(cls, type_and_flags : int, remaining_length : int):
        kwargs = { 
            Literals.REMAINING_LENGTH : VariableByteInteger.from_args(remaining_length),
            Literals.TYPE_AND_FLAGS : ByteInteger.from_args(type_and_flags)            
            }
        return cls(None, **kwargs)

    @classmethod
    def build_type_and_flags_byte(cls, packet_type : int, fixed_header_flags : int):
        type_and_flags = update_flag_byte(0, fixed_header_flags, 0, 3)
        type_and_flags = update_flag_byte(type_and_flags, packet_type, 4,7)
        return type_and_flags

    def as_json(self, exclude = []):
        return f"{{\"Packet Type\": \"{PacketType(self.packet_type).name}\",\"Remaining Length\": {self.remaining_length},\"Flags\": {self.flags}}}"

class MQTTVariableHeader:
    def init_from_args(self, **kwargs):
        raise NotImplementedError("Implement this method in child class")
    
    def init_from_stream(self, fixed_header : MQTTFixedHeader, stream : StreamReader):
        raise NotImplementedError("Implement this method in child class")
    
    def __init__(self, fixed_header : MQTTFixedHeader, stream : StreamReader, **kwargs):
        if stream is None:
            self.init_from_args(**kwargs)
        else:
            self.init_from_stream(fixed_header, stream)

    def __str__(self):
        return "\t********* Variable Header *********\n"

    def as_json(self, exclude = []):
        data = self.__dict__.copy()

        for field in exclude:
            data.pop(field, None)

        return data

class MQTTPayload:
    def init_from_args(self, **kwargs):
        raise NotImplementedError("Implement this method in child class")
    
    def init_from_stream(self, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader, stream: StreamReader):
        raise NotImplementedError("Implement this method in child class")

    def __init__(self, fixed_header : MQTTFixedHeader, variable_header : MQTTVariableHeader, stream : StreamReader, **kwargs):
        if stream is None:
            self.init_from_args(**kwargs)
        else:
            self.init_from_stream(fixed_header, variable_header, stream)

    def __str__(self):
        return "\t********* Payload *********\n"

    def as_json(self, exclude = []):
        data = self.__dict__.copy()

        for field in exclude:
            data.pop(field, None)

        return data


class Packet:
    # initialized by child classes
    VARIABLE_HEADER_CLASS = None
    PAYLOAD_CLASS = None
    NAME = None

    # the name of the fields in this 
    def init_from_args(self, fixed_header : MQTTFixedHeader, variable_header : MQTTVariableHeader, payload : MQTTPayload):
        self.fixed_header       = fixed_header
        self.variable_header    = variable_header
        self.payload            = payload

    def init_from_stream(self, fixed_header : MQTTFixedHeader, stream : StreamReader):
        self.fixed_header = fixed_header
        self.variable_header = self.VARIABLE_HEADER_CLASS(fixed_header, stream)
        self.payload = self.PAYLOAD_CLASS(fixed_header, self.variable_header, stream)
    
    def __init__(self, fixed_header : MQTTFixedHeader, stream : StreamReader, **kwargs):
        if stream is None:
            fixed_header = kwargs[Literals.FIXED_HEADER]
            variable_header = kwargs[Literals.VARIABLE_HEADER]
            payload = kwargs[Literals.PAYLOAD]
            self.init_from_args(fixed_header, variable_header, payload) 
        else:
            self.init_from_stream(fixed_header, stream)
    
    def __str__(self):
        return_string = "{:*^50}".format(f"{self.NAME} Packet")[:50]  + "\n"
        return_string += self.fixed_header.__str__()
        return_string += self.variable_header.__str__()
        return_string += self.payload.__str__()
        return return_string

    def to_bytes(self):
        attributes = ['fixed_header', 'variable_header', 'payload']
        return b''.join([getattr(self, attr).to_bytes() for attr in attributes if attr is not None])

    def as_json(self):
        return f"{{\"fixed_header\": {self.fixed_header.as_json()},\"variable_header\": {self.variable_header.as_json()},\"payload\": {self.payload.as_json()}}}".replace("None", "null").replace('\'', '\"')