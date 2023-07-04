import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from soundWindow import Ui_Form
import math
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene
from sound import Sound
import threading
import time

class SoundWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #连接点击事件到槽函数
        self.ui.clearSound.clicked.connect(self.clear_sound_list)
        self.ui.createSound.clicked.connect(self.create_sound)
        self.ui.soundView.mousePressEvent = self.on_graphicsView_clicked
        self.scene = QGraphicsScene(self)
        self.ui.soundView.setScene(self.scene)
        self.draw_polar_coordinates()
        self.soundListData = [] # 保存声音数据
        # update_thread = threading.Thread(target=self.refresh_sound_list())
        # update_thread.daemon = True
        # update_thread.start()

    def clear_sound_list(self):
        model = self.ui.soundList.model()
        selected_indexes = self.ui.soundList.selectedIndexes()
        selected_rows = {index.row() for index in selected_indexes}
        self.soundListData = [sound for i, sound in enumerate(self.soundListData) if i not in selected_rows]
        for index in reversed(selected_indexes):
            model.removeRow(index.row())

    def create_sound(self):
        sound_type = self.ui.comboBox.currentText().split()[-1]
        power = float(self.ui.powerInput.text())
        site_str = self.ui.siteInput.text()
        site_list = [float(coord.strip()) for coord in site_str.split(",")]
        decay_type = self.ui.comboBox_2.currentText().split()[-1]
        decay_time = float(self.ui.decayTime.text())
        sport_type = self.ui.comboBox_3.currentText().split()[-1]
        sport_speed = float(self.ui.speed.text())
        if len(site_list) != 2:
            print("坐标输入错误")
            return
        sound = Sound(sound_type, site_list, power, decay_type, decay_time, sport_type, sport_speed)
        self.soundListData.append(sound)
        self.refresh_sound_list()

    def refresh_sound_list(self):
      #while True:
        # Display the sound objects in the soundList
        model = QtGui.QStandardItemModel()
        for sound in self.soundListData:
            item = QtGui.QStandardItem(f"Type: {sound.type}, Site: {sound.site}, Power: {sound.power}, DType: {sound.decay_type}, DTime: {sound.decay_time}, S_Type: {sound.sport_type}, Speed: {sound.sport_speed}")
            model.appendRow(item)
        self.ui.soundList.setModel(model)
        # QtGui.QGuiApplication.postEvent(self.ui.soundList, QtGui.QHelpEvent(QtCore.QEvent.ChildAdded, model))
        # time.sleep(1)

    def on_graphicsView_clicked(self, event):
        view = self.ui.soundView
        pos = view.mapToScene(event.pos())
        center = QPointF(0, 0)  # 假设圆心在原点
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        radius = round((dx ** 2 + dy ** 2) ** 0.5,2)
        angle = round(math.degrees(math.atan2(-dy, dx)),2)
        self.ui.siteInput.setText(f"{radius}, {angle}")

    def draw_polar_coordinates(self):
        # 设置坐标系参数
        radius = 150  # 极坐标系半径
        angle_range = 360  # 极坐标系角度范围

        # 绘制圆形
        pen = QPen(Qt.black)
        pen.setWidth(2)
        self.scene.addEllipse(-radius, -radius, radius * 2, radius * 2, pen)

        # 绘制极坐标系
        pen.setStyle(Qt.DashLine)
        for angle in range(0, angle_range, 10):
            radian = math.radians(angle)
            dx = radius * math.cos(radian)
            dy = -radius * math.sin(radian)
            self.scene.addLine(0, 0, dx, dy, pen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SoundWindow()
    window.show()
    sys.exit(app.exec_())
