# Installation
pip install "git+http://gitlab.TWshop/michaela/mqtt_parser.git" 

# Info
The parser supports 2 mqtt versions 4 and 5.
The version is always mentioned in the first packet sent to the server - the CONNECT packet which is version independent.

When parsing a CONNECT packet the parser uses the version field of this packet to parse the following packets.
If you don't have a CONNECT packet, or you just want to parse a single mqtt message, you should mention the version - either 4 or 5.
If you don't mention the version the default is 4.

# Usage
In the following example the parser detects the version because its a CONNECT packet.
Any subsequent packets will be parsed with the version of this packet.

```python 
import mqtt_parser
from pprint import pprint
msg = "101a00044d5154540402003c000e6d717474785f3465633166353562"
packet = mqtt_parser.parse(bytearray.fromhex(msg))
pprint(packet)


>>> {'fixed_header': {'Flags': 0, 'Packet Type': 'CONNECT', 'Remaining Length': 26},
 'payload': {'client_id': 'mqttx_4ec1f55b',
             'password': None,
             'properties': None,
             'username': None,
             'will_payload': None,
             'will_topic': None},
 'variable_header': {'clean_start': 1,
                     'connect_flags': 2,
                     'keep_alive': 60,
                     'password_flag': 0,
                     'properties': None,
                     'protocol_name': 'MQTT',
                     'protocol_version': 4,
                     'reserved': 0,
                     'username_flag': 0,
                     'will_flag': 0,
                     'will_qos': 0,
                     'will_retain': 0}}
```

In the following example we want to parse this packet as a stand-alone packet.
A CONNECT packet wasn't parsed before this packet so we need to mention the version manually.
```python
import mqtt_parser
from pprint import pprint
msg2 = "82106c4d020b040008746573747474747402"
packet = mqtt_parser.parse(bytearray.fromhex(msg2), version = 5)
pprint(packet)
{'fixed_header': {'Flags': 2,
                  'Packet Type': 'SUBSCRIBE',
                  'Remaining Length': 16},
 'payload': {'topic options': [{'testtttt': 2}]},
 'variable_header': {'length': 5,
                     'packet_identifier': 27725,
                     'properties': {'SUBSCRIPTION_IDENTIFIER': 4}}}
```
