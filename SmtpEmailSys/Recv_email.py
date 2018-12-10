# encoding:utf8

from poplib import POP3
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


pop3_server = POP3("pop3.wangjunx.top")
pop3_server.user("wud@wangjunx.top")
pop3_server.pass_("949501holdon0.0")
rep, msg, size = pop3_server.list()
print rep

class Recv_email:
    def __init__(self):
        pass
        # self.pop3_server = POP3("pop3.wangjunx.top")
        # self.pop3_server.user("wud@wangjunx.top")
        # self.pop3_server.pass_("949501holdon0.0")
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

    def email_box(self, msg, indent=0):
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                print('%s%s: %s' % ('  ' * indent, header, value))

        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                print('%sText: %s' % ('  ' * indent, content + '...'))
                self.text = content
            else:
                print('%sAttachment: %s' % ('  ' * indent, content_type))

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


if __name__ == '__main__':
    pass
    for i in range(1, len(msg)+1):
        try:
            rep, text, size = pop3_server.retr(i)
            msg_content = b'\r\n'.join(text).decode().encode('utf-8')
            msg = Parser().parsestr(msg_content)
            Recv_email().email_box(msg)
        except Exception as e:
            print "Error -> ", str(e)
            pass
    pop3_server.quit()

