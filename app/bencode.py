from typing import Any, Generator

BCGen = Generator[str, None, bool]
class Bencode():
    """Decode and encode bencode"""
    def __init__(self):
        self.cur_gen: Generator[str,Any,bool]|None = None

    def __string_gen(self, string: bytes) -> BCGen:
        """Internal string generator"""
        for char in string:
            yield chr(char)
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
        if ch == 'i': # Number
            return self.__decode_int(cur_gen)
        elif ch == 'l': # List
            l: list[Any] = []
            while True:
                decoded: Any = self.__decode(cur_gen)
                if decoded == True:
                    break
                l.append(decoded)
            return l
        elif ch == 'd': # Dict
            d: dict[Any, Any] = {}
            while True:
                decoded: Any = self.__decode(cur_gen)
                if decoded == True:
                    break
                d[decoded] = self.__decode(cur_gen)
            return d
        elif ch == 'e': # End of block
            return True
        elif ch.isdigit():
            s_len = ch
            while ch != ':':
                ch = next(cur_gen)
                s_len += ch
            return self.__decode_str(int(s_len[:-1]), cur_gen)
        else:
            raise ValueError(f"{ch} is no valid type in bcode!")

    def __decode_int(self, gen: BCGen) -> int:
        """Decodes bencode number"""
        out: str = ""
        for n in gen:
            if n == 'e':
                break
            out += n
        return int(out)

    def __decode_str(self, str_len: int, gen: BCGen) -> str:
        """Decodes bencode str"""
        out: str = ""
        try:
            print(str_len)
            for _ in range(str_len):
                out += next(gen)
        except Exception as err:
            print(out)
            print(err)
            exit()

        return out

    def encode(self, data: Any) -> str:
        """Encodes given data to bencode string
        
        Keyword arguments:
        data -- Any data that will be converted
        """
        out: str = ""
        val: Any
        key: Any
        if isinstance(data, list):
            for val in data:
                out += self.encode(val)
            return f"l{out}e"
        elif isinstance(data, dict):
            for key, val in data.items():
                out += self.encode(key)
                out += self.encode(val)
            return f"d{out}e"
        elif isinstance(data, int):
            return f"i{data}e"
        elif isinstance(data, str):
            return f"{len(data)}:{data}"
        else:
            raise ValueError("Data is of unknown type")