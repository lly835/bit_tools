#excel拖拽后设置密码
#如果要打包成可执行文件，需把hook-tkinterdnd2.py和excel_encry.py2个文件放在一个目录下，然后执行
#pyinstaller -F -w excel_encry.py --additional-hooks-dir=.
# 再python3.9环境运行通过

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import msoffcrypto
import os

def set_password(file_path, password):
    with open(file_path, "rb") as file:
        # 创建一个MS Office文档加密对象
        office_file = msoffcrypto.OfficeFile(file)

        # 设置要使用的密码
        office_file.load_key(password=password)

        # 写入加密的Excel文件
        base_name, extension = os.path.splitext(file_path)
        with open(f"{base_name}_encrypted{extension}", "wb") as encrypted_file:
            office_file.encrypt(password, encrypted_file)

def drop(event):
    # 获取拖入的文件路径
    file_path = event.data
    # 在Text部件中显示文件名
    text_area.delete(1.0, tk.END)  # 清空内容
    text_area.insert(tk.END, file_path)

    set_password(file_path, password)


# 创建主窗口
password = 'nGuCtGh#r5R&8G'
root = TkinterDnD.Tk()
root.title("excel拖进来自动设置密码")
root.geometry("400x300")

# 创建一个文本区域用于显示文件路径
text_area = tk.Text(root, height=10, width=50)
text_area.pack(pady=10)

# 创建拖入区域
drop_area = tk.Label(root, text="将文件拖入这里", relief="groove", width=40, height=10)
drop_area.pack(pady=10)

# 绑定拖放事件
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)

# 启动主循环
root.mainloop()
