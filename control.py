import sys
import json
import psutil
import subprocess
import time
import os
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from mainui import Ui_RTSPReposter
from settingsui import Ui_Form 

class AddItemDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddItemDialog, self).__init__(parent)
        self.setWindowTitle("添加新转发")
        self.resize(500, 400)
        # self.setGeometry(200, 200, 300, 200)

        self.name_edit = QtWidgets.QLineEdit(self)
        self.channel_edit = QtWidgets.QLineEdit(self)
        self.status_edit = QtWidgets.QLineEdit(self)
        self.rtsp_addr_edit = QtWidgets.QLineEdit(self)
        self.rtsp_post_addr_edit = QtWidgets.QLineEdit(self)
        self.local_file_edit = QtWidgets.QLineEdit(self)
        self.show_time_edit = QtWidgets.QLineEdit(self)
        self.time_color_edit = QtWidgets.QLineEdit(self)
        self.desc_edit = QtWidgets.QLineEdit(self)
        self.active_edit = QtWidgets.QLineEdit(self)

        self.ok_button = QtWidgets.QPushButton("确定", self)
        self.cancel_button = QtWidgets.QPushButton("取消", self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("摄像头名:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QtWidgets.QLabel("通道:"))
        layout.addWidget(self.channel_edit)
        layout.addWidget(QtWidgets.QLabel("状态:"))
        layout.addWidget(self.status_edit)
        layout.addWidget(QtWidgets.QLabel("接收流地址:"))
        layout.addWidget(self.rtsp_addr_edit)
        layout.addWidget(QtWidgets.QLabel("转发流地址:"))
        layout.addWidget(self.rtsp_post_addr_edit)
        layout.addWidget(QtWidgets.QLabel("本地文件地址:"))
        layout.addWidget(self.local_file_edit)
        layout.addWidget(QtWidgets.QLabel("显示时间戳:"))
        layout.addWidget(self.show_time_edit)
        layout.addWidget(QtWidgets.QLabel("时间戳颜色:"))
        layout.addWidget(self.time_color_edit)
        layout.addWidget(QtWidgets.QLabel("描述:"))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QtWidgets.QLabel("是否启用:"))
        layout.addWidget(self.active_edit)
        
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "channel": self.channel_edit.text(),
            "status": self.status_edit.text(),
            "rtsp_addr": self.rtsp_addr_edit.text(),
            "rtsp_post_addr": self.rtsp_post_addr_edit.text(),
            "local_file" : self.local_file_edit.text(),
            "show_time": self.show_time_edit.text(),
            "time_color": self.time_color_edit.text(),
            "desc": self.desc_edit.text(),
            "activate": self.active_edit.text()
        }

class SettingsDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.load_settings_data('control_config.json')

        self.cudaacc.stateChanged.connect(self.update_json_data)
        self.gpuacc.stateChanged.connect(self.update_json_data)
        self.hardware_decoding_options.currentTextChanged.connect(self.update_json_data)

    def load_settings_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                # cuda_enabled = data.get("cuda", 0)
                gpu_enabled = data.get("use_gpu", 1)
                if not gpu_enabled:
                    self.hardware_decoding_options.hide()

                # self.cudaacc.setChecked(cuda_enabled)
                self.gpuacc.setChecked(gpu_enabled)

                self.version = data.get("version", "获取失败")
                self.label.setText(f"RTSP Reposter | 版本号：{self.version}")

                hardware_decoding_option = data.get("hardware_decoding_option", "")
                if hardware_decoding_option in ["QSV 编码（Intel核显）", "NVENC 编码（NVIDIA显卡）", "AMF 编码（AMD显卡）"]:
                    self.hardware_decoding_options.setCurrentText(hardware_decoding_option)

        except FileNotFoundError:
            print(f"File {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}.")
    
    def update_json_data(self):
        json_data = {
            "version": self.version,
            "cuda": 0,
            # "cuda": int(self.cudaacc.isChecked()),
            "use_gpu": int(self.gpuacc.isChecked()),
            "hardware_decoding_option": self.hardware_decoding_options.currentText()
        }

        with open('control_config.json', 'w') as file:
            json.dump(json_data, file, indent=2)

        if self.gpuacc.isChecked():
            self.hardware_decoding_options.show()
        else:
            self.hardware_decoding_options.hide()

