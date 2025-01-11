import os
import subprocess
import requests
import zipfile
import platform
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext

# ADB工具包的下载URL
ADB_DOWNLOAD_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"

# 指定解压目录
EXTRACT_DIR = os.path.join(os.path.expanduser("~"), "Android", "platform-tools")

class ADBDeployer:
    def __init__(self, master):
        self.master = master
        master.title("ADB一键部署工具（EEBBK BOOM制作）")

        # 创建状态文本框
        self.status_text = scrolledtext.ScrolledText(master, width=60, height=10)
        self.status_text.pack(pady=10)

        # 创建部署按钮
        self.deploy_button = tk.Button(master, text="一键部署ADB", command=self.deploy_adb)
        self.deploy_button.pack(pady=10)

    def log(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)

    def download_file(self, url, destination):
        self.log(f"正在下载ADB工具包：{url}")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.log("下载完成。")
        else:
            self.log(f"下载失败，状态码：{response.status_code}")
            messagebox.showerror("错误", f"下载失败，状态码：{response.status_code}")
            sys.exit(1)

    def extract_zip(self, zip_path, extract_to):
        self.log("正在解压ADB工具包...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        self.log("解压完成。")

    def add_to_path(self, path):
        self.log("正在添加ADB路径到环境变量...")
        if platform.system() == "Windows":
            # 获取当前用户的环境变量
            user_path = os.environ['PATH']
            if path not in user_path:
                # 添加到用户环境变量
                os.environ['PATH'] += os.pathsep + path
                # 永久添加到系统环境变量
                subprocess.run(f'setx PATH "{os.environ["PATH"]}"', shell=True)
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            # 获取当前用户的环境变量
            user_path = os.environ['PATH']
            if path not in user_path:
                # 添加到用户环境变量
                os.environ['PATH'] += os.pathsep + path
                # 永久添加到系统环境变量
                with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
                    bashrc.write(f'\nexport PATH="$PATH:{path}"\n')
        self.log("环境变量添加完成。")

    def deploy_adb(self):
        # 创建解压目录
        os.makedirs(EXTRACT_DIR, exist_ok=True)

        # 下载ADB工具包
        zip_path = os.path.join(EXTRACT_DIR, "platform-tools.zip")
        self.download_file(ADB_DOWNLOAD_URL, zip_path)

        # 解压工具包
        self.extract_zip(zip_path, EXTRACT_DIR)

        # 添加到环境变量
        self.add_to_path(os.path.join(EXTRACT_DIR, "platform-tools"))

        # 清理下载的zip文件
        os.remove(zip_path)
        self.log("清理完成。")

        # 验证安装
        try:
            adb_version = subprocess.check_output("adb version", shell=True, text=True)
            self.log(adb_version.strip())
            messagebox.showinfo("成功", "ADB部署成功！本工具由EEBBK BOOM制作，严禁倒卖")
        except subprocess.CalledProcessError as e:
            self.log(f"验证ADB安装失败：{e}")
            messagebox.showerror("错误", f"验证ADB安装失败：{e}")

def main():
    root = tk.Tk()
    app = ADBDeployer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
