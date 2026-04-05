import sys
from PyQt5.QtWidgets import QApplication
from ui import SSHApp


def main():
    app = QApplication(sys.argv)

    window = SSHApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()