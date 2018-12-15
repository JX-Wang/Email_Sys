#! usr/bin/env python
# encoding:utf8
"""
Email System Smtp Base
=======================
Author @ WUD
Data   @ 2018.12.4
Ver    @ 1.0
Others : NONE
"""
from Recv_email import Recv_email  # 邮件解析模块儿
from Encryption import Encryption  # 加密模块儿
from email.parser import Parser
from Tkinter import *  # UI
from tkinter import ttk
import smtplib  # smtp send email
from poplib import POP3  # smtp receive email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import easygui  # 选择附件窗口

import sys  # 中文编码问题
reload(sys)
sys.setdefaultencoding('utf-8')


class EmailSystem:
    def __init__(self):
        self.EMail_UI = Tk()
        self.user = ""
        self.passwd = ""
        self.Smtp_Server = ""
        self.pop_server = ""
        self.receiver = ""
        self.subject = ""
        self._send_text = ""
        self.path = []
        self.black_lists = []  # 黑名单
        self.black_num = 0

    def pop3_init(self):
        """与POP3服务器建立连接"""
        try:
            self.pop3_server = POP3(self.pop_server)
            self.pop3_server.user(self.user)
            self.pop3_server.pass_(self.passwd)
        except Exception as e:
            print "POP CONNECT ERROR ->", str(e)

    def destory_windows(self):
        self.remain_windows.destroy()

    def send_email(self):
        try:
            self.receiver = self.param_3.get()
            self.subject = self.param_4.get()
            self._send_text = self.param_5.get("0.0", "end")
        except Exception as e:
            print "RECEIVER INTO ERROR ->", str(e)
        print self.receiver, self.subject, self._send_text
        # 加入文本消息
        msg = MIMEMultipart()
        msg['From'] = 'WUD_EMAIL_SYSTEM <' + self.user + '>'
        msg['To'] = self.receiver
        msg['Subject'] = self.subject
        _send_text = Encryption().Encry_text(str(self._send_text))  # AES加密后的密文
        _send_text = MIMEText(_send_text, 'plain', 'utf-8')
        msg.attach(_send_text)

        # 加密文件
        cipher_path = []
        for path in self.path:
            cipher_path.append(Encryption().Encry_file(path))  # 加密图片文件
        self.path[:] = []
        for path in cipher_path:
            self.path.append(path)  # 将加密后的附件路径添加至发送列表

        # 添加附件 文件路径不能包含中文
        if len(self.path) != 0:
            try:
                for file_path in self.path:
                    print file_path
                    file_part = MIMEApplication(open(file_path, 'rb').read())
                    file_part.add_header('Content-Disposition', 'attachment', filename=file_path)
                    msg.attach(file_part)
                print "ADD SUCCESS"
            except Exception as e:
                print "ADD FILE ERROR ->", str(e)

        self.server.set_debuglevel(1)
        self.server = smtplib.SMTP(self.Smtp_Server, 25)  # 与邮件服务器重新建立连接
        self.server.login(self.user, self.passwd)  # 重新登入
        self.remain_windows = Tk()
        self.remain_windows.title("提示消息")
        try:
            self.server.sendmail(self.user, self.receiver, msg.as_string())
            self.server.quit()
            remain_lable = Frame(self.remain_windows)
            Label(remain_lable, text="Send Success!").pack(fill="y", expand="yes")
            remain_lable.pack()
            self.remain_windows.mainloop()
        except Exception as e:
            print "Send Error - >", str(e)
            remain_lable = Frame(self.remain_windows)
            Label(remain_lable, text="Send Failed!").pack(fill="y", expand="yes")
            remain_lable.pack()
            self.remain_windows.mainloop()

        exit_button = Frame(self.remain_windows)
        Button(exit_button, text="Confirm", command=self.destory_windows).pack()
        exit_button.pack()

    def add_file(self):
        try:
            _path = easygui.fileopenbox()
            if _path is None:
                # 没有选择文件
                return 1
            else:
                self.path.append(_path)
                for i in self.path:
                    # 显示添加到附件信息
                    if self.path.index(i) == 0:
                        Label(self.main_windows, text=i).place(x=250, y=(self.path.index(i)+1)*30 + 350)
                    else:
                        Label(self.main_windows, text=i).place(x=250, y=(self.path.index(i)+1)*20 + 360)
        except Exception as e:
            print "ADD FILE ERROR ->", str(e)

    def main_windows_destroy(self):
        """退出发送窗口, 填写数据清空"""
        self.main_windows.destroy()  # 销毁控制台
        self.path[:] = []  # 清空附件列表
        self.receiver = ""
        self.subject = ""
        self._send_text = ""

    def send_windows(self):
        """邮件系统主控制台"""
        try:
            self.EMail_UI.destroy()  # 清除初始化窗口
            self.check.destroy()  # 清除提示窗口
        except:
            pass
        self.main_windows = Tk()  # 主窗口控件
        self.main_windows.title("邮件系统主控制台")
        self.main_windows.geometry('800x600')  # 控制台大小
        self.main_windows.resizable(width=True, height=True)

        # 当前用户信息
        Label(self.main_windows, text="User: ").place(x=600, y=10)
        Label(self.main_windows, text=self.user).place(x=635, y=10)

        # 滚动条
        scroll_bar = Scrollbar(self.main_windows)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # 提示文字
        Label(self.main_windows, text="收件人:", background='#6699ff').place(x=10, y=10)
        Label(self.main_windows, text="主题:", background='#6688ff').place(x=10, y=40)
        Label(self.main_windows, text="正文:", background='#6677ff').place(x=10, y=70)

        # 输入窗口 接收人+主题+邮件内容
        self.param_3 = Entry(self.main_windows)
        self.param_3.place(x=70, y=10)
        self.param_4 = Entry(self.main_windows)
        self.param_4.place(x=70, y=40)
        self.param_5 = Text(self.main_windows, width=100, height=20, yscrollcommand=scroll_bar.set)
        self.param_5.place(x=70, y=70)

        # 添加附件按钮
        Button(self.main_windows, text="添加附件", command=self.add_file, width=10).place(x=250, y=350)

        # 加密方式
        Label(self.main_windows, text="加密方式:").place(x=10, y=350)
        self.encryption = ttk.Combobox(self.main_windows)
        self.encryption.place(x=70, y=350)
        self.encryption['value'] = ('AES', "base64")  # 默认使用AES加密，还有一个激就是默认的base64
        self.encryption.current(0)  # 默认rc4_md5加密

        # 按钮 发送+退出
        Button(self.main_windows, text="发送", command=self.send_email, width=10).place(x=600, y=350)  # 登陆成功后点击确认进入主要界面
        Button(self.main_windows, text="退出", command=self.main_windows_destroy, width=10).place(x=700, y=350)  # 退出邮箱系统
        self.main_windows.mainloop()

    def delete_msg(self):
        """删除邮件"""
        for i in range(0, len(self.msg)+1):
            if self.msg_list.select_includes(i):
                self.pop3_server.dele(i)  # 从pop服务器中删除邮件
                self.msg_list.delete(i, i)  # 在界面消失，并不从pop服务器删除

    def sys_quit(self):
        """结束程序"""
        self.index_window.destroy()
        sys.exit(0)

    def open_email(self, mouse):
        """打开，阅读邮件"""
        self.pop3_init()  # 等待时间可能过长，与pop3服务器重新建立连接
        # 找到当前邮件位置
        for i in range(0, len(self.msg)+1):
            if self.msg_list.select_includes(i):
                id_flag = list(self.msg_list.curselection())[0]
                print id_flag
                break
        rep, text, size = self.pop3_server.retr(self.stmp_num - id_flag)
        msg_content = b'\r\n'.join(text).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        print msg
        header_list = Recv_email().info_digest(msg)  # 包含From To Subject
        content = Recv_email().email_box(msg)
        try:
            self.EMail_UI.destroy()  # 清除初始化窗口
            self.check.destroy()  # 清除提示窗口
        except:
            pass
        self.open_email_windows = Tk()  # 主窗口控件
        self.open_email_windows.title("查阅邮件控制台")
        self.open_email_windows.geometry('900x600')  # 控制台大小
        self.open_email_windows.resizable(width=True, height=True)

        # 当前用户信息
        # Label(self.open_email_windows, text="User: ").place(x=600, y=10)
        # Label(self.open_email_windows, text=self.user).place(x=635, y=10)

        # 提示文字
        Label(self.open_email_windows, text="发件人:", background='#6699ff').place(x=10, y=10)
        Label(self.open_email_windows, text="主题:", background='#6688ff').place(x=10, y=40)
        # Label(self.open_email_windows, text="来自:", background='#6677ff').place(x=10, y=40)
        Label(self.open_email_windows, text="正文:", background='#6666ff').place(x=10, y=70)

        # 展示窗口 接收人+主题+邮件内容
        # self.param_3 = Label(self.open_email_windows, text=list[1])  # 收件人
        # self.param_3.place(x=70, y=10)
        self.param_4 = Label(self.open_email_windows, text=header_list[2])  # 主题
        self.param_4.place(x=70, y=40)
        self.param_5 = Label(self.open_email_windows, text=header_list[0])  # 发件人
        self.param_5.place(x=70, y=10)

        # 滚动条
        scroll_bar = Scrollbar(self.open_email_windows)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # 文件内容
        text_info = Text(self.open_email_windows, yscrollcommand=scroll_bar.set, font="宋体,15", width=100, height=30)
        text_info.place(x=70, y=70)
        # text_info.insert(END, content)
        text_info.insert(END, content)

        # 添加附件按钮
        # Button(self.open_email_windows, text="添加附件", command=self.add_file, width=10).place(x=10, y=390)

        # 加密方式
        # Label(self.open_email_windows, text="加密方式:").place(x=10, y=350)
        # self.encryption = ttk.Combobox(self.open_email_windows)
        # self.encryption.place(x=70, y=350)
        # self.encryption['value'] = ('rc4_md5', 'RSA', 'DES', 'AES', 'IDEA')
        # self.encryption.current(0)  # 默认rc4_md5加密

        # 按钮 发送+退出
        # Button(self.open_email_windows, text="发送", command=self.send_email, width=10).place(x=600, y=350)  # 登陆成功后点击确认进入主要界面

        Button(self.open_email_windows, text="退出", command=self.open_email_windows.destroy, width=10).place(x=800, y=560)  # 退出邮箱系统
        self.open_email_windows.mainloop()

    def add_black_list(self):
        """处理黑名单"""
        black_name = self.black_name.get()
        if black_name == "":
            print black_name
            print "no message"
        else:
            print black_name
            self.black_lists.append(str(black_name))
            self.black_list.insert(END, str(black_name))

    def delete_black_name(self):
        self.black_lists[:] = []
        self.black_list.delete(self.black_list.curselection(), self.black_list.curselection())

    def black_list_windows(self):
        """黑名单模块"""
        self.bl_windows = Tk()
        self.bl_windows.title("邮箱黑名单")
        self.bl_windows.geometry("300x200")
        self.bl_windows.resizable(width=False, height=False)

        # 输入窗口
        self.black_name = Entry(self.bl_windows)
        self.black_name.place(x=10, y=10)

        # 滚动条
        scroll_bar = Scrollbar(self.bl_windows)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # 按钮
        Button(self.bl_windows, text=" 加入 ", command=self.add_black_list).place(x=170, y=9)
        Button(self.bl_windows, text=" 清空 ", command=self.delete_black_name).place(x=220, y=9)

        # 显示
        self.black_list = Listbox(self.bl_windows, yscrollcommand=scroll_bar.set, width=35)
        self.black_list.place(x=10, y=40)

        if len(self.black_lists) != 0:
            for bl in self.black_lists:
                self.black_list.insert(END, bl)

        self.bl_windows.mainloop()

    def index_windows(self):
        """主界面"""
        self.index_window = Tk()
        self.index_window.title("index windows")
        self.index_window.resizable(width=False, height=False)
        self.index_window.geometry('900x700')

        # 当前用户信息
        Label(self.index_window, text="User: ").place(x=620, y=5)
        Label(self.index_window, text=self.user).place(x=655, y=5)

        # 滚动条
        scroll_bar = Scrollbar(self.index_window)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_bar_x = Scrollbar(self.index_window)
        scroll_bar_x.pack(side=BOTTOM, fill=X)

        # 收件信息窗口
        self.msg_list = Listbox(self.index_window, yscrollcommand=scroll_bar.set, xscrollcommand=scroll_bar_x.set,
                              width=110, height=30, font="宋体,15", selectmode=BROWSE)
        self.msg_list.place(x=0, y=30)
        self.msg_list.bind(sequence="<Double-Button-1>", func=self.open_email)

        # 登陆POP服务器 POP.XXX.XXX
        try:
            self.pop3_server = POP3(self.pop_server)
            self.pop3_server.user(self.user)
            self.pop3_server.pass_(self.passwd)
        except Exception as e:
            print "POP CONNECT ERROR ->", str(e)

        rep, self.msg, size = self.pop3_server.list()  # self.msg为全部收信

        all_recv_email = []
        email_num = len(self.msg)
        self.stmp_num = email_num
        while email_num > 0:
            try:
                rep, text, size = self.pop3_server.retr(email_num)
                msg_content = b'\r\n'.join(text).decode().encode('utf-8')
                msg = Parser().parsestr(msg_content)
                list = Recv_email().info_digest(msg)
                list.insert(0, str(self.stmp_num - email_num + 1) + " : ")
                all_recv_email.append(list)
            except Exception as e:
                print "POP PARSER ERROR ->", str(e)
                pass
            email_num -= 1

        for item in all_recv_email:
            if len(self.black_lists) != 0:
                if str(item[1]).find(self.black_lists[0]) != -1:
                    print self.black_lists[0]
                    print "THIS EMAIL IN BLACK LIST"
                    self.black_num += 1
                    pass
                else:
                    print str(item[1])
                    Id = str(item[0])
                    From = 'From: ' + str(item[1])
                    To = 'To: ' + str(item[2])
                    Subject = 'Subject: ' + item[3]
                    parma = Id + From + To + Subject
                    self.msg_list.insert(END, parma)
            else:
                self.black_num = 0
                Id = str(item[0])
                From = 'From: ' + str(item[1])
                To = 'To: ' + str(item[2])
                Subject = 'Subject: ' + item[3]
                parma = Id + From + To + Subject
                self.msg_list.insert(END, parma)
            # print parma
        scroll_bar.config(command=self.msg_list.yview)

        # 提示信息
        Label(self.index_window, text="收件箱: " + str(len(self.msg) - self.black_num) + "封", bg="#e6ebe0",
              font="黑体, 15").place(x=0, y=0)

        # 收件箱按钮
        # Button(self.index_window, text="已发送", command=self.delete_msg, width=8). place(x=200, y=0)

        # 删除按钮
        Button(self.index_window, text="删除", command=self.delete_msg, width=8). place(x=0, y=580)

        # 刷新按钮
        Button(self.index_window, text="刷新", command=self.index_windows, width=8). place(x=90, y=580)

        # 读取按钮
        # Button(self.index_window, text="打开", command=self.delete_msg, width=8). place(x=180, y=580)

        # 写信按钮
        Button(self.index_window, text="写信", command=self.send_windows, width=8). place(x=680, y=580)

        # 退出按钮
        Button(self.index_window, text="退出", command=self.sys_quit, width=8). place(x=780, y=580)

        # 邮箱信息验证？
        # 待添加

        # 伪造邮件地址黑名单
        Button(self.index_window, text="设置黑名单", command=self.black_list_windows, width=8). place(x=780, y=620)

        # 删除其他窗口
        try:
            self.EMail_UI.destroy()  # 清除初始化窗口
            self.check.destroy()  # 清除提示窗口
        except:
            pass

        # 循环
        self.index_window.mainloop()

    def check(self):
        """检查输入是否正确"""
        self.check = Tk()
        self.check.title("检查登陆")
        self.check.geometry('300x90')
        self.check.resizable(width=False, height=False)
        remain_info_text = Frame(self.check)
        try:
            self.user = self.param_1.get()
            self.passwd = self.param_2.get()
            self.Smtp_Server = "smtp." + self.user[self.user.index('@')+1:]  # smtp服务器
            self.pop_server = "pop3." + self.user[self.user.index('@')+1:]  # pop服务器
        except:
            Label(remain_info_text, text="ERROR:Check Your Input").pack(fill="y", expand="yes")
            remain_info_text.pack()

        try:
            self.server = smtplib.SMTP(self.Smtp_Server, 25)  # 与邮件服务器建立连接
            Label(remain_info_text, text="SMTP Connect Success").pack(fill="y", expand="yes")
            remain_info_text.pack()
        except Exception as e:
            print "SMTP Connect Error - >", str(e)
            remain_info_text = Frame(self.check)
            Label(remain_info_text, text="ERROR:SMTP Connect ERROR").pack(fill="y", expand="yes")
            remain_info_text.pack()
            self.EMail_UI.mainloop()

        try:
            self.server.login(self.user, self.passwd)
            self.server.quit()
            print "Log In success"
            remain_info_text = Frame(self.check)
            Label(remain_info_text, text="Log In Success").pack(fill="y", expand="yes")
            remain_info_text.pack()
            confirm_button_frame = Frame(self.check)
            Button(confirm_button_frame, text="Confirm", command=self.index_windows).pack()  # 登陆成功后点击确认进入主要界面
            confirm_button_frame.pack()
        except Exception as e:
            print "Log In Error - >", str(e)
            remain_info_text = Frame(self.check)
            Label(remain_info_text, text="ERROR:Check your passwd").pack(fill="y", expand="yes")
            remain_info_text.pack()

    def main(self):
        self.param_1 = StringVar()
        self.param_2 = StringVar()
        self.EMail_UI.title("Email System - Powered by WUD")
        self.EMail_UI.geometry('300x130')
        self.EMail_UI.resizable(width=True, height=True)

        # 系统文字
        """
        main_text_frame = Frame(self.EMail_UI)
        Label(main_text_frame,
              text="WUD信箱",
              font=('宋体', 20)
              ).pack()
        main_text_frame.pack(side=TOP)
        """

        # 提示文字
        Label(self.EMail_UI, text="用户名:").place(x=35, y=10)
        Label(self.EMail_UI, text="密码:").place(x=35, y=40)

        # 输入信息
        Entry(self.EMail_UI, textvariable=self.param_1).place(x=110, y=10)
        Entry(self.EMail_UI, textvariable=self.param_2, show='*').place(x=110, y=40)  # 加密输入

        # 按钮
        Button(self.EMail_UI, text='登陆', command=self.check, bg='white', width=10, height=1).place(x=40, y=80)
        Button(self.EMail_UI, text='退出', command=self.EMail_UI.destroy, bg='white', width=10, height=1).place(x=170, y=80)

        # 循环
        self.EMail_UI.mainloop()


if __name__ == '__main__':
    E = EmailSystem()
    E.main()
