import tkinter as tk
from tkinter import messagebox
import os
import subprocess

def open_exe():
    try:
        # 替换为你的.exe文件的完整路径
        exe_path = r'C:\example\app.exe'
        subprocess.run(exe_path, check=True)
    except Exception as e:
        messagebox.showerror("错误", f"无法打开文件: {e}")

def create_gui():
    root = tk.Tk()
    root.title("免责声明")

    disclaimer = tk.Text(root, height=15, width=50)
    disclaimer.insert(tk.END, """### 免责声明

### 关于步步高学习机解除第三方软件安装限制免责声明

协议更新日期:2024年6月16日

1. 所有已经解除第三方软件安装限制的学习机都可以恢复到解除限制前之状态。

2. 解除第三方软件安装限制后，学习机可以自由安装第三方软件，需要家长加强对孩子的监管力度，避免孩子沉迷网络、影响学习;学习机自带的学习功能不受影响。

3. 您对学习机进行解除第三方软件安装限制之操作属于您的自愿行为，若在操作过程中由于操作不当等自身原因，导致出现学习机无法正常使用等异常情况，以及解除软件安装限制之后产生的一切后果将由您本人承担!

4. 如果您使用本工具对学习机进行解除第三方软件安装限制之操作，即默认您同意本《免责声明》。""")

    disclaimer.pack(pady=20)

    agree_button = tk.Button(root, text="同意", command=open_exe)
    agree_button.pack(side=tk.LEFT, padx=(20, 10))

    disagree_button = tk.Button(root, text="拒绝", command=root.quit)
    disagree_button.pack(side=tk.RIGHT, padx=(10, 20))

    root.mainloop()

if __name__ == "__main__":
    create_gui()
