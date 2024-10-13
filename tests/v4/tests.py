import unittest
import mqtt_parser
from StreamReader import BytesStreamReader
from pprint import pprint
"""
just sanity check that no exceptions are raised during parsing
"""

if __name__ == '__main__':
    with open ('recorded_packets.txt', 'r') as f:
        for line in f:
            msg = line.split('msg:')[-1]
            packet = mqtt_parser.parse_mqtt(BytesStreamReader(bytes.fromhex(msg)))
            pprint(packet, indent=4)