# verify kiasu-bc 6r semifree colliison-38
from ulity import *

k0 = state_str_to_int("0e7b3f0ededc6852bb9100005959c6ac")
k0 = bytes([element for row in k0 for element in row])
p_k0 = state_str_to_int("98083b3229ff6c7043509500b598c2ac")
p_k0 = bytes([element for row in p_k0 for element in row])
print("k0:", extract_hex(bytes(k0)))
print("p_k0:", extract_hex(p_k0))
t = bytes(
    [
        0x98,
        0x08,
        0x00,
        0x00,
        0xC5,
        0x30,
        0x00,
        0x00,
        0xB5,
        0x7B,
        0x00,
        0x00,
        0xF9,
        0x33,
        0x00,
        0x00,
    ]
)
p_t = bytes(
    [
        0x98,
        0x08,
        0x00,
        0x00,
        0x29,
        0xF1,
        0x00,
        0x00,
        0xA1,
        0x7B,
        0x00,
        0x00,
        0x95,
        0x33,
        0x00,
        0x00,
    ]
)

x0 = xor_bytes(k0, t)
p_x0 = xor_bytes(p_k0, p_t)

keys = key_schedule(k0)
p_keys = key_schedule(p_k0)

X = []
p_X = []
Y = []
p_Y = []
Z = []
p_Z = []
W = []
p_W = []

for r in range(3):
    if r == 0:
        x = x0
        p_x = p_x0
        X.append(x0)
        p_X.append(p_x0)
    else:
        x = xor_bytes(keys[r], W[r - 1], t)
        p_x = xor_bytes(p_keys[r], p_W[r - 1], p_t)
        X.append(x)
        p_X.append(p_x)

    y = sub_state(bytes(x))
    p_y = sub_state(bytes(p_x))
    Y.append(y)
    p_Y.append(p_y)

    z = shift_rows(bytes(y))
    p_z = shift_rows(p_y)
    Z.append(z)
    p_Z.append(p_z)

    if r != 2:
        w = bytes()
        p_w = bytes()
        for i in range(4):
            w += mix_col(z[4 * i : 4 * i + 4])
            p_w += mix_col(p_z[4 * i : 4 * i + 4])
        W.append(w)
        p_W.append(p_w)


c = xor_bytes(Z[-1], keys[3], t)
p_c = xor_bytes(p_Z[-1], p_keys[3], p_t)
print("c:", extract_hex(c))
print("p_c:", extract_hex(p_c))
print("delta c:", extract_hex(xor_bytes(c, p_c)))
