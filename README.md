# Installation
pip install "git+http://gitlab.TWshop/michaela/mqtt_parser.git" 

# Info
The parser supports 2 mqtt versions 4 and 5.
The version is always mentioned in the first packet sent to the server - the CONNECT packet.

When parsing a CONNECT packet the parser uses the version field of this packet to parse the following packets.
If you don't have a CONNECT packet, or you just want to parse a single mqtt message, you should mention the version - either 4 or 5.
If you don't mention the version the default is 4.

# Usage


