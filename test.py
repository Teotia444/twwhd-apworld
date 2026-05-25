from pymem import pymem
wwhd = pymem.Pymem("Cemu")

wwhd.write_char(0x000001e7b1be0000 + 0x28F8844, chr(0x31))
for i in range(20):
    a = wwhd.read_uchar(0x000001e7b1be0000 + 0x28F8844 + i)
    print(a)
