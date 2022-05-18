import sys

from PyQt5.QtWidgets import QApplication, QWidget, QToolTip
from training_ui_7 import MyMainWindow, InstructionsWindow

# 二屏全屏参数 1000 739 12 12 10 0 0
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyMainWindow()
    Iwin = InstructionsWindow()
    win.show()
    win.instructionButton.clicked.connect(Iwin.show_w2)
    sys.exit(app.exec_())
