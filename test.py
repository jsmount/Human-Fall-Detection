import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton

class MyApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.count = 0

        self.setWindowTitle("My First Application")

        layout = QHBoxLayout()
        self.setLayout(layout)

        my_label = QLabel('버튼 누르기')
        layout.addWidget(my_label)

        my_button = QPushButton('누르세요')
        my_button.clicked.connect(self.button_click)
        layout.addWidget(my_button)

        self.counter = QLabel('button clicked : 0 times')
        layout.addWidget(self.counter)

        self.show()

    def button_click(self):
        self.count += 1
        self.counter.setText(f'button clicked : {self.count} times')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    