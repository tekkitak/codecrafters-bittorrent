from typing import Any
import json
import sys
from bencode import Bencode

bc = Bencode()

def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.

    if command == "decode":
        bencoded_value: bytes = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data: Any) -> str:
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        # Uncomment this block to pass the first stage
        print(json.dumps(bc.decode(bencoded_value), default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
