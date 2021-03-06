import sys, os
if hasattr(sys, 'frozen'):
	os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from MainWindow import MainWindow
from ResultDialog import ResultDialog

if __name__ == '__main__':
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	app = QApplication(sys.argv)
	mainWindow = ResultDialog()

	sys.exit(app.exec_())