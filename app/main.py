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

def piece_hashes(pieces: bytes) -> list[str]:
    hashes: list[str] = []
    for piece in [pieces[i:i+20] for i in range(0, len(pieces), 20)]:
        hashes.append(piece.hex())
    return hashes

def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value: bytes = sys.argv[2].encode()

        print(decode(bencoded_value))
    elif command == "info":
        with open(sys.argv[2], "rb") as f:
            bencode_data: dict[str, Any] = bc.decode(b''.join(f.readlines()))
        info: dict[str, Any] = bencode_data['info']
        announce: str = bencode_data['announce']
        # created_by: str = bencode_data['created_by']
        info_hash = sha1(bc.encode(info))

        print(f"Tracker URL: {announce}")
        print(f"Length: {info['length']}")
        print(f"Info Hash: {info_hash.hexdigest()}")
        print(f"Piece Length: {info['piece length']}")
        print("Piece Hashes:")
        for piece_hash in piece_hashes(info['pieces']):
            print(piece_hash)
    elif command == "debug":
        with open(sys.argv[2], "rb") as f:
            info: dict[str, Any] = bc.decode(b''.join(f.readlines()))
        info_hash = sha1(bc.encode(info["info"]))
        print(info)
        print(f"Hash: {info_hash.hexdigest()}")
        print("Piece hashes:", *piece_hashes(info['info']['pieces']), sep="\n\t")
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
