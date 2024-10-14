from mqtt_data_types import *
from packets.packet import  Packet, MQTTVariableHeader, MQTTPayload, MQTTFixedHeader
from StreamReader import StreamReader
from utils import update_flag_byte
from enum import Enum



class ConnectVariableHeader(MQTTVariableHeader):
    def init_from_stream(self, fixed_header : MQTTFixedHeader, stream : StreamReader):
        self.protocol_name = Utf8EncodedString(stream) 

        self.protocol_version = ByteInteger(stream)

        self.connect_flags = ByteInteger(stream)

        self.username_flag = (self.connect_flags.value >> 7) & 0b1
        self.password_flag = (self.connect_flags.value >> 6) & 0b1
        self.will_retain   = (self.connect_flags.value >> 5) & 0b1
        self.will_qos      = (self.connect_flags.value >> 3) & 0b11
        self.will_flag     = (self.connect_flags.value >> 2) & 0b1
        self.clean_start   = (self.connect_flags.value >> 1) & 0b1
        self.reserved      = (self.connect_flags.value >> 0) & 0b1

        self.keep_alive = TwoByteInteger(stream)

        if self.protocol_version.value == 5:
            self.properties = Properties(stream)
        else:
            self.properties = None

    def init_from_args(self, **kwargs):
        self.protocol_name = kwargs[Literals.PROTOCOL_NAME]
        self.protocol_version = kwargs[Literals.PROTOCOL_VERSION]
        self.connect_flags = kwargs[Literals.CONNECT_FLAGS]

        self.username_flag = (self.connect_flags.value >> 7) & 0b1
        self.password_flag = (self.connect_flags.value >> 6) & 0b1
        self.will_retain   = (self.connect_flags.value >> 5) & 0b1
        self.will_qos      = (self.connect_flags.value >> 3) & 0b11
        self.will_flag     = (self.connect_flags.value >> 2) & 0b1
        self.clean_start   = (self.connect_flags.value >> 1) & 0b1
        self.reserved      = (self.connect_flags.value >> 0) & 0b1

        self.keep_alive = kwargs[Literals.KEEP_ALIVE]
        self.properties = kwargs[Literals.PROPERTIES]

    def __str__(self):
        return_string = super().__str__()
        
        return_string += f"\t\tProtocol Name:{self.protocol_name}\n"
        return_string += f"\t\tProtocol Version:{self.protocol_version}\n"
        return_string += f"\t\tConnect Flags:{self.connect_flags}\n"
        return_string += f"\t\t\tClean Start:{self.clean_start}\n"
        return_string += f"\t\t\tReserved:{self.reserved}\n"
        return_string += f"\t\t\tWill Flag:{self.will_flag}\n"
        return_string += f"\t\t\tWill qos:{self.will_qos}\n"
        return_string += f"\t\t\tWill Retain:{self.will_retain}\n"
        return_string += f"\t\t\tUser Name Flag:{self.username_flag}\n"
        return_string += f"\t\t\tPassword Flag:{self.password_flag}\n"
        return_string += f"\t\t\tKeep Alive:{self.keep_alive}\n"
        if (self.properties is not None):
            return_string += f"\t\tProperties:{self.properties}\n"
        else:
            return_string += f"\t\tProperties: None\n"

        return return_string
    
    def to_bytes(self):
        attributes = ['protocol_name', 'protocol_version', 'connect_flags', 'keep_alive', 'properties']
        return b''.join([getattr(self, attr).to_bytes() for attr in attributes if attr is not None])

    @classmethod
    def from_args(cls, protocol_name : str, protocol_version : int,  username_flag : bool,  password_flag : bool,  will_retain : bool,  will_qos : bool,  will_flag : bool,  clean_start : bool,  keep_alive : int,  variable_header_properties : list[Property]):
        kwargs = {}
        kwargs[Literals.PROTOCOL_NAME] = Utf8EncodedString.from_args(protocol_name)
        kwargs[Literals.PROTOCOL_VERSION] = ByteInteger.from_args(protocol_version)
        flags_byte = 0
        flags_byte = update_flag_byte(flags_byte, username_flag, 7, 7)
        flags_byte = update_flag_byte(flags_byte, password_flag, 6, 6)
        flags_byte = update_flag_byte(flags_byte, will_retain, 5, 5)
        flags_byte = update_flag_byte(flags_byte, will_qos, 3, 4)
        flags_byte = update_flag_byte(flags_byte, will_flag, 2, 2)
        flags_byte = update_flag_byte(flags_byte, clean_start, 1, 1)
        kwargs[Literals.CONNECT_FLAGS] = ByteInteger.from_args(flags_byte)
        kwargs[Literals.KEEP_ALIVE] = TwoByteInteger.from_args(keep_alive)
        kwargs[Literals.PROPERTIES] = Properties.from_args(variable_header_properties)
        return cls(fixed_header=None, stream=None, **kwargs)

