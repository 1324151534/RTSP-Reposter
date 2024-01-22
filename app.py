from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

class VideoThread(QThread):
    frame_ready = pyqtSignal(QImage)
    video_width = 0
    video_height = 0

    def __init__(self, rtsp_url):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.running = True

    def run(self):
        video_capture = cv2.VideoCapture(self.rtsp_url)
        while self.running:
            ret, frame = video_capture.read()
            if ret:
                frame = self.add_timestamp_to_frame(frame)
                height, width, channel = frame.shape
                self.video_width = width
                self.video_height = height
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(q_image)
                self.msleep(30)  # 30 milliseconds per frame
            else:
                break

        video_capture.release()
    
    # 用于文字边框展示，传入draw,坐标x,y，字体，边框颜色和填充颜色
    def text_border(self, draw, text, x, y, font, shadowcolor, fillcolor, cam_name):

        # thicker border
        draw.text((x - 3, y - 3), text, font=font, fill=shadowcolor)
        draw.text((x + 3, y - 3), text, font=font, fill=shadowcolor)
        draw.text((x - 3, y + 3), text, font=font, fill=shadowcolor)
        draw.text((x + 3, y + 3), text, font=font, fill=shadowcolor)
    
        # now draw the text over it
        draw.text((x - 1, y), text, font=font, fill=fillcolor)
        draw.text((x + 1, y), text, font=font, fill=fillcolor)
        draw.text((x, y + 1), text, font=font, fill=fillcolor)
        draw.text((x, y + 1), text, font=font, fill=fillcolor)

        name_len = len(cam_name.encode('utf-8')) 
        name_x = self.video_width - 52 - 32 * name_len
        name_y = self.video_height - 120

        # thicker border
        draw.text((name_x - 2, name_y - 2), cam_name, font=font, fill=shadowcolor)
        draw.text((name_x + 2, name_y - 2), cam_name, font=font, fill=shadowcolor)
        draw.text((name_x - 2, name_y + 2), cam_name, font=font, fill=shadowcolor)
        draw.text((name_x + 2, name_y + 2), cam_name, font=font, fill=shadowcolor)
        
        draw.text((name_x, name_y), cam_name, font=font, fill=fillcolor)

    def add_timestamp_to_frame(self, frame):
        current_datetime = QDateTime.currentDateTime()
        current_date = current_datetime.toString("yyyy-MM-dd")
        week_day = current_datetime.toString("dddd")  # 获取星期几，中文全名
        current_time = current_datetime.toString("hh:mm:ss")

        full_string = current_date + " " + week_day +  " " + current_time

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        # 使用PIL在图像上绘制时间戳和星期
        font_path = "./UnifontDot.ttf"  # 替换为宋体字体文件的实际路径
        font = ImageFont.truetype(font_path, 65)

        self.text_border(draw, full_string, 30, 30, font, (0, 0, 0), (255, 255, 255), "大门1")

        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        return frame

    def stop(self):
        self.running = False
        self.wait()

class RTSPPlayer(QMainWindow):
    def __init__(self, rtsp_url):
        super().__init__()

        self.rtsp_url = rtsp_url
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.video_label)

        self.video_thread = VideoThread(self.rtsp_url)
        self.video_thread.frame_ready.connect(self.update_frame)
        self.video_thread.start()

    def update_frame(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_thread.stop()
        event.accept()

if __name__ == "__main__":
    rtsp_url = "rtsp://admin:123456@192.168.0.15:554/mpeg4"
    app = QApplication([])
    player = RTSPPlayer(rtsp_url)
    player.setGeometry(100, 100, 800, 600)
    player.setWindowTitle('Python RTSP Player')
    player.show()
    app.exec_()
