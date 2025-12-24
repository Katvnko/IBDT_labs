def hex_to_little_endian(hex_value: str) -> int:
    hex_value = hex_value.replace(" ", "").lower()
    data = bytes.fromhex(hex_value)
    return int.from_bytes(data, byteorder="little", signed=False)


def hex_to_big_endian(hex_value: str) -> int:
    hex_value = hex_value.replace(" ", "").lower()
    data = bytes.fromhex(hex_value)
    return int.from_bytes(data, byteorder="big", signed=False)


def little_endian_to_hex(value: int, num_bytes: int) -> str:
    data = value.to_bytes(num_bytes, byteorder="little", signed=False)
    return data.hex()


def big_endian_to_hex(value: int, num_bytes: int) -> str:
    data = value.to_bytes(num_bytes, byteorder="big", signed=False)
    return data.hex()
