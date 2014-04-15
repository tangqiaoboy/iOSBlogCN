__author__ = 'wwxiang'

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
        lab = tkinter.Label(self.root,text='从README.md文件中分析出适合的RES文件，并导出。')
        lab.pack(padx=5,pady=5,anchor='w')
        self.export = tkinter.Button(self.root,text='Export')
        self.export.pack(padx=5,pady=5,anchor='w')
        self.export.bind('<Button-1>',self.handler)
        pass
    def handler(self,event):
        filename = tkinter.filedialog.askopenfilename()
        isblock = True
        handlerData = []
        lineNo = 0
        '''
            逻辑，逐行读取，忽略回车，空格。

            如果第一个字符不是[则忽略，如果是则这一条数据，分解为三个键值对，为title，url，resURL

            一个字典，加入一个列表

            最后一行停止循环，锁上。
        '''
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
                    '''
                        正则匹配()[]<>中的值，构建xml

                        结构如下：
                        <outline text="" title="" type="rss" xmlUrl="" htmlUrl=""/>

                    '''
                    title = re.findall(r'\[(.+?)\]',val)[0]
                    xmlUrl = re.findall(r'<(.+?)>',val)[0]
                    htmlUrl = re.findall(r'\((.+?)\)',val)[0]
                    handlerData.append('<outline text="{0}" title="{0}" type="rss" xmlUrl="{1}" htmlUrl="{2}"/>'.format(title,xmlUrl,htmlUrl))
                fs.close()
        except:
            tkinter.messagebox.showerror('错误处理','读取文件失败')
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