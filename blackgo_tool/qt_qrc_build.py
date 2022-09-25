import subprocess, os

# images = os.listdir('./icons')
qss = os.listdir('./obj')
f = open('obj.qrc', 'w+')
f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource>\n')
#
# for item in images:
#     f.write(u'<file alias="icons/'+ item +'">icons/'+ item +'</file>\n')

for item in qss:
    f.write(u'<file alias="obj/'+ item +'">obj/'+ item +'</file>\n')

f.write(u'</qresource>\n</RCC>')
f.close()

pipe = subprocess.Popen(r'pyside6-rcc -o rc_obj.py obj.qrc', stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, creationflags=0x08)