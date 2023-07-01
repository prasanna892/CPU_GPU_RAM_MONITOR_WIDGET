# importing required module
import traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from screeninfo import get_monitors
import psutil
from psutil._common import bytes2human
from collections import Counter
import math
import json
import os
from pathlib import Path
import winreg as reg	
import sys
from time import sleep
from datetime import date

# Creating SysInfo class
class SysInfo(QWidget):
    def __init__(self, parent = None):
        super(SysInfo, self).__init__(parent)

        # reading property.json for getting GUI last x_pos & y_pos
        with open('./assets/property.json', 'r') as file:
            self.data = json.load(file)
            file.close()

        # Setting window to frameless and transparent
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.88) # window opacity
        # screen width and height
        self.screen_width = 320 
        self.screen_height = 320
        # screen x&y position
        self.pos_x = self.data['position']["x_pos"]
        self.pos_y = self.data['position']["y_pos"]
        
        # setting screen geomentry
        self.setGeometry(self.pos_x, self.pos_y, self.screen_width, self.screen_height)
	self.setFixedSize(self.screen_width, self.screen_height)

        # getting GPU present info from result.json
        with open('./assets/TempINFO/result.json') as self.result_file:
            TempINFOdata = json.load(self.result_file)
            self.result_file.close()
        self.gpu = True if TempINFOdata["GPU"]["Name"].get("Name") != 'GPU Not Found' else False

        # creating required variable
        self.label1_pos = 60
        self.radius = 10
        self.mouse_doubleClicked = False
        self.pos_ = self.label1_pos
        self.txt_cal_flag = True
        self.text_dict = {
            'CPU_Utilized': {
                'text_rect': None,
                'circumference': None,
                'painter_path': None,
                'fm': None,
                'pts': None,
                'ang': None
            },
            'GPU_Utilized': {
                'text_rect': None,
                'circumference': None,
                'painter_path': None,
                'fm': None,
                'pts': None,
                'ang': None
            },
            'CPU_Temp': {
                'text_rect': None,
                'circumference': None,
                'painter_path': None,
                'fm': None,
                'pts': None,
                'ang': None
            },
            'GPU_Temp': {
                'text_rect': None,
                'circumference': None,
                'painter_path': None,
                'fm': None,
                'pts': None,
                'ang': None
            },
            'RAM_Used': {
                'text_rect': None,
                'circumference': None,
                'painter_path': None,
                'fm': None,
                'pts': None,
                'ang': None
            }
        }

        # pointers initial location
        self.cpu_utilized_pointer_if_gpu_present = 0.112
        self.cpu_temp_pointer_if_gpu_present = 0.114
        self.gpu_utilized_pointer = 0.610
        self.gpu_temp_pointer = 0.616
        self.cpu_utilized_pointer_if_gpu_absent = 0.866
        self.cpu_temp_pointer_if_gpu_absent = 0.884
        self.ram_utilized_pointer = 0.950

        # creating timer to update info
        self.info_timer = QTimer()
        self.info_timer.timeout.connect(self.show_info)

        self.pointer_timer = QTimer()
        self.pointer_timer.timeout.connect(self.pointer_update)
        self.pointer_timer.start(1000)

        self.label() # calling label method

        self.animate_circle() # calling cirle animation method

        # checking window close operation and setting it to closeEvent()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    # creating info label
    def label(self):
        # creating widget to contain system info label
        self.widget1 = QWidget(self)
        self.widget1.setGeometry((self.width()-24)//2, (self.height()-24)//2, 24, 24)
        
        # label to show system info
        self.label1 = QLabel("", self.widget1)
        self.label1.setAlignment(Qt.AlignHCenter)
        self.label1.setGeometry((self.width()-24)//2, (self.height()-24)//2, 24, 24)

        # empty roung label for design
        self.round = QLabel("", self)
        self.round.setGeometry((self.width()-310)//2, (self.height()-310)//2, 310, 310)
        self.round.setStyleSheet("border-radius: 155px; background-color: rgba(0, 0, 0, 0); border: 4px solid cyan")

    # method for drawing circle on background of circular text
    def draw_circle_around_txt(self, qfont, txt, circle_colour, qpoint, radius):
        # creating painter and setting rendering hints
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # getting font bounding rectangle and calling draw circle function
        fm = QFontMetrics(qfont)
        txt_rect = fm.boundingRect(txt)
        height = txt_rect.height()

        painter.setPen(QPen(circle_colour, height))
        painter.drawEllipse(qpoint, radius, radius)

        # closing painter
        painter.end()

        return height

    # drawing arc to indicate system condition
    def draw_arc(self, width, radius, start_angle, end_angle, gradient_start_angle, color1=Qt.red, color2=Qt.yellow, color3=Qt.green, color1_set=0.0, color2_set=0.2, color3_set=0.4):

        # creating painter and setting render hint
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        conicalGradient = QConicalGradient(QPointF(self.width()/2, self.width()/2), gradient_start_angle)
        conicalGradient.setColorAt(color1_set, color1)
        conicalGradient.setColorAt(color2_set, color2)
        conicalGradient.setColorAt(color3_set, color3)
        
        painter.setPen(QPen(conicalGradient, width))
        painter.drawArc(QRectF(self.width()/2-radius, self.width()/2-radius, radius*2, radius*2), start_angle * 16, end_angle * 16)

        painter.end()
         
    # method to calculate circumference, text bounding box dimension, text path and font matrix
    def txt_bounding_box(self, radius, qfont, qpoint, txt):
        # getting circumference of circle and font matrix
        circumference = 2 * math.pi * radius
        fm = QFontMetrics(qfont)

        # creating painter path and setting circlular path to painter path
        painter_path = QPainterPath()
        painter_path.addEllipse(qpoint, radius, radius)

        # getting font bounding rectangle and calling draw circle function
        text_rect = fm.boundingRect(txt)

        return [text_rect, circumference, painter_path, fm]

    # method to calculate text path all points and angle at all points
    def txt_path_all_points(self, text_rect, circumference, painter_path, txt, char_space, txt_position):
        # getting circular path all point and angle at that point
        # appending geted points and angle in pts and ang list
        pts = []
        ang = []
        cir_per = 0
        cir_per_inc = 1/circumference
        center = 0
        for i in range(0, int(circumference)):
            if cir_per + cir_per_inc < 1:
                cir_per += cir_per_inc
            pts.append(painter_path.pointAtPercent(cir_per))
            if int(painter_path.pointAtPercent(cir_per).x()) == self.width()//2:
                center = i
            ang.append(painter_path.angleAtPercent(cir_per))
        pts.append(painter_path.pointAtPercent(0.999999))
        ang.append(painter_path.angleAtPercent(0.999999))

        center = abs(center-(text_rect.width()+((len(txt)+1)*char_space))//2)
        pts = pts[center:] + pts[:center]
        ang = ang[center:] + ang[:center]

        pts = pts[txt_position:] + pts[:txt_position]
        ang = ang[txt_position:] + ang[:txt_position]

        return [pts, ang]

    # method for rendring circular text on screen
    def render_txt(self, qpoint, radius, txt, qfont, txt_colour, txt_position, hardware_flag, char_space = 0, draw_txt_path = False, draw_rect = False):
        
        if self.txt_cal_flag:
            self.text_dict[hardware_flag]['text_rect'], self.text_dict[hardware_flag]['circumference'], self.text_dict[hardware_flag]['painter_path'], self.text_dict[hardware_flag]['fm'] = self.txt_bounding_box(radius, qfont, qpoint, txt)

        # drawing circular path if set to true
        if draw_txt_path:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.drawPath(self.text_dict[hardware_flag]['painter_path'])
            painter.end()

        if self.txt_cal_flag:
            self.text_dict[hardware_flag]['pts'], self.text_dict[hardware_flag]['ang'] = self.txt_path_all_points(self.text_dict[hardware_flag]['text_rect'], self.text_dict[hardware_flag]['circumference'], self.text_dict[hardware_flag]['painter_path'], txt, char_space, txt_position)

        # rendering text char one by one in circular path
        set_char_pos = 0
        for i in range(len(txt)):
            # creating painter and setting render hint
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            
            # setting font and pen
            painter.setFont(qfont)
            painter.setPen(QPen(txt_colour))

            self.text_dict[hardware_flag]['text_rect'] = self.text_dict[hardware_flag]['fm'].boundingRect(txt[i])  # getting char bounding rectangle
            if txt[i] == ' ': # for space there is no bounding rect 
                self.text_dict[hardware_flag]['text_rect'] = self.text_dict[hardware_flag]['fm'].boundingRect("s") # so I change it to 's' because space and 's' has almost same bounding rect
            set_char_pos += (self.text_dict[hardware_flag]['text_rect'].width()+char_space) # seperating char from colliding
            
            # getting point and angle at point 
            point = self.text_dict[hardware_flag]['pts'][set_char_pos]
            text_angle = self.text_dict[hardware_flag]['ang'][set_char_pos]

            # setting translate position at geted circular path point x, y and rotating text char
            painter.translate(point.x(), point.y())
            painter.rotate(-text_angle)
            
            # setting text char rendering at path point center and drawing text char
            self.text_dict[hardware_flag]['txt_rect'] = QRectF(-self.text_dict[hardware_flag]['text_rect'].width()/2, -self.text_dict[hardware_flag]['text_rect'].height()/2, self.text_dict[hardware_flag]['text_rect'].width(), self.text_dict[hardware_flag]['text_rect'].height())
            painter.drawText(self.text_dict[hardware_flag]['txt_rect'], 0, txt[i])

            # drawing bounding box around char if set to true
            if draw_rect:
                painter.drawRect(self.text_dict[hardware_flag]['txt_rect'])

            painter.end() # closing painter

    # drawing blank circle around value pointer
    def draw_circle_around_pointer(self, radius, width, circle_colour, brush=False):
        # creating painter and setting rendering hints
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        
        painter.setPen(QPen(circle_colour, width))
        if brush:
            painter.setBrush(QBrush(circle_colour))
        painter.drawEllipse(QPointF(self.width()/2, self.height()/2), radius, radius)

        # closing painter
        painter.end()

    # creating a pointer to indicate system condition
    def pointer(self, pointer_size, gradient_start_angle, radius, point_percent, color1=Qt.red, color2=Qt.yellow, color3=Qt.green, color1_set=0.0, color2_set=0.2, color3_set=0.4):
        # creating painter and setting render hint
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        conicalGradient = QConicalGradient(QPointF(self.width()/2, self.width()/2), gradient_start_angle)
        conicalGradient.setColorAt(color1_set, color1)
        conicalGradient.setColorAt(color2_set, color2)
        conicalGradient.setColorAt(color3_set, color3)
        
        painter.setPen(QPen(conicalGradient, 4, join=Qt.MiterJoin))
        painter.setBrush(QBrush(conicalGradient))
        painter_path = QPainterPath()
        painter_path.addEllipse(QPointF(self.width()/2, self.width()/2), radius, radius)
        
        # rotate pointer for animation
        Lpoint = painter_path.pointAtPercent(point_percent)
        ang = painter_path.angleAtPercent(point_percent)
        transform = QTransform()
        transform.translate(round((Lpoint.x() + Lpoint.x()-pointer_size//2 + Lpoint.x()+pointer_size//2) / 3, 2), round((Lpoint.y() + Lpoint.y()-pointer_size + Lpoint.y()+pointer_size) / 3, 2))
        transform.rotate(-ang)
        transform.translate(-round((Lpoint.x() + Lpoint.x()-pointer_size//2 + Lpoint.x()+pointer_size//2) / 3, 2), -round((Lpoint.y() + Lpoint.y()-pointer_size + Lpoint.y()+pointer_size) / 3, 2))
        painter.setTransform(transform)

        # creating triangle pointer
        painter.drawPolygon(Lpoint, QPointF(Lpoint.x()-pointer_size//2, Lpoint.y()+pointer_size), QPointF(Lpoint.x()+pointer_size//2, Lpoint.y()+pointer_size))

        painter.end()

    # to create info label animation
    def animate_circle(self):
        self.rounded_ani = QVariantAnimation(self.widget1)
        self.rounded_ani.setStartValue(0)
        self.rounded_ani.setEndValue(154)
        self.rounded_ani.setDuration(600)
        self.rounded_ani.valueChanged.connect(self.changesize)

    # method to change size of the label at each second
    def changesize(self, value):
        self.radius = value*2
        self.widget1.setStyleSheet(f"border-radius: {value}px; background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 rgb(191, 100, 255), stop:1 blue);")
        self.widget1.setGeometry((self.width()-self.radius)//2, (self.height()-self.radius)//2, self.radius, self.radius)
        
        self.label1.setStyleSheet("background: rgba(0, 0, 0, 0);")
        self.label1.setGeometry(0, self.label1_pos, self.radius, self.radius*4)

        self.widget1.setMask(QRegion(QRect(0, 0, self.radius, self.radius), QRegion.Ellipse))

        # reset required values when animation finish
        if value == 0:
            self.label1.setText("")
            self.result_file.close()
            self.info_timer.stop()
            self.pointer_timer.start(1000)

    # method for getting information from result.json every seconds
    def retrive_info(self, title_property=None, sub_title_property=None, value_property=None):

        # reading result.json file
        with open('./assets/TempINFO/result.json') as self.result_file:
            data = json.load(self.result_file) # saving data in dict formate

        # checking if CPU info is found
        if data["CPU"]["Name"].get("Name") != 'CPU Not Found':
            # getting CPU info
            cpu_dict = {
                "CPU Information" :
                    [
                        ["Name:", data["CPU"]["Name"].get("Name")],
                        ["Number OF Core", str(psutil.cpu_count(logical=False))],
                        ["Number OF Threads", str(psutil.cpu_count(logical=True))],
                        ["Frequency", data["CPU"]["***************Clocks***************"].get("CPU Core #1") if data["CPU"]["***************Clocks***************"].get("CPU Core #1") else data["CPU"]["***************Clocks***************"].get("CPU Core")],
                        ["Temperature", data["CPU"]["*************Temperature*************"].get("CPU Package", "00.0   ")[::-1][3:][::-1]+"C"],
                        ["Utilized", data["CPU"]["*****************Load****************"].get("CPU Total") if data["CPU"]["*****************Load****************"].get("CPU Total") else data["CPU"]["*****************Load****************"].get("CPU Core")],
                        ["Power", data["CPU"]["***************Power****************"].get("CPU Package")]
                    ]
                }
        # else empty dict
        else:
            cpu_dict = {
                "CPU Information" :
                    [
                        ["CPU", "Not Found"]
                    ]
                }

        # checking if GPU is installed in this system
        if self.gpu:
            # getting gpu info
            gpu_dict = {
                "GPU Information" :
                    [
                        ["Name:", data["GPU"]["Name"].get("Name")],
                        ["Frequency", data["GPU"]["***************Clocks***************"].get("GPU Core")],
                        ["Temperature", data["GPU"]["*************Temperature*************"].get("GPU Core", "-_-   ")[::-1][3:][::-1]+"C"],
                        ["Utilized", data["GPU"]["*****************Load****************"].get("GPU Core")],
                        ["Memory Total", data["GPU"]["*****************Data****************"].get("GPU Memory Total")],
                        ["Memory Used", data["GPU"]["*****************Data****************"].get("GPU Memory Used")],
                        ["Memory Free", data["GPU"]["*****************Data****************"].get("GPU Memory Free")],
                        ["Power", data["GPU"]["***************Power****************"].get("GPU Power")]
                    ]
                }
            cpu_dict.update(gpu_dict)

        # getting RAM info 
        ram_dict = {
            "RAM Information" :
                [
                    ["Utilized", data["RAM"]["*****************Load****************"].get("Memory")],
                    ["Memory Total", str(round(float(data["RAM"]["*****************Data****************"].get("Used Memory", "-_-   ")[::-1][3:][::-1])+float(data["RAM"]["*****************Data****************"].get("Available Memory")[::-1][3:][::-1])))+" GB"],
                    ["Memory Used", data["RAM"]["*****************Data****************"].get("Used Memory")],
                    ["Memory Free", data["RAM"]["*****************Data****************"].get("Available Memory")]
                ]
            }
        cpu_dict.update(ram_dict)

        # evenly arranging RAM information
        disk_dict = {}
        disk_info = [["Disk", ''.join(["Total--", "-Used-", "-Free-", "--Use"])]]
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_info.append([part.device[0]+"-Drive", '-'.join([bytes2human(usage.total), bytes2human(usage.used), bytes2human(usage.free), str(usage.percent)+'%'])])
        disk_dict["DISK Information"] = disk_info
        cpu_dict.update(disk_dict)

        # evenly arrenging all getted information
        txt = cpu_dict

        if title_property == None:
            return txt

        str_len_lst = []  
        for key in txt:
            for index in txt[key]:
                index[1] = ' '.join(list(Counter(index[1].split(' '))))
                if len(index[1]) < 11:
                    str_len_lst.append(len(''.join(index)))
                
        ma = max(str_len_lst)

        for key in txt:
            for index in txt[key]:
                if len(index[1]) < 11:
                    space = abs(ma - len(''.join(index)))
                    index[0] += ("-"*space+"->")

        # setting info font size and colour
        txt = {f"""<br> <font face="Consolas" color="{title_property[0]}" size="{title_property[1]}"> <i>{k}</i> </font> <br> <br>""":v for k,v in txt.items()}
        for key in txt:
            for index in range(len(txt[key])): 
                txt[key][index][0] = f"""<font face="Consolas" color="{sub_title_property[0]}" size="{sub_title_property[1]}"> <i>{txt[key][index][0]}</i> </font>"""
                if len(str(txt[key][index][1])) < 11:
                    txt[key][index][1] = f"""<font face="Consolas" color="{value_property[0]}" size="{value_property[1]}"> <i>{txt[key][index][1]}</i> </font> <br>"""
                else:
                    txt[key][index][1] = ' '.join(list(Counter(txt[key][index][1].split(' '))))
                    txt[key][index][1] = f"""<br> <font face="Consolas" color="{value_property[0]}" size="{value_property[1]}"> <i>{txt[key][index][1]}</i> </font> <br>"""
            
        return txt # return edited info html formate txt

    # method to set html info txt to label
    def show_info(self):
        try:
            self.txt = self.retrive_info(["Gold", 10], ["SeaShell", 5], ["Chartreuse", 5])
        except:
            pass

        html = ""
        for names in self.txt:
            html += names
            for name in self.txt[names]:
                html += ''.join(name)

        self.label1.setText(html)

    # updating pointer every second 
    def pointer_update(self):
        try:
            self.all_info = self.retrive_info()
        except:
            pass
        
        cpu_utilized_percentage = float(self.all_info['CPU Information'][5][1][::-1][2:][::-1])
        cpu_temp_percentage = float(self.all_info['CPU Information'][4][1][::-1][2:][::-1])
        ram_utilized_percentage = float(self.all_info['RAM Information'][0][1][::-1][2:][::-1])

        if self.gpu:
            # CPU utilized pointer
            self.cpu_utilized_pointer_if_gpu_present = (cpu_utilized_percentage*0.00274) + 0.112
            # GPU utilized pointer
            gpu_utilized_percentage = float(self.all_info['GPU Information'][3][1][::-1][2:][::-1])
            self.gpu_utilized_pointer = (gpu_utilized_percentage*0.00274) + 0.610

            # CPU temperature pointer
            if cpu_temp_percentage > 100:
                self.cpu_temp_pointer_if_gpu_present = 0.388
            else: self.cpu_temp_pointer_if_gpu_present = (cpu_temp_percentage*0.00274) + 0.114
            # GPU temperature pointer
            gpu_temp_percentage = float(self.all_info['GPU Information'][2][1][::-1][2:][::-1])
            if gpu_temp_percentage > 100:
                self.gpu_temp_pointer = 0.894
            else: self.gpu_temp_pointer = (gpu_temp_percentage*0.00278) + 0.616

        else:
            # CPU utilized pointer
            self.cpu_utilized_pointer_if_gpu_absent = (cpu_utilized_percentage*0.00760) + 0.866
            if self.cpu_utilized_pointer_if_gpu_absent >= 0.999:
                self.cpu_utilized_pointer_if_gpu_absent = (cpu_utilized_percentage*0.00760) - 0.134

            # CPU temperature pointer
            if cpu_temp_percentage > 100:
                self.cpu_temp_pointer_if_gpu_present = 0.616
            else: self.cpu_temp_pointer_if_gpu_absent = (cpu_temp_percentage*0.00732) + 0.884
            if self.cpu_temp_pointer_if_gpu_absent >= 0.999:
                self.cpu_temp_pointer_if_gpu_absent = (cpu_temp_percentage*0.00732) - 0.116
        

        # RAM utilized pointer
        self.ram_utilized_pointer = (ram_utilized_percentage*0.00599) + 0.952
        if self.ram_utilized_pointer >= 0.999:
            self.ram_utilized_pointer = (ram_utilized_percentage*0.00599) - 0.049


        self.update()
                  
    # handle painting event
    def paintEvent(self, event):
        # calling all painting methods

        # calling txt render function
        if self.gpu:
            # CPU, GPU Utilized
            width = self.draw_circle_around_txt(QFont("Consolas", 13, 1, True), "CPU Utilized:", QColor(0, 102, 204), QPointF(*([self.width()/2]*2)), 140)
            self.render_txt(QPointF(*([self.width()/2]*2)), 140, "CPU Utilized:", QFont("Consolas", 13, 1, True), QColor(255, 255, 255), int((2 * math.pi * 140)/4), 'CPU_Utilized', 1)
            self.render_txt(QPointF(*([self.width()/2]*2)), 140, "GPU Utilized:", QFont("Consolas", 13, 1, True), QColor(255, 255, 255), int((2 * math.pi * 140)/4)*3, 'GPU_Utilized', 1)
            self.draw_arc(width, 140, 45, 90, 20)
            self.draw_arc(width, 140, -135, 90, -160)

            # CPU, GPU temperature
            width = self.draw_circle_around_txt(QFont("Consolas", 12, 3, True), "CPU Temp:", QColor(0, 102, 204), QPointF(*([self.width()/2]*2)), 86)
            self.render_txt(QPointF(*([self.width()/2]*2)), 86, "CPU Temp:", QFont("Consolas", 12, 3, True), QColor(255, 255, 255), int((2 * math.pi * 85)/4), 'CPU_Temp', 1)
            self.render_txt(QPointF(*([self.width()/2]*2)), 86, "GPU Temp:", QFont("Consolas", 12, 3, True), QColor(255, 255, 255), int((2 * math.pi * 85)/4)*3, 'GPU_Temp', 1)
            self.draw_arc(width, 86, 45, 85, 20)
            self.draw_arc(width, 86, -131, 81, -160)

        else:
            # CPU Utilized
            width = self.draw_circle_around_txt(QFont("Consolas", 13, 1, True), "CPU Utilized:", QColor(0, 102, 204), QPointF(*([self.width()/2]*2)), 140)
            self.render_txt(QPointF(*([self.width()/2]*2)), 140, "CPU Utilized:", QFont("Consolas", 13, 1, True), QColor(255, 255, 255), -5, 'CPU_Utilized', 1)
            self.draw_arc(width, 140, -221, 265, 90, color2_set=0.5, color3_set=1.0)

            # CPU temperature
            width = self.draw_circle_around_txt(QFont("Consolas", 12, 3, True), "CPU Temp:", QColor(0, 102, 204), QPointF(*([self.width()/2]*2)), 86)
            self.render_txt(QPointF(*([self.width()/2]*2)), 86, "CPU Temp:", QFont("Consolas", 12, 3, True), QColor(255, 255, 255), -5, 'CPU_Temp', 1)
            self.draw_arc(width, 86, -215, 250, 90, color2_set=0.5, color3_set=1.0)

        # RAM usage
        width = self.draw_circle_around_txt(QFont("Consolas", 11, 3), "RAM Used", QColor(0, 102, 204), QPointF(*([self.width()/2]*2)), 41)
        self.render_txt(QPointF(*([self.width()/2]*2)), 41, "RAM Used", QFont("Consolas", 11, 3), QColor(255, 255, 255), -5, 'RAM_Used', 1)
        self.draw_arc(width, 41, -180, 180, 90, color2_set=0.5, color3_set=1.0)

        # circle between segment
        self.draw_circle_around_pointer(112, 30, QColor(0, 0, 0, 170))
        self.draw_circle_around_pointer(63, 24, QColor(0, 0, 0, 170))
        self.draw_circle_around_pointer(16, 29, QColor(0, 0, 0, 170))
        self.draw_circle_around_pointer(10, 0, QColor(0, 102, 204, 200), True)

        if self.gpu:
            # CPU, GPU utilized pointer
            self.pointer(10, -160, 116, self.cpu_utilized_pointer_if_gpu_present) # CPU
            self.pointer(10, 20, 116, self.gpu_utilized_pointer) # GPU
            
            # CPU, GPU temperature pointer
            self.pointer(9, -160, 65, self.cpu_temp_pointer_if_gpu_present) # CPU
            self.pointer(9, 20, 65, self.gpu_temp_pointer) # GPU

        else:
            # CPU utilized, temperature pointer
            self.pointer(10, 90, 115, self.cpu_utilized_pointer_if_gpu_absent, color2_set=0.5, color3_set=1.0) # CPU
            self.pointer(9, 90, 67, self.cpu_temp_pointer_if_gpu_absent, color2_set=0.5, color3_set=1.0) # CPU

        # RAM usage pointer
        self.pointer(9, 90, 25, self.ram_utilized_pointer, color2_set=0.5, color3_set=1.0) # RAM

        self.txt_cal_flag = False

    # method scroll label
    def scroll_label(self):
        if self.pos_ > 60: self.pos_ = 60
        self.label1.move(self.label1.pos().x(), self.pos_)

    # triger animation 
    def circle_ani(self):
        self.pointer_timer.stop()
        self.info_timer.start(1000)
        self.rounded_ani.setDirection(int(self.mouse_doubleClicked))
        self.rounded_ani.start()
        self.mouse_doubleClicked = not self.mouse_doubleClicked # reverse animation

    # catch mouse wheel event occure
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.pos_ += 15
        else:
            self.pos_ -= 15

        self.scroll_label() # scroll info label
            

    # catch double click event occure
    def mouseDoubleClickEvent(self, event):
        self.circle_ani() # triger animation
        

    # catch mouse hold event occure
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    # catch mouse relese event occure
    def mouseReleaseEvent(self, event):
        # assiging current window position
        self.data['position']["x_pos"] = self.pos().x()
        self.data['position']["y_pos"] = self.pos().y()
        # rewriting property.json
        with open('./assets/property.json', 'w') as file:
            json.dump(self.data, file, indent = 4)
            file.close()

    # catch mouse move event occure
    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    # detect key down event
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.finish()

    # catch window close event
    def closeEvent(self, event):
        self.finish()
    
    # to upadate all changed data to property,josn when close
    def finish(self):
        QCoreApplication.instance().quit()  # quit window
        self.result_file.close() # closing result.json file

        close_TempINFO() # close TempINFO.exe file

# function for closing TempINFO.exe using PID
def close_TempINFO():
    running_apps=psutil.process_iter(['pid','name']) #returns names of running processes
    for app in running_apps:
        sys_app=app.info.get('name')

        if sys_app in "TempINFO.exe".split() or "TempINFO.exe" in sys_app:
            pid=app.info.get('pid') #returns PID of the given app if found running
            
            try: #deleting the app if asked app is running.(It raises error for some windows apps)
                app_pid = psutil.Process(pid)
                app_pid.terminate()
            except: pass

# function to check every 500ms if given folder or file is present
def implicite_wait(file):
    if Path(file).is_file():
        return True
    else:
        sleep(0.5)
        return implicite_wait(file)

# function to set working directory
def set_wd():
    # key we want to get value is HKEY_CURRENT_USER
	# key value is Software\Microsoft\Windows\CurrentVersion\App Paths\tempInfo.py
    path = reg.HKEY_CURRENT_USER
    app_path = r"Software\Microsoft\Windows\CurrentVersion\App Paths\tempInfo.py"

    # open the key to get value
    open = reg.OpenKeyEx(path, app_path, 0, reg.KEY_READ)
    cwd_path = reg.QueryValueEx(open, "Path")[0]

    os.chdir(cwd_path) # set cwd

    reg.CloseKey(open) # close open key

# creating QApplication
def load():
    # starting task shaduler TempInfo.lnk shortcut after TempInfo.lnk file created
    if implicite_wait('assets\TempInfo.lnk'):
        os.startfile(os.path.join(os.getcwd(), 'assets\TempInfo.lnk'))

    # starting GUI after result.json file generated from TempINFO.exe
    if implicite_wait('./assets/TempINFO/result.json'):
        app = QApplication(sys.argv)
        sysInfo = SysInfo()
        app.aboutToQuit.connect(sysInfo.finish) # detect close event by system
        sysInfo.show()
        sys.exit(app.exec())

def main():
    # set working directory
    set_wd()
    
    load()

if __name__ == '__main__':
    try:
        main()
    except: # if any error occurs it write occurred error message in errLog.txt file
        error = traceback.format_exc()
        with open('./assets/errLog.txt', 'w') as file:
            file.writelines("Reported date: "+date.today()+"\n"+error)
            file.close()
