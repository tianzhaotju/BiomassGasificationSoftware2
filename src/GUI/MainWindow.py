import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		#窗口大小和布局
		width = QApplication.desktop().screenGeometry(0).width()
		height = QApplication.desktop().screenGeometry(0).height()
		self.resize(width*5/6,height*5/6)
		self.center()

		#窗口标题
		self.setWindowTitle('气化炉控制系统软件')

		titleFont = QFont("黑体",12,QFont.Bold)
		########选择颜色########
		text1 = QLabel()
		text1.setFont(titleFont)
		text1.setText("选择颜色:")
		textBox1 = QHBoxLayout()
		textBox1.addWidget(text1)

		#颜色label
		self.colorLabel = QLabel()
		colorBox = QHBoxLayout()
		colorBox.addWidget(self.colorLabel)
		self.colorLabel.setText('<br><br><br><br><br><br>')
		self.colorLabel.setStyleSheet('QWidget {background-color:#000000;height:10px;}')
		self.selectedColor = "#000000"
		self.colorLabel.setToolTip('<b>HSB:</b> (0,0%,0%)')
		#颜色选择按钮
		btn1 = QPushButton('自定义颜色', self)
		btn1.clicked.connect(self.colorSelect1)
		btn2 = QPushButton('常见材质颜色', self)
		btn2.clicked.connect(self.colorSelect2)
		colorBtns = QHBoxLayout()
		colorBtns.addWidget(btn1)
		colorBtns.addWidget(btn2)

		########材质属性########
		text2 = QLabel()
		text2.setFont(titleFont)
		text2.setText("材质属性:")
		textBox2 = QHBoxLayout()
		textBox2.addWidget(text2)

		#5个滑动条
		self.splidersValue = [0,0,0,0,0]
		hbox1 = self.getSplider("透明度:", 0)
		hbox2 = self.getSplider("反射率:", 1)
		hbox3 = self.getSplider("粗糙度:", 2)
		hbox4 = self.getSplider("杂色覆盖率:", 3)
		hbox5 = self.getSplider("穿孔率:", 4)

		#穿孔类型
		self.text4 = QLabel()
		self.text4.setFont(QFont("黑体",10,QFont.Bold))
		self.text4.setText("穿孔类型:")
		textBox4 = QHBoxLayout()
		textBox4.addWidget(self.text4)

		#穿孔类型复选框
		self.chuanKongType = [0,0,0]
		self.chuanKongRadio1 = QCheckBox('菱形')
		self.chuanKongRadio2 = QCheckBox('圆形')
		self.chuanKongRadio3 = QCheckBox('其他')
		self.chuanKongRadio1.stateChanged.connect(self.chuanKong1Checked)
		self.chuanKongRadio2.stateChanged.connect(self.chuanKong2Checked)
		self.chuanKongRadio3.stateChanged.connect(self.chuanKong3Checked)

		textBox4.addWidget(self.chuanKongRadio1)
		textBox4.addWidget(self.chuanKongRadio2)
		textBox4.addWidget(self.chuanKongRadio3)

		########匹配类型########
		text3 = QLabel()
		text3.setFont(titleFont)
		text3.setText("匹配类型:")
		textBox3 = QHBoxLayout()
		textBox3.addWidget(text3)

		#颜色种类单选框
		radioBtn1 = QRadioButton('主体色(同类色)',self)
		#默认选择第一个
		radioBtn1.setChecked(True)
		self.colorType = 1 #单选框标识
		#radioBtn2 = QRadioButton('辅助色',self)
		#radioBtn3 = QRadioButton('点缀色',self)
		self.radioGroup = QButtonGroup(self)
		self.radioGroup.addButton(radioBtn1, 1)
		#self.radioGroup.addButton(radioBtn2, 2)
		#self.radioGroup.addButton(radioBtn3, 3)
		self.radioGroup.buttonClicked.connect(self.radioBtnClicked)
		radioBtns = QHBoxLayout()
		radioBtns.addWidget(radioBtn1)
		#radioBtns.addWidget(radioBtn2)
		#radioBtns.addWidget(radioBtn3)

		#匹配按钮
		searchBtn = QPushButton('匹配', self)
		searchBtn.clicked.connect(self.search)
		searchBtnBox = QHBoxLayout()
		searchBtnBox.addWidget(searchBtn)

		#竖直Layout
		vbox = QVBoxLayout()
		vbox.addLayout(textBox1)
		vbox.addLayout(colorBox)
		vbox.addLayout(colorBtns)
		vbox.addStretch(1)
		vbox.addLayout(textBox2)
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)
		vbox.addLayout(hbox4)
		vbox.addLayout(hbox5)
		vbox.addLayout(textBox4)
		vbox.addStretch(1)
		vbox.addLayout(textBox3)
		vbox.addLayout(radioBtns)
		vbox.addStretch(1)
		vbox.addLayout(searchBtnBox)
		vbox.addStretch(1)

		#设置
		self.setLayout(vbox)
		self.show()

	#主窗口居中
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	#调色板调用
	def colorSelect1(self):
		col = QColorDialog.getColor()
		if col.isValid():
			self.changeColor(col.name())

	#常见材质颜色选择
	def colorSelect2(self):
		colorDialog = MaterialColorDialog()
		if colorDialog.exec_() == QDialog.Accepted:
			pass
		if colorDialog.colorIndex != -1:
			self.changeColor(colorDialog.result)

	def changeColor(self, newColor):
		self.colorLabel.setStyleSheet('QWidget {background-color:%s}' % newColor)
		self.selectedColor = newColor
		h, s, v = hex_hsv(newColor)
		self.colorLabel.setToolTip('<b>HSB:</b> ('+ str(h) + ', ' + str(s) +'%, ' + str(v) +'%)')

	#输入滑块名字和序号，获得一组横向滑块
	def getSplider(self, name, index):
		#创建滑块
		splider = QSlider(Qt.Horizontal, self)
		splider.setMinimum(0)
		splider.setMaximum(100)
		splider.setTickInterval(10)
		splider.valueChanged.connect(lambda: self.changeValue(splider, value, index))

		#创建文本框
		label = QLabel()
		label.setFont(QFont("宋体",10))
		label.setText(name)
		value = QLabel()
		value.setFont(QFont("宋体",10))
		value.setNum(0)

		#复选框
		checkBox = QCheckBox()
		checkBox.setChecked(True)
		checkBox.stateChanged.connect(lambda:self.whichCanUse(label, value, splider, index))
		checkBox.stateChanged.connect(self.canUse)
		checkBox.setStyleSheet("""
QCheckBox::indicator{
					width: 25px;
					height: 25px;
				}""")
		#横向Layout
		hbox = QHBoxLayout()
		subHBox = QHBoxLayout()
		#添加靠左对齐的控件
		subHBox.addWidget(checkBox, Qt.AlignLeft)
		subHBox.addWidget(label, Qt.AlignLeft)
		subHBox.addWidget(value, Qt.AlignLeft)
		hbox.addLayout(subHBox)
		hbox.addWidget(splider, Qt.AlignLeft)
		#设置0,1列的比例为1:3
		hbox.setStretch(0, 1)
		hbox.setStretch(1, 3)

		return hbox

	#滑块取值事件
	def changeValue(self, splider, value, index):
		value.setNum(splider.value())
		self.splidersValue[index] = splider.value()
		#print(self.splidersValue[index])

	def whichCanUse(self, label, value, splider, index):
		self.tempIndex = index
		self.tempLabel = label
		self.tempValue = value
		self.tempSplider = splider
		#穿孔
		#if index == 4:
			#print("穿孔")

	#复选框检查
	def canUse(self, state):
		if state != Qt.Checked:
			self.tempLabel.setEnabled(False)
			self.tempValue.setEnabled(False)
			self.tempSplider.setEnabled(False)
			self.splidersValue[self.tempIndex] = -1
		else:
			self.tempLabel.setEnabled(True)
			self.tempValue.setEnabled(True)
			self.tempSplider.setEnabled(True)
			self.splidersValue[self.tempIndex] = self.tempSplider.value()
		if self.tempIndex == 4:
			if state != Qt.Checked:
				self.text4.setVisible(False)
				self.chuanKongRadio1.setVisible(False)
				self.chuanKongRadio2.setVisible(False)
				self.chuanKongRadio3.setVisible(False)
			else:
				self.text4.setVisible(True)
				self.chuanKongRadio1.setVisible(True)
				self.chuanKongRadio2.setVisible(True)
				self.chuanKongRadio3.setVisible(True)


	def radioBtnClicked(self):
		self.colorType = self.radioGroup.checkedId()
		#print(self.colorType)

	def chuanKong1Checked(self, state):
		if state != Qt.Checked:
			self.chuanKongType[0] = 0
		else:
			self.chuanKongType[0] = 1

	def chuanKong2Checked(self, state):
		if state != Qt.Checked:
			self.chuanKongType[1] = 0
		else:
			self.chuanKongType[1] = 1

	def chuanKong3Checked(self, state):
		if state != Qt.Checked:
			self.chuanKongType[2] = 0
		else:
			self.chuanKongType[2] = 1

	def search(self):
		mColor = self.selectedColor
		mColorType = self.colorType
		mValue0 = self.splidersValue[0]
		mValue1 = self.splidersValue[1]
		mValue2 = self.splidersValue[2]
		mValue3 = self.splidersValue[3]
		mValue4 = self.splidersValue[4]
		chuanKongType = self.chuanKongType
		excel = DBExcel('data/', mColor, mColorType, mValue0, mValue1, mValue2, mValue3, mValue4, chuanKongType)
		materials = excel.getSelectedMaterial()
		print(len(materials), mColor, mColorType, mValue0, mValue1, mValue2, mValue3, mValue4, chuanKongType)
		if len(materials) == 0:
			reply = QMessageBox.information(self,
										"无结果",  
										"没有根据您的条件匹配到合适的材料。",  
										QMessageBox.Ok)
			return
		resultDialog = ResultDialog(materials)
		if resultDialog.exec_() == QDialog.Accepted:
			pass








