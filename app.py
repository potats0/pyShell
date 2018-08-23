import sys

from PyQt5.QtWidgets import QApplication

from controller import controller_main
from view import main_view

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctrl_main = controller_main()
    mywin = main_view(ctrl_main)
    mywin.display()
    sys.exit(app.exec_())
