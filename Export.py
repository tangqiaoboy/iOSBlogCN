__author__ = 'wwxiang'

import tkinter
import tkinter.messagebox
import tkinter.filedialog
import os
import xml

work = os.getcwd()

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
        export = tkinter.Button(self.root,text='Export')
        export.pack(padx=5,pady=5,anchor='w')
        export.bind('<Button-1>',self.handler)
        pass
    def handler(self,event):
        filename = tkinter.filedialog.askopenfilename()
        try:
            with open(filename,'rb') as fs:
                self.fileData = fs.read().decode().replace('\r\n','')
                fs.close()
        except:
            tkinter.messagebox.showerror('错误处理','读取文件失败')
        print(self.fileData)
        pass
    def loop(self):
        self.root.resizable(False,False)
        self.cre_gui()
        self.root.mainloop()
        pass
    pass
app = GuiApp()
app.loop()