class ConnectPayload(MQTTPayload):

    def init_from_stream(self, fixed_header : MQTTFixedHeader, variable_header : ConnectVariableHeader, stream : StreamReader):
        self.will_topic, self.will_payload, self.username, self.password, self.properties = None, None, None, None, None
        self.client_id = Utf8EncodedString(stream)

        if variable_header.will_flag:
            
            self.properties = Properties(stream)

            self.will_topic = Utf8EncodedString(stream)

            self.will_payload = BinaryData(stream)

        if variable_header.username_flag:
            self.username = Utf8EncodedString(stream)

        if variable_header.password_flag:
            self.password = BinaryData(stream)

    def init_from_args(self, **kwargs):
        self.client_id = kwargs[Literals.CLIENT_ID]
        self.properties = kwargs[Literals.PROPERTIES]
        self.will_topic = kwargs[Literals.WILL_TOPIC]
        self.will_payload = kwargs[Literals.WILL_PAYLOAD]
        self.username = kwargs[Literals.USERNAME]
        self.password = kwargs[Literals.PASSWORD]

    def __str__(self):
        return_string = super().__str__()
        return_string += f"\t\tClient Id:{self.client_id}\n"
        return_string += f"\t\tWill Topic:{self.will_topic}\n"
        return_string += f"\t\tWill Payload:{self.will_payload}\n"
        return_string += f"\t\tUser Name:{self.username}\n"
        return_string += f"\t\tPassword:{self.password}\n"
        return_string += f"\t\tProperties:{self.properties}\n"
        return return_string

    def to_bytes(self):
        attributes = ['client_id', 'will_topic', 'will_payload', 'username', 'password', 'properties']
        return b''.join([instance.to_bytes() for instance in [getattr(self, attr) for attr in attributes] if instance is not None])

    @classmethod
    def from_args(cls, client_id : str, payload_properties : list[Property], will_topic : str, will_payload : bytes, user_name : str, password : bytes):
        kwargs = {}
        kwargs[Literals.CLIENT_ID] = Utf8EncodedString.from_args(client_id)
        kwargs[Literals.PROPERTIES] = Properties.from_args(payload_properties)
        kwargs[Literals.WILL_TOPIC] = Utf8EncodedString.from_args(will_topic)
        kwargs[Literals.WILL_PAYLOAD] = BinaryData.from_args(will_payload)
        kwargs[Literals.USERNAME] = Utf8EncodedString.from_args(user_name)
        kwargs[Literals.PASSWORD] = BinaryData.from_args(password)
        return cls(fixed_header = None, variable_header = None, stream = None, **kwargs)

class ConnectPacket(Packet):
    VARIABLE_HEADER_CLASS =  ConnectVariableHeader
    PAYLOAD_CLASS = ConnectPayload
    NAME = "Connect"

    @classmethod
    def from_args(cls, protocol_name : str, protocol_version : int,  username_flag : bool,  password_flag : bool,  will_retain : bool,  will_qos : bool,  will_flag : bool,  clean_start : bool,  keep_alive : int,  variable_header_properties : list[Property],  
                  client_id : str,  payload_properties : list[Property],  will_topic : str,  will_payload : bytes,  user_name : str,  password : bytes):
        
        variable_header = ConnectVariableHeader.from_args(protocol_name, protocol_version, username_flag, password_flag, will_retain, will_qos, will_flag, clean_start, keep_alive, variable_header_properties)
        payload = ConnectPayload.from_args(client_id, payload_properties, will_topic, will_payload, user_name, password)
        
        type_and_flags = PacketFixedHeaderFlags.CONNECT
        remaining_length = len(variable_header.to_bytes()) + len(payload.to_bytes())
        fixed_header = MQTTFixedHeader.from_args(type_and_flags, remaining_length)

        kwargs = {
            Literals.VARIABLE_HEADER : variable_header,
            Literals.PAYLOAD : payload,
            Literals.FIXED_HEADER : fixed_header
        }

        return cls(fixed_header=None, stream=None, **kwargs)
    
    