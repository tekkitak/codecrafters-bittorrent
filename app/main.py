from typing import Any, Tuple
import json
import sys
from hashlib import sha1
import requests as rq
import urllib.parse 

from app.bencode import Bencode

bc = Bencode()
peer_id:int = 16714_65761_65787_15794
port:int = 1337

def get_info(bcode: bytes) -> Tuple[str, dict[str, Any]]:
    bencode_data: dict[str, Any] 
    try:
        bencode_data = bc.decode(bcode)
        return bencode_data['announce'], bencode_data['info']
    except Exception as error:
        print(error)
        print(bencode_data)
        exit()

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
        announce: str
        info: dict[str, Any]
        with open(sys.argv[2], "rb") as f:
            announce, info = get_info(b"".join(f.readlines()))
        info_hash = sha1(bc.encode(info))

        print(f"Tracker URL: {announce}")
        print(f"Length: {info['length']}")
        print(f"Info Hash: {info_hash.hexdigest()}")
        print(f"Piece Length: {info['piece length']}")
        print("Piece Hashes:")
        for piece_hash in piece_hashes(info['pieces']):
            print(piece_hash)
    elif command == "peers":
        announce: str
        info: dict[str, Any]
        with open(sys.argv[2], "rb") as f:
            announce, info = get_info(b"".join(f.readlines()))
        info_hash = sha1(bc.encode(info))

        params = {
            "info_hash": info_hash.digest(),
            "peer_id": peer_id,
            "port": port,
            "uploaded": 0,
            "downloaded": 0,
            "left": info["length"],
            "compact": 1,
        }
        response = rq.get(announce, params=params, timeout=1000)

        data: dict[str,str|int|bytes]= bc.decode(response.content)

        peer_data: bytes
        for peer_data in [data["peers"][i:i+6] for i in range(0,len(data["peers"]), 6)]: # type: ingore
            peer_ip = ".".join([str(byte) for byte in peer_data[:4]])
            peer_port: int = int.from_bytes(peer_data[4:], "big")
            print(f"{peer_ip}:{peer_port}")
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
