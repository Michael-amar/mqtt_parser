from .StreamReader import *
from enum import IntEnum, StrEnum

class PacketFixedHeaderFlags(IntEnum):
    CONNECT     = 0b00010000
    CONNACK     = 0b00100000
    PUBACK      = 0b01000000
    PUBREC      = 0b01010000
    PUBREL      = 0b01100010
    PUBCOMP     = 0b01110000
    SUBSCRIBE   = 0b10000010
    SUBACK      = 0b10010000
    UNSUBSCRIBE = 0b10100010
    UNSUBACK    = 0b10110000
    PINGREQ     = 0b11000000
    PINGRESP    = 0b11010000
    DISCONNECT  = 0b11100000
    AUTH        = 0b11110000

class PacketType(IntEnum):
    CONNECT     = 1
    CONNACK     = 2
    PUBLISH     = 3
    PUBACK      = 4
    PUBREC      = 5
    PUBREL      = 6
    PUBCOMP     = 7
    SUBSCRIBE   = 8
    SUBACK      = 9
    UNSUBSCRIBE = 10
    UNSUBACK    = 11
    PINGREQ     = 12
    PINGRESP    = 13
    DISCONNECT  = 14
    AUTH        = 15

class PropertyIdentifier(IntEnum):
    PAYLOAD_FORMAT_INDICATOR            = 0x01
    MESSAGE_EXPIRY_INTERVAL             = 0x02
    CONTENT_TYPE                        = 0x03
    RESPONSE_TOPIC                      = 0x08
    CORRELATION_DATA                    = 0x09
    SUBSCRIPTION_IDENTIFIER             = 0x0b
    SESSION_EXPIRY_LEVEL                = 0x11
    ASSIGNED_CLIENT_IDENTIFIER          = 0x12
    SERVER_KEEP_ALIVE                   = 0x13
    AUTHENTICATION_METHOD               = 0x15
    AUTHENTICATION_DATA                 = 0x16
    REQUEST_PROBLEMT_INFORMATION        = 0x17
    WILL_DELAY_INTERVAL                 = 0x18
    REQEST_RESPONSE_INFORMATION         = 0x19
    RESPONSE_INFORMATION                = 0x1a
    SERVER_REFERENCE                    = 0x1c
    REASON_STRING                       = 0x1f
    RECEIVE_MAXIMUM                     = 0x21
    TOPIC_ALIAS_MAXIMUM                 = 0x22
    TOPIC_ALIAS                         = 0x23
    MAXIMUM_QOS                         = 0x24
    RETAIN_AVAILABLE                    = 0x25
    USER_PROPERTY                       = 0x26
    MAXIMUM_PACKET_SIZE                 = 0x27
    WILDCARD_SUBSCRIPTION_AVAILABLE     = 0x28
    SUBSCRIPTION_IDENTIFIER_AVAILABLE   = 0x29
    SHARED_SUBSCRIPTION_AVAILABLE       = 0x2a

