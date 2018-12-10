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
from Recv_email import Recv_email

from email.parser import Parser
from Tkinter import *  # UI
from tkinter import ttk
import smtplib  # smtp send email
from poplib import POP3  # smtp receive email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import easygui  # 选择附件窗口

import sys
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
        _send_text = MIMEText(self._send_text, 'plain', 'utf-8')
        msg.attach(_send_text)

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
                return 1
            else:
                self.path.append(_path)
        except Exception as e:
            print "ADD FILE ERROR ->", str(e)

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
        self.encryption['value'] = ('rc4_md5', 'RSA', 'DES', 'AES', 'IDEA')
        self.encryption.current(0)  # 默认rc4_md5加密

        # 按钮 发送+退出
        Button(self.main_windows, text="发送", command=self.send_email, width=10).place(x=600, y=350)  # 登陆成功后点击确认进入主要界面
        Button(self.main_windows, text="退出", command=self.main_windows.destroy, width=10).place(x=700, y=350)  # 退出邮箱系统
        self.main_windows.mainloop()

    def delete_msg(self):
        for i in range(0, 49):
            if self.msg_list.select_includes(i):
                self.msg_list.delete(i, i)

    def sys_quit(self):
        """结束程序"""
        self.index_window.destroy()
        sys.exit(0)

    def open_email(self, mouse):
        # 找到当前邮件位置
        for i in range(0, 49):
            if self.msg_list.select_includes(i):
                localtion = i
                break
        rep, text, size = self.pop3_server.retr(localtion+1)
        print text
        msg_content = b'\r\n'.join(text).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        list = Recv_email().info_digest(msg)  # 包含From To Subject

        try:
            self.EMail_UI.destroy()  # 清除初始化窗口
            self.check.destroy()  # 清除提示窗口
        except:
            pass
        self.open_email_windows = Tk()  # 主窗口控件
        self.open_email_windows.title("查阅邮件控制台")
        self.open_email_windows.geometry('800x600')  # 控制台大小
        self.open_email_windows.resizable(width=True, height=True)

        # 当前用户信息
        # Label(self.open_email_windows, text="User: ").place(x=600, y=10)
        # Label(self.open_email_windows, text=self.user).place(x=635, y=10)

        # 提示文字
        Label(self.open_email_windows, text="收件人:", background='#6699ff').place(x=10, y=10)
        Label(self.open_email_windows, text="主题:", background='#6688ff').place(x=10, y=70)
        Label(self.open_email_windows, text="来自:", background='#6677ff').place(x=10, y=40)
        Label(self.open_email_windows, text="正文:", background='#6666ff').place(x=10, y=100)

        # 展示窗口 接收人+主题+邮件内容
        self.param_3 = Label(self.open_email_windows, text=list[1])  # 收件人
        self.param_3.place(x=70, y=10)
        self.param_4 = Label(self.open_email_windows, text=list[2])  # 主题
        self.param_4.place(x=70, y=70)
        self.param_5 = Label(self.open_email_windows, text=list[0])  # 发件人
        self.param_5.place(x=70, y=40)

        # 滚动条
        scroll_bar = Scrollbar(self.open_email_windows)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # 文件内容
        text_info = Text(self.open_email_windows, yscrollcommand=scroll_bar.set, width=100, height=30)
        text_info.place(x=70, y=100)
        for line in text:
            text_info.insert(END, line)

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

        Button(self.open_email_windows, text="退出", command=self.open_email_windows.destroy, width=10).place(x=700, y=550)  # 退出邮箱系统
        self.open_email_windows.mainloop()

    def index_windows(self):
        """主界面"""
        self.index_window = Tk()
        self.index_window.title("index windows")
        self.index_window.resizable(width=True, height=True)
        self.index_window.geometry('900x700')

        # 当前用户信息
        Label(self.index_window, text="User: ").place(x=620, y=5)
        Label(self.index_window, text=self.user).place(x=655, y=5)

        # 滚动条
        scroll_bar = Scrollbar(self.index_window)
        scroll_bar.pack(side=RIGHT, fill=Y)


        # 收件信息窗口
        self.msg_list = Listbox(self.index_window, yscrollcommand=scroll_bar.set, width=110, height=20, font="宋体,15",selectmode=BROWSE)
        self.msg_list.place(x=0, y=30)
        self.msg_list.bind(sequence="<Double-Button-1>", func=self.open_email)

        # 登陆POP服务器 POP.XXX.XXX
        try:
            self.pop3_server = POP3("pop3.wangjunx.top")
            self.pop3_server.user("wud@wangjunx.top")
            self.pop3_server.pass_("949501holdon0.0")
            # self.pop3_server = POP3(self.pop_server)
            # self.pop3_server.user(self.user)
            # self.pop3_server.pass_(self.passwd)
        except Exception as e:
            print "POP CONNECT ERROR ->", str(e)

        rep, self.msg, size = self.pop3_server.list()  # self.msg为全部收信

        # 提示信息
        Label(self.index_window, text="收件箱: " + str(len(self.msg)) + "封", bg="#e6ebe0", font="黑体, 15").place(x=0, y=0)

        all_recv_email = []
        for i in range(1, len(self.msg)+1):
            try:
                rep, text, size = self.pop3_server.retr(i)
                msg_content = b'\r\n'.join(text).decode().encode('utf-8')
                msg = Parser().parsestr(msg_content)
                list = Recv_email().info_digest(msg)
                list.insert(0, str(i)+" : ")
                all_recv_email.append(list)
            except Exception as e:
                # print msg
                print "POP PARSER ERROR ->", str(e)
                pass

        for item in all_recv_email:
            try:
                Id = str(item[0])
                From = 'From: ' + str(item[1])
                To = 'To: ' + str(item[2])
                Subject = 'Subject: ' + item[3]
                parma = Id + From + To + Subject
                self.msg_list.insert(END, parma)
            except Exception as e:
                print parma
                print "ADD RECV ERROR ->", str(e)
        scroll_bar.config(command=self.msg_list.yview)

        # 收件箱按钮
        Button(self.index_window, text="已发送", command=self.delete_msg, width=8). place(x=200, y=0)

        # 删除按钮
        Button(self.index_window, text="删除", command=self.delete_msg, width=8). place(x=0, y=400)

        # 刷新按钮
        Button(self.index_window, text="刷新", command=self.delete_msg, width=8). place(x=90, y=400)

        # 读取按钮
        Button(self.index_window, text="打开", command=self.delete_msg, width=8). place(x=180, y=400)

        # 写信按钮
        Button(self.index_window, text="写信", command=self.send_windows, width=8). place(x=680, y=400)

        # 退出按钮
        Button(self.index_window, text="退出", command=self.sys_quit, width=8). place(x=780, y=400)

        # 邮箱信息验证？
        # 待添加

        # 伪造邮件地址黑名单
        Button(self.index_window, text="添加黑名单", command=self.sys_quit, width=8). place(x=780, y=600)
        # 功能待添加

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
