from typing import Any
import json
import sys
from hashlib import sha1

from app.bencode import Bencode

bc = Bencode()

def decode(bcode: bytes):
    def bytes_to_str(data: Any) -> str:
        if isinstance(data, bytes):
            return data.decode()

        raise TypeError(f"Type not serializable: {type(data)}")

    # Uncomment this block to pass the first stage
    return json.dumps(bc.decode(bcode), default=bytes_to_str)

def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value: bytes = sys.argv[2].encode()

        print(decode(bencoded_value))
    elif command == "info":
        with open(sys.argv[2], "rb") as f:
            info: dict[str, Any] = bc.decode(f.readline())
            info_hash = sha1(bc.encode(info["info"]))
            print(f"Tracker URL: {info['announce']}")
            print(f"Length: {info['info']['length']}")
            print(f"Info Hash: {info_hash.hexdigest()}")
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
