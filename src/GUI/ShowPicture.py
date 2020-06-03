import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ShowPicture(QDialog):

	def __init__(self, img):

		super().__init__()
		if img == 0:
			self.close()
			return
		layout = QVBoxLayout()
		self.setLayout(layout)

		#图片label
		self.label = QLabel()
		layout.addWidget(self.label)

		#加载图片
		image = QImage.fromData(img)
		self.resize(image.size())
		pixmap = QPixmap.fromImage(image)
		self.label.setPixmap(pixmap)

		#设置窗体信息
		self.setWindowTitle("查看图片")
		self.center()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

	def center(self):
		#获取屏幕坐标系
		screen = QDesktopWidget().screenGeometry()#得到屏幕的坐标系
		#获取窗口坐标系
		size = self.geometry()
		newLeft = (screen.width()-size.width())/2#计算
		newTop = (screen.height()-size.height())/2
		self.move(newLeft,newTop)

	def mousePressEvent(self,QMouseEvent):
		if QMouseEvent.button() == Qt.LeftButton:
			self.flag = True
			self.m_Position = QMouseEvent.globalPos() - self.pos()
			QMouseEvent.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))
		if QMouseEvent.button() == Qt.RightButton:
			self.close()

	def mouseMoveEvent(self,QMouseEvent):
		if Qt.LeftButton and self.flag:
			self.move(QMouseEvent.globalPos()-self.m_Position)
			QMouseEvent.accept()

	def mouseReleaseEvent(self, QMouseEvent):
		self.flag = False
		self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
	with open('test.png', 'rb') as f:
		img = f.read()
	app = QApplication(sys.argv)
	fileload = ShowPicture(img)
	fileload.show()
	sys.exit(app.exec_())