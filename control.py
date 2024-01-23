import sys
import json
import psutil
import subprocess
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from mainui import Ui_RTSPReposter

class AddItemDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddItemDialog, self).__init__(parent)
        self.setWindowTitle("添加新转发")
        self.resize(500, 400)
        # self.setGeometry(200, 200, 300, 200)

        # 创建文本框
        self.name_edit = QtWidgets.QLineEdit(self)
        self.channel_edit = QtWidgets.QLineEdit(self)
        self.status_edit = QtWidgets.QLineEdit(self)
        self.rtsp_addr_edit = QtWidgets.QLineEdit(self)
        self.rtsp_post_addr_edit = QtWidgets.QLineEdit(self)
        self.local_file_edit = QtWidgets.QLineEdit(self)
        self.show_time_edit = QtWidgets.QLineEdit(self)
        self.time_color_edit = QtWidgets.QLineEdit(self)
        self.desc_edit = QtWidgets.QLineEdit(self)

        # 创建确定和取消按钮
        self.ok_button = QtWidgets.QPushButton("确定", self)
        self.cancel_button = QtWidgets.QPushButton("取消", self)

        # 将文本框和按钮添加到布局中
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
        layout.addWidget(self.local_file_edit)
        layout.addWidget(QtWidgets.QLabel("本地文件地址:"))
        layout.addWidget(self.rtsp_post_addr_edit)
        layout.addWidget(QtWidgets.QLabel("显示时间戳:"))
        layout.addWidget(self.show_time_edit)
        layout.addWidget(QtWidgets.QLabel("时间戳颜色:"))
        layout.addWidget(self.time_color_edit)
        layout.addWidget(QtWidgets.QLabel("描述:"))
        layout.addWidget(self.desc_edit)
        
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        # 连接按钮的点击事件到相应的槽函数
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        # 返回用户填写的数据
        return {
            "name": self.name_edit.text(),
            "channel": self.channel_edit.text(),
            "status": self.status_edit.text(),
            "rtsp_addr": self.rtsp_addr_edit.text(),
            "rtsp_post_addr": self.rtsp_post_addr_edit.text(),
            "local_file" : self.local_file_edit.text(),
            "show_time": self.show_time_edit.text(),
            "time_color": self.time_color_edit.text(),
            "desc": self.desc_edit.text()
        }


class MainApplication(QtWidgets.QMainWindow, Ui_RTSPReposter):
    json_data = {}
    bNotAdd = True
    process = None  # 用于存储 start_repost.py 进程对象

    def __init__(self):
        super(MainApplication, self).__init__()
        self.setupUi(self)
        self.load_json_data('config.json')  # 配置文件
        # self.tableWidget.itemDoubleClicked.connect(self.editItem)
        self.Add.clicked.connect(self.add_item)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.tableWidget.itemChanged.connect(self.on_item_changed)
        self.Delete.clicked.connect(self.delete_item)
        self.Switch.clicked.connect(self.switch_status)
        self.Start.clicked.connect(self.toggle_repost_service)
        self.sort_data()

    def toggle_repost_service(self):
        if self.process and self.process.poll() is None:
            # 如果进程存在且尚未结束，说明服务正在运行，需要停止服务
            self.stop_repost_service()
        else:
            # 否则，启动服务
            self.start_repost_service()

    def start_repost_service(self):
        # 启动 start_repost.py 进程
        self.process = subprocess.Popen(["python", "start_repost.py"])

        # 更新按钮文本
        self.Start.setText("停止转发服务")

    def stop_repost_service(self):
        # 检查进程是否存在再尝试写入 stdin
        if self.process and self.process.poll() is None:

            # 递归停止所有子进程
            self.terminate_all_subprocesses()

            # 更新按钮文本
            self.Start.setText("启动转发服务")

    def terminate_all_subprocesses(self):
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                # 如果子进程已经退出，跳过
                pass

    def add_item(self):
        self.bNotAdd = False
        # 创建并显示添加项对话框
        dialog = AddItemDialog(self)
        result = dialog.exec_()

        # 如果用户点击了确定按钮，将新项添加到表格和 JSON 中
        if result == QtWidgets.QDialog.Accepted:
            new_data = dialog.get_data()

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            for col, value in enumerate(new_data.values()):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_position, col, item)

            json_key = str(row_position)
            self.json_data[json_key] = new_data

            # 保存更新后的 JSON 到文件
            self.save_json_data('config.json')
        self.bNotAdd = True

    def on_item_clicked(self, item):
        # 当某一行的任意一列被点击时，选中整行
        row = item.row()
        self.tableWidget.selectRow(row)

    def on_item_changed(self, item: QTableWidgetItem):
        if self.bNotAdd:
            # 获取修改后的值
            new_value = item.text()

            # 获取行和列的索引
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
                8: "desc"
            }

            # 获取 JSON 中的键
            json_key = str(row)

            # 获取对应的 JSON 键名
            data_index = enu_col[col]

            # 更新 JSON 数据
            self.json_data[json_key][data_index] = new_value

            # 保存更新后的 JSON 到文件
            self.save_json_data('config.json')

    def delete_item(self):
        selected_rows = set(index.row() for index in self.tableWidget.selectionModel().selectedRows())
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "提示", "请选择要删除的行")
            return

        # 从表格中删除选中的行
        for row in sorted(selected_rows):
            self.tableWidget.removeRow(row)
            json_key = str(row)
            print(self.json_data)
            print( "DEBUG " + json_key)
            if json_key in self.json_data:
                del self.json_data[json_key]
        
        self.sort_data()
        
        # 保存更新后的 JSON 到文件
        self.save_json_data('config.json')

    def sort_data(self):
        flag = -1
        temp_data_dic = self.json_data.copy()
        for data in temp_data_dic:
            print(data)
            if data == str(flag + 1):
                flag += 1
            else:
                print("CHECK " + str(data) + " | " + str(flag))
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
            "描述" : "desc"
        }

        # Prompt the user for a new value
        new_value, ok = QtWidgets.QInputDialog.getText(
            self.tableWidget, "编辑", f"输入新的{self.tableWidget.horizontalHeaderItem(col).text()}:", QtWidgets.QLineEdit.Normal, item.text())

        if ok:
            # Update the table
            item.setText(new_value)

            # Update the JSON data

            json_key = str(row)
            data_index = enu_col[self.tableWidget.horizontalHeaderItem(col).text()]
            
            print("DEBUG: " + data_index + " | " + json_key)
            self.json_data[json_key][data_index] = new_value

            # Save the updated JSON to the file
            self.save_json_data('config.json')  # Replace with your JSON file path

    def save_json_data(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.json_data, file, indent=2)

    def switch_status(self):
        selected_rows = set(index.row() for index in self.tableWidget.selectionModel().selectedRows())
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "提示", "请选择要切换状态的行")
            return

        # 切换选中行的状态
        for row in selected_rows:
            json_key = str(row)
            if json_key in self.json_data:
                current_status = self.json_data[json_key].get("status", "")
                new_status = "网络" if current_status == "本地" else "本地"
                self.json_data[json_key]["status"] = new_status
                
                # 更新表格中的显示
                item = self.tableWidget.item(row, 2)
                item.setText(new_status)

        # 保存更新后的 JSON 到文件
        self.save_json_data('config.json')

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