class ReasonCodeEnum(IntEnum):
    SUCCESS                                 = 0x00
    NORMAL_DISCONNECT                       = 0x00
    GRANTED_QOS_0                           = 0x00
    GRANTED_QOS_1                           = 0x01
    GRANTES_QOS_2                           = 0x02
    DISCONNECT_WITH_WILL_MESSAGE            = 0x04
    NO_MATCHING_SUBSCRIBERS                 = 0x10
    NO_SUBSCRIPTION_EXISTED                 = 0x11
    CONTINUE_AUTHENTICATION                 = 0x18
    REAUTHENTICATE                          = 0x19
    UNSPECIFIED_ERROR                       = 0x80
    MALFORMED_PACKET                        = 0x81
    PROTOCOL_ERROR                          = 0x82
    IMPLEMENTATION_SPECIFIC_EROROR          = 0x83
    UNSUPPORTED_PROTOCOL_VERSION            = 0x84
    CLIENT_IDENTIFIER_NOT_VALID             = 0x85
    BAD_USER_NAME_OR_PASSWORD               = 0x86
    NOT_AUTHORIZED                          = 0x87
    SERVER_UNAVAILABLE                      = 0x88
    SERVER_BUSY                             = 0x89
    BANNED                                  = 0x8A
    SERVER_SHUTTING_DOWN                    = 0x8B
    BAD_AUTHENTICATION_METHOD               = 0x8c
    KEEP_ALIVE_TIMEOUT                      = 0x8D
    SESSION_TAKEN_OVER                      = 0x8E
    TOPIC_FILTER_INVALID                    = 0x8F
    TOPIC_NAME_INVALID                      = 0x90
    PACKED_IDENTIFIER_IN_USE                = 0x91
    PACKET_IDENTIFIER_NOT_FOUND             = 0x92
    RECEIVE_MAXIMUM_EXCEEDED                = 0x93
    TOPIC_ALIAS_INVALID                     = 0x94
    PACKET_TOO_LARGE                        = 0x95
    MESSAGE_RATE_TOO_HIGH                   = 0x96
    QUOTA_EXCEEDED                          = 0x97
    ADMINISTRATIVE_ACTION                   = 0x98
    PAYLOAD_FORMAT_INVALID                  = 0x99
    RETAIN_NOT_SUPPORTED                    = 0x9A
    QOS_NOT_SUPPORTED                       = 0x9B
    USE_ANOTHER_SERVER                      = 0x9C
    SERVER_MOVED                            = 0x9D
    SHARED_SUBSCRIPTIONS_NOT_SUPPORTED      = 0x9E
    CONNECTION_RATE_EXCEEDED                = 0x9F
    MAXIMUM_CONNECT_TIMEOUT                 = 0xA0
    SUBSCRIPTION_IDENTIFIERS_NOT_SUPPORTED  = 0xA1
    WILDCARD_SUBSCRIPTIONS_NOT_SUPPORTED    = 0xA2

class Literals(StrEnum):
    # used globally
    FIXED_HEADER                = "Fixed Header"
    VARIABLE_HEADER             = "Variable Header"
    PAYLOAD                     = "Payload"
    REASON_CODE                 = "Reason Code"
    PACKET_IDENTIFIER           = "Packet Identifier"
    TOPIC_NAME                  = "Topic Name"
    REASON_CODES                = "Reason Codes"
    PAYLOAD_LENGTH              = "Payload Length"
    TOPICS                      = "Topics"

    # used in MQTTFixedHeader kwargs
    TYPE_AND_FLAGS              = "Type And Flags"
    REMAINING_LENGTH            = "Remaining Length"

    # used in ConnackVariableHeader kwargs
    CONNECT_ACKNOWLEDGE_FLAGS   = "Connect Acknowledge Flags"
    CONNECT_REASON_CODE         = "Connect Reason Code"
    PROPERTIES                  = "Properties"

    # used in ConnectVariableHeader kwargs
    PROTOCOL_NAME               = "Protocol Name"
    PROTOCOL_VERSION            = "Protocol Version"
    CONNECT_FLAGS               = "Connect Flags"
    KEEP_ALIVE                  = "Keep Alive"

    # used in ConnectPayload kwargs
    CLIENT_ID                   = "Client Id"
    WILL_TOPIC                  = "Will Topic"
    WILL_PAYLOAD                = "Will Payload"
    USERNAME                    = "Username"
    PASSWORD                    = "Password"

    # used in MQTTDataTypes kwargs
    VALUE                       = 'Value'
    LENGTH                      = 'Length'
    STRING                      = 'String'
    DATA                        = 'Data'
    NAME                        = 'Name'
    PROPERTY_CODE               = 'Property Code'
    PROPERTIES_LENGTH           = "Properties Length"

class MQTTDataType():
    def __init__(self, stream : StreamReader, **kwargs):
        if stream is None:
            self.init_from_args(**kwargs)
        else:
            self.init_from_stream(stream, **kwargs)

    def __repr__(self):
        return self.__str__()

