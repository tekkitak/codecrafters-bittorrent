from typing import Any, Generator

BCGen = Generator[str, None, bool]
class Bencode():
    def __init__(self):
        self.cur_gen: Generator[str,Any,bool]|None = None

    def __string_gen(self, string: bytes) -> BCGen:
        for char in string:
            yield(chr(char))
        return True

    def decode(self, bcode: bytes) -> Any:
        cur_gen = self.__string_gen(bcode)
        return self.__decode(cur_gen)

    def __decode(self, cur_gen: BCGen) -> Any:
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
        out: str = ""
        for n in gen:
            if n == 'e':
                break
            out += n
        return int(out)


    def __decode_str(self, str_len: int, gen: BCGen) -> str:
        out: str = ""
        for _ in range(str_len):
            out += next(gen)

        return out