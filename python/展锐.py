import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QProcess

class BrushingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('紫光展锐刷机工具')
        self.setGeometry(100, 100, 400, 300)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建按钮
        self.btn_select_sys = QPushButton('选择system.img', self)
        self.btn_select_sys.clicked.connect(self.select_sys_img)
        layout.addWidget(self.btn_select_sys)

        self.btn_select_boot = QPushButton('选择boot.img', self)
        self.btn_select_boot.clicked.connect(self.select_boot_img)
        layout.addWidget(self.btn_select_boot)

        self.btn_brush = QPushButton('开始刷机', self)
        self.btn_brush.clicked.connect(self.start_brushing)
        layout.addWidget(self.btn_brush)

        self.btn_unlock_bl = QPushButton('解除BL锁', self)
        self.btn_unlock_bl.clicked.connect(self.unlock_bl)
        layout.addWidget(self.btn_unlock_bl)

        # 设置中心窗口的布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化变量
        self.sys_img_path = ''
        self.boot_img_path = ''

    def select_sys_img(self):
        # 选择system.img文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择system.img", "img/", "Image Files (*.img)", options=options)
        if file_name:
            self.sys_img_path = file_name

    def select_boot_img(self):
        # 选择boot.img文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择boot.img", "img/", "Image Files (*.img)", options=options)
        if file_name:
            self.boot_img_path = file_name

    def start_brushing(self):
        # 开始刷机
        if not self.sys_img_path or not self.boot_img_path:
            QMessageBox.warning(self, '警告', '请先选择system.img和boot.img文件！')
            return

        # 重启设备到Fastboot模式
        self.run_command('adb reboot bootloader')

        # 刷入system.img
        self.run_command(f'fastboot flash system {self.sys_img_path}')

        # 刷入boot.img
        self.run_command(f'fastboot flash boot {self.boot_img_path}')

        # 重启设备
        self.run_command('fastboot reboot')

        QMessageBox.information(self, '提示', '刷机完成！')

    def unlock_bl(self):
        # 解除BL锁
        # 使用SPD_DUMP工具进入9008模式
        self.run_command('adb reboot edl')

        # 使用SPD_DUMP工具进行操作
        # 以下命令需要根据SPD_DUMP工具的具体使用方法进行调整
        self.run_command('spd_dump -c 9008 -f unlock_bl.bin')

        QMessageBox.information(self, '提示', 'BL锁解除完成！')

    def run_command(self, command):
        # 运行命令
        process = QProcess(self)
        process.start(command)
        process.waitForFinished()
        output = process.readAllStandardOutput().data().decode('utf-8')
        error = process.readAllStandardError().data().decode('utf-8')
        if error:
            QMessageBox.warning(self, '错误', f'命令执行失败：{error}')
        else:
            print(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BrushingTool()
    ex.show()
    sys.exit(app.exec_())