class VariableByteInteger(MQTTDataType):
    """
    The Variable Byte Integer is encoded using an encoding scheme which uses a single byte for values up
    to 127. Larger values are handled as follows. The least significant seven bits of each byte encode the
    data, and the most significant bit is used to indicate whether there are bytes following in the
    representation. Thus, each byte encodes 128 values and a "continuation bit". The maximum number of 
    bytes in the Variable Byte Integer field is four.
    """
    def init_from_stream(self, stream : StreamReader, **kwargs):
        multiplier = 1
        value = 0
        while True:
            encoded_byte = int.from_bytes(stream.read(1))
            value += (encoded_byte & 127) * multiplier
            multiplier *= 128
            if multiplier > 128*128*128:
                raise Exception("Malformaed variable byte integer")
            if ((encoded_byte & 128) == 0):
                break
        self.value = value

    def init_from_args(self, **kwargs):
        self.value = kwargs[Literals.VALUE]
        
    def to_bytes(self):
        output = b''
        value = self.value
        while True:
            encoded_byte = value % 128
            value = value // 128
            if value > 0:
                encoded_byte = encoded_byte | 128
            output += encoded_byte.to_bytes(1)
            if value <= 0:
                break
        
        return output

    def __str__(self):
        return self.value.__str__()
    
    @classmethod
    def from_args(cls, value : int):
        kwargs = {Literals.VALUE : value}
        return cls(None, **kwargs)

class ByteInteger(MQTTDataType):
    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.value = int.from_bytes(stream.read(1, **kwargs))

    def init_from_args(self, **kwargs):
        self.value = kwargs[Literals.VALUE]
            
    def to_bytes(self):
        return self.value.to_bytes(1)

    def __str__(self):
        return self.value.__str__()
    
    @classmethod
    def from_args(cls, num : int):
        kwargs = {Literals.VALUE : num}
        return cls(None, **kwargs)        
    
class TwoByteInteger(MQTTDataType):

    def init_from_stream(self, stream: StreamReader, **kwargs):
        self.value = int.from_bytes(stream.read(2, **kwargs), byteorder='big')

    def init_from_args(self, **kwargs):
        self.value = kwargs[Literals.VALUE]

    def to_bytes(self):
        return self.value.to_bytes(2, "big")
    
    def __str__(self):
        return self.value.__str__()
    
    @classmethod
    def from_args(cls, value : int):
        kwargs = {Literals.VALUE : value}
        return cls(None, **kwargs)
    
class FourByteInteger(MQTTDataType):

    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.value = int.from_bytes(stream.read(4, **kwargs), byteorder='big')

    def init_from_args(self, **kwargs):
        self.value = kwargs[Literals.VALUE]        
    
    def to_bytes(self):
        return self.value.to_bytes(4, "big")

    def __str__(self):
        return self.value.__str__()
    
    @classmethod
    def from_args(cls, value : int):
        kwargs = {Literals.VALUE : value}
        return cls(None, **kwargs)
    
class Utf8EncodedString(MQTTDataType):

    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.length = TwoByteInteger(stream, **kwargs)
        self.string = stream.read(self.length.value).decode('utf-8')

    def init_from_args(self, **kwargs):
        self.length = kwargs[Literals.LENGTH]
        self.string = kwargs[Literals.STRING]
        
    def to_bytes(self):
        return self.length.to_bytes() + self.string.encode('utf-8')
    
    def __str__(self):
        return f"\"{self.string}\""

    @classmethod
    def from_args(cls, string : str):
        kwargs = {Literals.LENGTH : TwoByteInteger.from_args(len(string)),
                  Literals.STRING : string}
        return cls(None, **kwargs)


class BinaryData(MQTTDataType):

    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.length = TwoByteInteger(stream, **kwargs)
        self.data = stream.read(self.length.value, **kwargs)

    def init_from_args(self, **kwargs):
        self.length = kwargs[Literals.LENGTH]
        self.data = kwargs[Literals.DATA]

    def to_bytes(self):
        return self.length.to_bytes() + self.data
    
    def __str__(self):
        return f"\"{self.data.decode('utf-8', 'latin1')}\""


    @classmethod
    def from_args(cls, data : bytes):
        kwargs = {Literals.DATA : data, Literals.LENGTH : TwoByteInteger.from_args(len(data))}
        return cls(None, **kwargs)

class ReasonCode(MQTTDataType):
    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.reason_code : ByteInteger = ByteInteger(stream, **kwargs)

    def init_from_args(self, **kwargs):
        self.reason_code : ByteInteger = kwargs[Literals.REASON_CODE] 
    
    def to_bytes(self):
        return self.reason_code.to_bytes()
    
    def __str__(self):
        return f"\"{ReasonCodeEnum(self.reason_code.value).name}\""

    @classmethod
    def from_args(cls, reason_code : ReasonCodeEnum):
        kwargs = {
            Literals.REASON_CODE : ByteInteger.from_args(reason_code),
        }
        return cls(None, **kwargs)

