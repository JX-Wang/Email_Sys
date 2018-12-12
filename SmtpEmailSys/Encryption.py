# usr/bin/env python
# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Cryptodome.Cipher import AES # str不是16的倍数那就补足为16的倍数
from binascii import b2a_hex, a2b_hex

key = 'this is a key123'
inv_key = 'This is an IV456'


class Encryption:
    def __init__(self):
        self.declare = "wud"
        self.key = 'this is a key123'
        self.inv_key = 'This is an IV456'

    def Encry_file(self, path):
        """文件加密模块儿"""
        obj = AES.new(key, AES.MODE_OFB, inv_key)

        f = open(path, "rb")
        info = f.read()
        while len(info) % 16 != 0:
            info += '='

        ciphertext = b2a_hex(obj.encrypt(info))

        f_4 = open("1.bin", "wb")
        f_4.write(ciphertext)
        f_4.close()
        f.close()

        print "加密完成"

    def Decry_file(self, path):
        """文件解密模块儿"""
        obj = AES.new(key, AES.MODE_OFB, inv_key)
        f = open(path, "rb")
        info = f.read()
        f.close()
        plain = obj.decrypt(a2b_hex(info))
        f_3 = open("2.jpg", "wb")
        f_3.write(plain)
        f.close()
        print "解密完成"

    def Encry_text(self, message):

        obj = AES.new(key, AES.MODE_OFB, inv_key)

        while len(message) % 16 != 0:
            message += '='

        ciphertext = obj.encrypt(message)
        ciphertext = b2a_hex(ciphertext)
        return ciphertext
        # f = open("cipher.bin", "wb")
        # f.write(ciphertext)
        # f.close()
        #
        # f_4 = open("cipher.bin", "rb")
        # text = f_4.read()
        # obj_2 = AES.new(key, AES.MODE_OFB, inv_key)
        # plain_text = obj_2.decrypt(a2b_hex(text))
        # print plain_text


if __name__ == '__main__':
    message = "asjf;jg;awjf;j;afjfafasdfgf"
    path = "1.bin"
    Encryption().Decry_file(path)
