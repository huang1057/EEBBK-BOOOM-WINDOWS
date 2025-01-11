import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct

#注释写的很明白，再看不懂就说不过去了

# 定义BPK和ZIP的文件头
ZIP_HEADERS = {
    b'PK\x01\x02': b'BP\x01',  # Central Directory
    b'PK\x03\x04': b'BP\x03',  # Local File Header
    b'PK\x05\x06': b'BP\x05',  # End of Central Directory Record
    b'PK\x07\x08': b'BP\x07'   # Data Descriptor
}

# 异或加密函数
def xor_encrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# 转换APK到BPK
def convert_apk_to_bpk(apk_path, bpk_path):
    with open(apk_path, 'rb') as apk_file:
        apk_data = apk_file.read()

    # 替换文件头
    for zip_header, bpk_header in ZIP_HEADERS.items():
        apk_data = apk_data.replace(zip_header, bpk_header)

    # 加密EOCD
    eocd_start = apk_data.rfind(b'BP\x05')
    if eocd_start != -1:
        eocd = apk_data[eocd_start:eocd_start + 22]
        xor_code = "END_OF_CENTRAL_DIRECTORY_XOR_CODE_OF_BBK_APK_ENCRYPTION".encode()
        encrypted_eocd = b'BP\x05' + xor_encrypt(eocd[3:], xor_code)
        apk_data = apk_data[:eocd_start] + encrypted_eocd + apk_data[eocd_start + 22:]

    # 加密CD
    cd_start = struct.unpack('<I', apk_data[eocd_start + 16:eocd_start + 20])[0]
    cd_size = struct.unpack('<I', apk_data[eocd_start + 12:eocd_start + 16])[0]
    cd_data = apk_data[cd_start:cd_start + cd_size]
    xor_code = "CENTRAL_DIRECTORY_XOR_CODE_OF_BBK_APK_ENCRYPTION".encode()
    encrypted_cd = xor_encrypt(cd_data, xor_code)
    apk_data = apk_data[:cd_start] + encrypted_cd + apk_data[cd_start + cd_size:]

    # 保存BPK文件
    with open(bpk_path, 'wb') as bpk_file:
        bpk_file.write(apk_data)

    messagebox.showinfo("转换完成", f"BPK文件已保存到：{bpk_path}")

# GUI界面
def create_gui():
    def select_apk():
        apk_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if apk_path:
            bpk_path = os.path.join(os.path.dirname(apk_path), 'bpk', os.path.basename(apk_path).replace('.apk', '.bpk'))
            os.makedirs(os.path.dirname(bpk_path), exist_ok=True)
            convert_apk_to_bpk(apk_path, bpk_path)

    root = tk.Tk()
    root.title("APK to BPK Converter")
    root.geometry("300x150")

    label = tk.Label(root, text="选择APK文件进行转换")
    label.pack(pady=20)

    select_button = tk.Button(root, text="选择APK", command=select_apk)
    select_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
