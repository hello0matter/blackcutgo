import frida, sys

jsCode = """"""""
with open('sohook.js', 'r', encoding='utf-8') as file:
    content = file.read()
    jsCode = content

# process = frida.get_device_manager().add_remote_device('192.168.3.68:8888').attach('com.dodonew.online')
device = frida.get_usb_device()
pid = device.spawn(["com.example.hellojni_sign2"])    # 以挂起方式创建进程
process = device.attach(pid)
# process = device.attach('com.example.hellojni_sign2')
script = process.create_script(jsCode)
script.load()
device.resume(pid)  # 加载完脚本, 恢复进程运行
sys.stdin.read()