class Utf8StringPair(MQTTDataType):

    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.name = Utf8EncodedString(stream, **kwargs)
        self.value = Utf8EncodedString(stream, **kwargs)

    def init_from_args(self, **kwargs):
        self.name = kwargs[Literals.NAME]
        self.value = kwargs[Literals.VALUE]

    
    def to_bytes(self):
        return self.name.to_bytes() + self.value.to_bytes()
    
    def __str__(self):
        return f"{{ {self.name} : {self.value} }}"

    def __repr__(self):
        return f"{{{self.name} : {self.value}}}"

    @classmethod
    def from_args(cls, name : str, value : str):
        kwargs = {
            Literals.NAME : Utf8EncodedString.from_args(name),
            Literals.VALUE : Utf8EncodedString.from_args(value)
        }
        return cls(None, **kwargs)

class Property(MQTTDataType):
    """
    A Property consists of an Identifier which defines its usage and data type, followed by a value. The
    Identifier is encoded as a Variable Byte Integer    
    """

    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.property_code = VariableByteInteger(stream)
        match self.property_code.value:
                case PropertyIdentifier.PAYLOAD_FORMAT_INDICATOR:
                    value = ByteInteger(stream)
                case PropertyIdentifier.MESSAGE_EXPIRY_INTERVAL:
                    value = FourByteInteger(stream)
                case PropertyIdentifier.CONTENT_TYPE:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.RESPONSE_TOPIC:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.CORRELATION_DATA:
                    value = BinaryData(stream)
                case PropertyIdentifier.SUBSCRIPTION_IDENTIFIER:
                    value = VariableByteInteger(stream)
                case PropertyIdentifier.SESSION_EXPIRY_LEVEL:
                    value = FourByteInteger(stream)
                case PropertyIdentifier.ASSIGNED_CLIENT_IDENTIFIER:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.SERVER_KEEP_ALIVE:
                    value = TwoByteInteger(stream)
                case PropertyIdentifier.AUTHENTICATION_METHOD:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.AUTHENTICATION_DATA:
                    value = BinaryData(stream)
                case PropertyIdentifier.REQUEST_PROBLEMT_INFORMATION:
                    value = ByteInteger(stream)
                case PropertyIdentifier.WILL_DELAY_INTERVAL:
                    value = FourByteInteger(stream)
                case PropertyIdentifier.REQEST_RESPONSE_INFORMATION:
                    value = ByteInteger(stream)
                case PropertyIdentifier.RESPONSE_INFORMATION:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.SERVER_REFERENCE:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.REASON_STRING:
                    value = Utf8EncodedString(stream)
                case PropertyIdentifier.RECEIVE_MAXIMUM:
                    value = TwoByteInteger(stream)
                case PropertyIdentifier.TOPIC_ALIAS_MAXIMUM:
                    value = TwoByteInteger(stream)
                case PropertyIdentifier.TOPIC_ALIAS:
                    value = TwoByteInteger(stream)
                case PropertyIdentifier.MAXIMUM_QOS:
                    value = ByteInteger(stream)
                case PropertyIdentifier.RETAIN_AVAILABLE:
                    value = ByteInteger(stream)
                case PropertyIdentifier.USER_PROPERTY:
                    value = Utf8StringPair(stream)
                case PropertyIdentifier.MAXIMUM_PACKET_SIZE:
                    value = FourByteInteger(stream)
                case PropertyIdentifier.WILDCARD_SUBSCRIPTION_AVAILABLE:
                    value = ByteInteger(stream)
                case PropertyIdentifier.SUBSCRIPTION_IDENTIFIER_AVAILABLE:
                    value = ByteInteger(stream)
                case PropertyIdentifier.SHARED_SUBSCRIPTION_AVAILABLE:
                    value = ByteInteger(stream)
            
        self.value = value

    def init_from_args(self, **kwargs):
        self.property_code = kwargs[Literals.PROPERTY_CODE]
        self.value = kwargs[Literals.VALUE]

    def to_bytes(self):
        return self.property_code.to_bytes() + self.value.to_bytes()

    def __str__(self):
        return f"\"{PropertyIdentifier(self.property_code.value).name}\" : {self.value.__str__()} "

    @classmethod
    def from_args(cls, property_code : PropertyIdentifier, value : int | str | list[str] | bytes):
        if property_code in [PropertyIdentifier.PAYLOAD_FORMAT_INDICATOR,           PropertyIdentifier.REQUEST_PROBLEMT_INFORMATION, 
                             PropertyIdentifier.REQEST_RESPONSE_INFORMATION,        PropertyIdentifier.MAXIMUM_QOS, 
                             PropertyIdentifier.RETAIN_AVAILABLE,                   PropertyIdentifier.WILDCARD_SUBSCRIPTION_AVAILABLE, 
                             PropertyIdentifier.SUBSCRIPTION_IDENTIFIER_AVAILABLE,  PropertyIdentifier.SHARED_SUBSCRIPTION_AVAILABLE]:
            value = ByteInteger.from_args(value)
        elif property_code in [PropertyIdentifier.SERVER_KEEP_ALIVE,    PropertyIdentifier.RECEIVE_MAXIMUM,
                               PropertyIdentifier.TOPIC_ALIAS_MAXIMUM,  PropertyIdentifier.TOPIC_ALIAS,]:
            value = TwoByteInteger.from_args(value)
        elif property_code in [PropertyIdentifier.MESSAGE_EXPIRY_INTERVAL,      PropertyIdentifier.SESSION_EXPIRY_LEVEL,
                               PropertyIdentifier.WILL_DELAY_INTERVAL,          PropertyIdentifier.MAXIMUM_PACKET_SIZE]:
            value = FourByteInteger.from_args(value)
        elif property_code in [PropertyIdentifier.CONTENT_TYPE,                 PropertyIdentifier.RESPONSE_TOPIC,
                               PropertyIdentifier.ASSIGNED_CLIENT_IDENTIFIER,   PropertyIdentifier.AUTHENTICATION_METHOD,
                               PropertyIdentifier.RESPONSE_INFORMATION,         PropertyIdentifier.SERVER_REFERENCE,
                               PropertyIdentifier.REASON_STRING]:
            value = Utf8EncodedString.from_args(value)
        elif property_code in [PropertyIdentifier.CORRELATION_DATA, PropertyIdentifier.AUTHENTICATION_DATA]:
            value = BinaryData.from_args(value)
        elif property_code in [PropertyIdentifier.USER_PROPERTY]:
            value = Utf8StringPair.from_args(value)
        elif property_code in [PropertyIdentifier.SUBSCRIPTION_IDENTIFIER]:
            value = VariableByteInteger.from_args(value)
        kwargs = {
            Literals.PROPERTY_CODE : property_code,
            Literals.VALUE         : value
        }
        return cls(None, **kwargs)

