from typing import Any, Generator

class Bencode():
    def __init__(self):
        self.cur_gen: Generator[str,Any,bool]|None = None

    def __string_gen(self, string: bytes) -> Generator[str, None, bool]:
        for char in string:
            yield(chr(char))
        return True

    def decode(self, bcode: bytes) -> Any:
        self.cur_gen = self.__string_gen(bcode)
        ch = next(self.cur_gen)
        if ch == 'i': # Number
            pass
        elif ch == 'l': # List
            pass
        elif ch == 'd': # Dict
            pass
        elif ch.isdigit():
            s_len = ch
            while ch != ':':
                ch = next(self.cur_gen)
                s_len += ch
            return self.__decode_str(int(s_len[:-1]))
        else:
            raise ValueError(f"{ch} is no valid type in bcode!")

    def __decode_str(self, str_len: int) -> str:
        out: str = ""
        for _ in range(str_len):
            # We asssume that there is no issue in bcode such we dont need to check if its char
            out += next(self.cur_gen) # type: ignore

        return out