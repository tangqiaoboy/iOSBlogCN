__author__ = 'wwxiang'

#coding=utf-8

import os
import re

work = os.getcwd()
resxml = work + os.path.sep + 'blogcn.opml'
workmd = work + os.path.sep + 'README.md'

def handler():
    isblock = True
    handlerData = []
    lineNo = 0
    try:
        with open(workmd,'rb') as linefs:
            lineCout = len(linefs.readlines())
            linefs.close()
        with open(workmd,'rb') as fs:
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
        print('错误处理','读取文件失败')
        return
    export_xml = '<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head><title>导出订阅</title></head><body><outline text="ios" title="ios" >\n'
    export_xml += '\r\n'.join(handlerData)
    export_xml += '</outline></body></opml>\r\n'
    with open(resxml,'wb') as fs:
        fs.write(export_xml.encode())
        fs.close()
    print('res.xml文件处理完成')
    pass
if os.path.isfile(workmd):
    handler()

