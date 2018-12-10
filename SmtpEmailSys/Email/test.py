# encoding:utf-8

from tkinter import *
'''
Listbox组件根据selectmode选项提供了四种不同的选择模式：SINGLE(单选）
BROWSE（也是单选，但推动鼠标或通过方向键可以直接改变选项）
MULTIPLE（多选）和EXTENDED（也是多选，但需要同时按住Shift和Ctrl或拖动鼠标实现
），默认是BROWSE
'''
root = Tk()
theLB = Listbox(root,selectmode=MULTIPLE,height=11)#height=11设置listbox组件的高度，默认是10行。
theLB.pack()
for item in['公鸡','母鸡','小鸡','火鸡','战斗机',]:
    theLB.insert(END,item)  #END表示每插入一个都是在最后一个位置
theButton = Button(root, text='删除',\
                   command=lambda x=theLB:x.delete(ACTIVE))
theButton.pack()
mainloop()