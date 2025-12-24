from hex_endian.converter import (
    hex_to_little_endian,
    hex_to_big_endian,
    little_endian_to_hex,
    big_endian_to_hex
)

# Vector 1
v1 = "ff" + "00" * 31
print(hex_to_little_endian(v1))
print(hex_to_big_endian(v1))

# Vector 2
v2 = "aaaa" + "00" * 30
print(hex_to_little_endian(v2))
print(hex_to_big_endian(v2))

# Vector 3
v3 = "FFFFFFFF"
print(hex_to_little_endian(v3))
print(hex_to_big_endian(v3))

# Vector 4 (512 bytes)
v4 = "f0" + "00" * 511
print(hex_to_little_endian(v4))
print(hex_to_big_endian(v4))