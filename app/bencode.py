from typing import Any, Generator
import sys

BCGen = Generator[bytes, None, bool]
class Bencode():
    """Decode and encode bencode"""
    def __init__(self):
        self.cur_gen: BCGen|None = None

    def __string_gen(self, string: bytes) -> BCGen:
        """Internal string generator"""
        print("Stderr:\n", string, "\n", file=sys.stderr)
        for char in string:
            yield bytes([char])
        yield b''
        return True

    def decode(self, bcode: bytes) -> Any:
        """Takes bencode string and returns decoded data

        bcode -- Bencoded string
        """
        cur_gen = self.__string_gen(bcode)
        return self.__decode(cur_gen)

    def __decode(self, cur_gen: BCGen) -> Any:
        """Internal decode function, recursivly decodes bencode string

        cur_gen -- bencode string generator to continue from 
        """
        ch = next(cur_gen)
        if ch == b'i': # Number
            return self.__decode_int(cur_gen)
        elif ch == b'l': # List
            l: list[Any] = []
            while True:
                decoded: Any = self.__decode(cur_gen)
                if decoded is True:
                    print("DEBUG: ending list", file=sys.stderr)
                    break
                l.append(decoded)
            return l
        elif ch == b'd': # Dict
            d: dict[Any, Any] = {}
            while True:
                decoded: Any = self.__decode(cur_gen)
                if decoded is True:
                    break
                d[decoded] = self.__decode(cur_gen)
            return d
        elif ch == b'e': # End of block
            return True
        elif ch.isdigit():
            s_len = ch
            while ch != b':':
                ch = next(cur_gen)
                s_len += ch
            out = self.__decode_str(int(s_len[:-1]), cur_gen)
            try:
                return out.decode()
            except (UnicodeDecodeError, AttributeError):
                return out
        else:
            raise ValueError(f"{ch} is no valid type in bcode!")

    def __decode_int(self, gen: BCGen) -> int:
        """Decodes bencode number"""
        out: bytes = b""
        for n in gen:
            if n == b'e':
                break
            out += n
        return int(out)

    def __decode_str(self, str_len: int, gen: BCGen) -> bytes:
        """Decodes bencode str"""
        out: bytes = b""
        try:
            for _ in range(str_len):
                out += next(gen)
        except Exception as err:
            print(f"ERROR: \n\t{out=}\n\t{err=}\n\t{str_len=}", file=sys.stderr)
            exit()

        return out

    def encode(self, data: Any) -> bytes:
        """Encodes given data to bencode string
        
        Keyword arguments:
        data -- Any data that will be converted
        """
        out: bytearray
        val: Any
        key: Any
        if isinstance(data, list): # List
            out = bytearray(b'l')
            for val in data:
                out += self.encode(val)
            out += b'e'
            return bytes(out)
        elif isinstance(data, dict): # Dictionary
            out = bytearray(b'd')
            for key, val in data.items():
                out += self.encode(key)
                out += self.encode(val)
            out += b'e'
            return bytes(out)
        elif isinstance(data, int): # Integer
            return f"i{data}e".encode()
        elif isinstance(data, str) or isinstance(data, bytes): # String
            return f"{len(data)}:{data}".encode()
        else:
            print(f"ERROR: {data=}", file=sys.stderr)
            raise ValueError("Data is of unknown type")