# usr/bin/env python
# encoding: utf-8

# 导入DES模块
from Cryptodome.Cipher import DES
import binascii

# 这是密钥
key = b'abcdefgh'
# 需要去生成一个DES对象
des = DES.new(key, DES.MODE_ECB)
# 需要加密的数据
text = 'python spider!'
text = text + (8 - (len(text) % 8)) * '='

# 加密的过程
encrypto_text = des.encrypt(text.encode())
encrypto_text = binascii.b2a_hex(encrypto_text)
print(encrypto_text)

