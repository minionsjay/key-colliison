# verify aes-192 5r colliison-59
from ulity import *

k0 = state_str_to_int("4936599cabf802baeaf076a7fbd9fba30e7fd7a114008928")
k0 = bytes([element for row in k0 for element in row])

keys = key_schedule(k0)

delta_k = state_str_to_int("313156623131562a313153623131532a0000004800000000")
delta_k = [element for row in delta_k for element in row]
p_k = xor_bytes(delta_k, k0)
p_keys = key_schedule(p_k)

k0 = keys[0]
p_k0 = p_keys[0]

print("k0:", extract_hex(bytes(k0)))
print("p_k0:", extract_hex(p_k0))
print("delta k0:", extract_hex(xor_bytes(k0, p_k0)))


p = bytes([0x00] * 16)

X = []
p_X = []
Y = []
p_Y = []
Z = []
p_Z = []
W = []
p_W = []

for r in range(5):
    if r == 0:
        x = xor_bytes(keys[r], p)
        p_x = xor_bytes(p_keys[r], p)
        X.append(x)
        p_X.append(p_x)
    else:
        x = xor_bytes(keys[r], W[r - 1])
        p_x = xor_bytes(p_keys[r], p_W[r - 1])
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

    if r != 4:
        w = bytes()
        p_w = bytes()
        for i in range(4):
            w += mix_col(z[4 * i : 4 * i + 4])
            p_w += mix_col(p_z[4 * i : 4 * i + 4])
        W.append(w)
        p_W.append(p_w)


c = xor_bytes(Z[-1], keys[5])
p_c = xor_bytes(p_Z[-1], p_keys[5])
print("c:", extract_hex(c))
print("p_c:", extract_hex(p_c))
print("delta c:", extract_hex(xor_bytes(c, p_c)))
