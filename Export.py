__author__ = 'wwxiang'

#coding=utf-8

import tkinter
import tkinter.messagebox
import tkinter.filedialog
import os
import re

work = os.getcwd()
workxml = work + os.path.sep + 'res.xml'

class GuiApp:
    def __init__(self,width=320,height=100):
        self.root = tkinter.Tk()
        self.root.geometry('{0}x{1}'.format(width,height))
        self.root.title('导出RES文件')
        self.fileData = None
        pass
    def cre_gui(self):
        lab = tkinter.Label(self.root,text='提取README.md并导出res.xml文件')
        lab.pack(padx=5,pady=5,anchor='w')
        self.export = tkinter.Button(self.root,text='Export')
        self.export.pack(padx=5,pady=5,anchor='w')
        self.export.bind('<Button-1>',self.handler)
        pass
    def handler(self,event):
        filename = tkinter.filedialog.askopenfilename()
        if not len(filename):
            tkinter.messagebox.showerror('错误','未选择文件')
            self.export.option_clear()
            return
        isblock = True
        handlerData = []
        lineNo = 0
        try:
            with open(filename,'rb') as linefs:
                lineCout = len(linefs.readlines())
                linefs.close()
            with open(filename,'rb') as fs:
                while isblock:
                    lineNo += 1
                    val = fs.readline().decode()
                    if lineNo == lineCout:
                        isblock = False
                    if not val[0] == '[':
                        continue
                    title = re.findall(r'\[(.+?)\]',val)[0]
                    xmlUrl = re.findall(r'<(.+?)>',val)[0]
                    htmlUrl = re.findall(r'\((.+?)\)',val)[0]
                    handlerData.append('<outline text="{0}" title="{0}" type="rss" xmlUrl="{1}" htmlUrl="{2}"/>'.format(title,xmlUrl,htmlUrl))
                fs.close()
        except:
            tkinter.messagebox.showerror('错误处理','读取文件失败')
            self.export.option_clear()
            return
        export_xml = '<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head><title>导出订阅</title></head><body>\n'
        export_xml += '\r\n'.join(handlerData)
        export_xml += '</body></opml>'
        with open(workxml,'wb') as fs:
            fs.write(export_xml.encode())
            fs.close()
        tkinter.messagebox.showinfo('成功','处理完成')
        self.export.option_clear()
        pass
    def loop(self):
        self.root.resizable(False,False)
        self.cre_gui()
        self.root.mainloop()
        pass
    pass
app = GuiApp()
app.loop()