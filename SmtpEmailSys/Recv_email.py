# encoding:utf8

from poplib import POP3
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Recv_email:
    def __init__(self):
        pass
        # self.pop3_server = POP3("x")
        # self.pop3_server.user("x")
        # self.pop3_server.pass_("x")
        # rep, self.msg, size = self.pop3_server.list()  # self.msg为全部收信

    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def email_box(self, msg):
        """解析邮箱正文内容"""
        maintype = msg.get_content_maintype()
        print maintype
        if maintype == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    mail_content = part.get_payload(decode=True).strip()
                    return mail_content
                elif maintype == 'text':
                    mail_content = msg.get_payload(decode=True).strip()
                    return mail_content
        elif maintype == 'text':
            content = msg.get_payload(decode=True)
            charset = self.guess_charset(msg)
            if charset:
                content = content.decode(charset)
                return content
        else:
            pass
            print "content no contain in this function: ", maintype
            # print mail_content



    def info_digest(self, msg, indent=0):
        digest = []
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        subject = self.decode_str(value)
                        digest.append(subject)
                    if header == 'From':
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        From = u'%s <%s>' % (name, addr)
                        digest.append(From)
                    if header == 'To':
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        To = u'%s <%s>' % (name, addr)
                        digest.append(To)

        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                pass
                # print('%spart %s' % ('  ' * indent, n))
                # print('%s--------------------' % ('  ' * indent))
                # print
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                # print('%sText: %s' % ('  ' * indent, content + '...'))
            else:
                pass
                # print('%sAttachment: %s' % ('  ' * indent, content_type))
        return digest

    def show_msg(self, msg):
        # 循环信件中的每一个mime的数据块
        for par in msg.walk():
            if not par.is_multipart():  # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
                name = par.get_param("name")  # 如果是附件，这里就会取出附件的文件名
                if name:
                    # 有附件
                    # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                    h = email.Header.Header(name)
                    dh = email.Header.decode_header(h)
                    fname = dh[0][0]
                    print '附件名:', fname
                    data = par.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中

                    try:
                        f = open(fname, 'wb')  # 注意一定要用wb来打开文件，因为附件一般都是二进制文件
                    except:
                        print '附件名有非法字符，自动换一个'
                        f = open('aaaa', 'wb')
                    f.write(data)
                    f.close()
                else:
                    # 不是附件，是文本内容
                    print par.get_payload(decode=True)  # 解码出文本内容，直接输出来就可以了。

                print '+' * 60  # 用来区别各个部分的输出


if __name__ == '__main__':
    pass
    # for i in range(1, 31):
    #     try:
    #         rep, text, size = pop3_server.retr(i)
    #         # for line in text:
    #         #     print line
    #         # print "END --------------------------------------------- END"
    #         msg_content = b'\r\n'.join(text).decode().encode('utf-8')
    #         msg = Parser().parsestr(msg_content)
    #         Recv_email().email_box(msg)
    #     except Exception as e:
    #         print str(e)
    # pop3_server.quit()

