from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtCore import QDateTime
import cv2
import numpy as np

class VideoProcessor:
    video_width = 1920
    video_height = 1080
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


    def add_timestamp_to_frame(self, frame, cam_name, time_color, videoX, videoY):

        self.video_width = int(videoX)
        self.video_height = int(videoY)

        current_datetime = QDateTime.currentDateTime()
        current_date = current_datetime.toString("yyyy-MM-dd")
        week_day = current_datetime.toString("dddd")  # 获取星期几，中文全名
        current_time = current_datetime.toString("hh:mm:ss")

        full_string = current_date + " " + week_day + " " + current_time

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)

        # 使用PIL在图像上绘制时间戳和星期
        font_path = "./UnifontDot.ttf"  # 替换为宋体字体文件的实际路径
        font = ImageFont.truetype(font_path, 65)

        fillcolor = (255, 255, 255)
        color_enum = {
            "red" : (0, 0, 255),
            "green" : (0, 255, 0),
            "blue" : (255, 0, 0)
        }
        fillcolor = color_enum.get(time_color, (255, 255, 255))

        self.text_border(draw, full_string, 30, 30, font, (0, 0, 0), fillcolor, cam_name)

        # frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2YUV)
        frame = np.array(pil_image)

        return frame
