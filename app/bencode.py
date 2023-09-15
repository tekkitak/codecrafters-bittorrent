from typing import Any, Generator

class Bencode():
    def __init__(self):
        self.cur_gen: Generator[str,Any,bool]|None = None

    def __string_gen(self, string: str) -> Generator[str, None, bool]:
        for char in string:
            yield(char)
        return True

    def decode(self, bcode: bytes) -> Any:
        self.cur_gen = self.__string_gen(str(bcode))
        
        ch = next(self.cur_gen)
        if ch == 'i': # Number
            pass
        elif ch == 'l': # List
            pass
        elif ch == 'd': # Dict
            pass
        elif ch.isdigit():
            pass
        else:
            raise ValueError(f"{ch} is no valid type in bcode!")
        pass

    def __decode_str(self, bcode: str) -> str:
        if bcode[0].isdigit():
            length = int(bcode.split(":")[0])
            return bcode.split(":")[1][:length]
        else:
            raise TypeError("Given bcode is not a string!")