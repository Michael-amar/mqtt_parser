from abc import abstractmethod

import websockets.sync.server
import websockets.sync
import websockets


class StreamReader:
    """
    reads n bytes from the stream at a time
    """
    @abstractmethod
    def read(self, n : int, **kwargs) -> bytearray:
        pass

    """
    returns the number of bytes read so far
    """
    @abstractmethod
    def tell(self) -> int:
        pass


class BytesStreamReader(StreamReader):
    def __init__(self, byte_array):
        self.stream = byte_array
        self.position = 0

    def read(self, n, **kwargs):
        if n < 0:
            raise ValueError("n must be non-negative")

        if self.position + n > len(self.stream):
            raise Exception("Not enough bytes available to read")

        start = self.position
        end = self.position + n
        self.position = end

        res = self.stream[start:end]
        return res

    def tell(self):
        return self.position


class WebsocketStreamReader(StreamReader):
    def __init__(self, websocket: websockets.sync.server.ServerConnection):
        self.websocket = websocket
        self.buffer = b''
        self.buffer_copy = b''  # copy of the received bytes
        self.bytes_read = 0

    def read(self, n, **kwargs):
        timeout = kwargs.get('timeout', 2)  # defualt timeout after 2 seconds
        while len(self.buffer) < n:
            temp_buffer = self.websocket.recv(timeout=None)
            self.buffer += temp_buffer
            self.buffer_copy += temp_buffer

        self.bytes_read += n
        return_buffer = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return return_buffer

    def tell(self):
        return self.bytes_read
