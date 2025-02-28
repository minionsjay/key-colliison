# verify aes-128 2r colliison-40
from ulity import *


k0 = state_str_to_int("60ded0d98010de933785157a00287122")
k0 = [element for row in k0 for element in row]
x0 = k0

din_x_0 = state_str_to_int("5c3b3b4d00003b4d0b3b009300000000")
dout_x_0 = state_str_to_int("3bc499170000c4c1713900c400000000")

din_x_0 = [element for row in din_x_0 for element in row]
dout_x_0 = [element for row in dout_x_0 for element in row]


p_k0 = xor_bytes(bytes(din_x_0), bytes(k0))
print("k0:", extract_hex(bytes(k0)))
print("p_k0:", extract_hex(p_k0))

p_x0 = xor_bytes(bytes(din_x_0), bytes(x0))

y0 = sub_state(bytes(x0))
p_y0 = xor_bytes(bytes(dout_x_0), bytes(y0))

z0 = shift_rows(bytes(y0))
p_z0 = shift_rows(p_y0)

w0 = bytes()
p_w0 = bytes()
for i in range(4):
    w0 += mix_col(z0[4 * i : 4 * i + 4])
    p_w0 += mix_col(p_z0[4 * i : 4 * i + 4])

keys = key_schedule(bytes(k0))
p_keys = key_schedule(bytes(p_k0))

k1 = keys[1]
p_k1 = p_keys[1]

x1 = xor_bytes(k1, w0)
p_x1 = xor_bytes(p_k1, p_w0)

y1 = sub_state(x1)
p_y1 = sub_state(p_x1)

z1 = shift_rows(bytes(y1))

p_z1 = shift_rows(p_y1)

k2 = keys[2]
p_k2 = p_keys[2]

c = xor_bytes(k2, z1)
p_c = xor_bytes(p_k2, p_z1)
print("c:", extract_hex(c))
print("p_c:", extract_hex(p_c))
print("delta c:", extract_hex(xor_bytes(c, p_c)))