class Properties(MQTTDataType):
    '''
    The set of Properties is composed of a Property Length followed by the Properties
    The Property Length is encoded as a Variable Byte Integer
    '''
    def init_from_stream(self, stream : StreamReader, **kwargs):
        self.properties_length = VariableByteInteger(stream)
        self.properties : list[Property]= []
        number_of_bytes_read = stream.tell()
        while (stream.tell() - number_of_bytes_read) < self.properties_length.value:
            property = Property(stream)
            self.properties.append(property)

    def init_from_args(self, **kwargs):
        self.properties_length = kwargs[Literals.PROPERTIES_LENGTH]
        self.properties = kwargs[Literals.PROPERTIES]

    def to_bytes(self):
        if self.properties_length is None:
            return b''
        else:
            return self.properties_length.to_bytes() + b''.join([property.to_bytes() for property in self.properties])
    
    def __str__(self):
        if self.properties_length is None or self.properties_length == 0:
            return 'None'
        else:
            return '{' + ','.join([f'{propertyy.__str__()}' for propertyy in self.properties]) + '}'
        
    @classmethod
    def from_args(cls, properties : list[Property] | None):
        if properties is None:
            properties_length = None
        else: 
            properties_length = sum([len(property.to_bytes()) for property in properties])
            properties_length = VariableByteInteger.from_args(properties_length)
        kwargs ={
            Literals.PROPERTIES_LENGTH : properties_length,
            Literals.PROPERTIES         : properties
        }
        return cls(None, **kwargs)
