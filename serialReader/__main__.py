''' 
Main function for the Friction Ramp Analysis Software
'''

import sys
from PyQt5.QtWidgets import QApplication
from .classes.callSerialReader import (
        serialReaderUI)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Creates an instance of the main GUI
    # defined in defined in callForceRampGUI.py
    w = serialReaderUI()
    w.show()
    sys.exit(app.exec_())