class MainApplication(QtWidgets.QMainWindow, Ui_RTSPReposter):
    json_data = {}
    bNotAdd = True
    process = None

    def __init__(self):
        super(MainApplication, self).__init__()
        self.setupUi(self)
        self.load_json_data('config.json')
        # self.tableWidget.itemDoubleClicked.connect(self.editItem)
        self.Add.clicked.connect(self.add_item)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.tableWidget.itemChanged.connect(self.on_item_changed)
        self.Delete.clicked.connect(self.delete_item)
        self.Switch.clicked.connect(self.switch_status)
        self.Start.clicked.connect(self.toggle_repost_service)
        self.sort_data()

        self.settings_dialog = SettingsDialog(self)
        self.main.triggered.connect(self.open_settings)

        subprocess.Popen("mediamtx.exe")

    def open_settings(self):
        self.settings_dialog.show()

    def toggle_repost_service(self):
        if self.process and self.process.poll() is None:
            self.stop_repost_service()
        else:
            self.start_repost_service()

    def start_repost_service(self):
        self.process = subprocess.Popen(["python", "start_repost.py"])

        self.Start.setText("停止转发服务")

    def stop_repost_service(self):
        if self.process and self.process.poll() is None:

            self.terminate_all_subprocesses()

            self.Start.setText("启动转发服务")

    def terminate_all_subprocesses(self):
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass

    def add_item(self):
        self.bNotAdd = False
        dialog = AddItemDialog(self)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            new_data = dialog.get_data()

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            for col, value in enumerate(new_data.values()):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_position, col, item)

            json_key = str(row_position)
            self.json_data[json_key] = new_data

            self.save_json_data('config.json')
        self.bNotAdd = True

    def on_item_clicked(self, item):
        pass
        # row = item.row()
        # self.tableWidget.selectRow(row)

    def on_item_changed(self, item: QTableWidgetItem):
        if self.bNotAdd:
            new_value = item.text()

            row = item.row()
            col = item.column()

            enu_col = {
                0: "name",
                1: "channel",
                2: "status",
                3: "rtsp_addr",
                4: "rtsp_post_addr",
                5: "local_file",
                6: "show_time",
                7: "time_color",
                8: "desc",
                9: "activate"
            }

            json_key = str(row)
            data_index = enu_col[col]
            self.json_data[json_key][data_index] = new_value
            self.save_json_data('config.json')

    def delete_item(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self, "提示", "请选择要删除的行")
            return

        selected_rows = set(index.row() for index in selected_indexes)

        for row in sorted(selected_rows):
            self.tableWidget.removeRow(row)
            json_key = str(row)
            if json_key in self.json_data:
                del self.json_data[json_key]
        
        self.sort_data()
        
        self.save_json_data('config.json')

        self.clickedItem = None

    def sort_data(self):
        flag = -1
        temp_data_dic = self.json_data.copy()
        for data in temp_data_dic:
            if data == str(flag + 1):
                flag += 1
            else:
                flag += 1
                new_key = flag
                self.json_data[new_key] = self.json_data[data]
                del self.json_data[data]
        self.save_json_data('config.json')
        self.tableWidget.setRowCount(0)
        self.load_json_data('config.json')

    def load_json_data(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.json_data = data

        for key, values in data.items():
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

            for col, value in enumerate(values.values()):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowPosition, col, item)
    
    def editItem(self, item):
        row = item.row()
        col = item.column()
        enu_col = {
            "摄像头名" : "name",
            "状态" : "status",
            "通道" : "channel",
            "接收流地址" : "rtsp_addr",
            "转发流地址" : "rtsp_post_addr",
            "本地文件地址" : "local_file",
            "显示时间戳" : "show_time",
            "时间戳颜色" : "time_color",
            "描述" : "desc",
            "是否启用" : "activate"
        }

        new_value, ok = QtWidgets.QInputDialog.getText(
            self.tableWidget, "编辑", f"输入新的{self.tableWidget.horizontalHeaderItem(col).text()}:", QtWidgets.QLineEdit.Normal, item.text())

        if ok:
            item.setText(new_value)

            json_key = str(row)
            data_index = enu_col[self.tableWidget.horizontalHeaderItem(col).text()]
            
            self.json_data[json_key][data_index] = new_value

            self.save_json_data('config.json')

    def save_json_data(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.json_data, file, indent=2)

    def switch_status(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self, "提示", "请选择要删除的行")
            return

        selected_rows = set(index.row() for index in selected_indexes)
        
        self.stop_repost_service()

        for row in selected_rows:
            json_key = str(row)
            if json_key in self.json_data:
                current_status = self.json_data[json_key].get("status", "")
                new_status = "网络" if current_status == "本地" else "本地"
                self.json_data[json_key]["status"] = new_status
                
                item = self.tableWidget.item(row, 2)
                item.setText(new_status)

        self.save_json_data('config.json')

        time.sleep(0.5)
        self.start_repost_service()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
