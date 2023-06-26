import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDesktopWidget, QBoxLayout
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class SecondPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle("Human_Fall_Detection")
        self.setWindowIcon(QIcon("icons/fall_icon.png"))
        self.resize(890,500)
        self.center()
    
        vbox = QVBoxLayout()

        label = QLabel(self)
        label.setText("옵션 선택")
        label.setFont(QFont('Arial', 16, QFont.Bold))
        label.setContentsMargins(10, 10, 0, 0)
        vbox.addWidget(label)

        hbox = QHBoxLayout()

        # select file

        button = QPushButton(self)
        button.setFixedWidth(260)
        button.setFixedHeight(300)

        layout = QVBoxLayout(button)
        layout.setSpacing(10)

        title = QLabel("Select File", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 18, QFont.Bold))
        layout.addWidget(title)

        icon = QLabel(self)
        icon.setPixmap(QPixmap("icons/document.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        detail = QLabel(self)
        detail.setText("동영상 파일 선택하기")
        detail.setAlignment(Qt.AlignCenter)
        detail.setFont(QFont('Arial', 12))
        layout.addWidget(detail)

        button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        hbox.addWidget(button)

        # select folder

        button2 = QPushButton(self)
        button2.setFixedWidth(260)
        button2.setFixedHeight(300)

        layout2 = QVBoxLayout(button2)
        layout2.setSpacing(10)

        title2 = QLabel("Select Folder", self)
        title2.setAlignment(Qt.AlignCenter)
        title2.setFont(QFont('Arial', 18, QFont.Bold))
        layout2.addWidget(title2)

        icon2 = QLabel(self)
        icon2.setPixmap(QPixmap("icons/folder.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        icon2.setAlignment(Qt.AlignCenter)
        layout2.addWidget(icon2)

        detail2 = QLabel(self)
        detail2.setText("폴더 내의 동영상 모두 선택하기")
        detail2.setAlignment(Qt.AlignCenter)
        detail2.setFont(QFont('Arial', 12))
        layout2.addWidget(detail2)

        button2.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        hbox.addWidget(button2)

        # select webcam

        button3 = QPushButton(self)
        button3.setFixedWidth(260)
        button3.setFixedHeight(300)

        layout3 = QVBoxLayout(button3)
        layout3.setSpacing(10)

        title3 = QLabel("Select Webcam", self)
        title3.setAlignment(Qt.AlignCenter)
        title3.setFont(QFont('Arial', 18, QFont.Bold))
        layout3.addWidget(title3)

        icon3 = QLabel(self)
        icon3.setPixmap(QPixmap("icons/dslr-camera-gray.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        icon3.setAlignment(Qt.AlignCenter)
        layout3.addWidget(icon3)

        detail3 = QLabel(self)
        detail3.setText("웹캠 선택하기")
        detail3.setAlignment(Qt.AlignCenter)
        detail3.setFont(QFont('Arial', 12))
        layout3.addWidget(detail3)

        button3.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        hbox.addWidget(button3)

        vbox.addLayout(hbox)

        detect_button = QPushButton("이상행동 감지하기", self)
        detect_button.setFixedWidth(200)
        detect_button.setFixedHeight(40)
        detect_button.setFont(QFont('Arial', 12))
        detect_button.setStyleSheet("background-color: rgb(52, 152, 219); color: white; border: none; border-radius: 5px;")

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(detect_button)

        hbox2.setAlignment(Qt.AlignRight)
        hbox2.setContentsMargins(0, 0, 20, 0)  # 오른쪽 마진을 10으로 설정합니다.

        vbox.addLayout(hbox2)

        self.setLayout(vbox)



class MyApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle("Human_Fall_Detection")
        self.setWindowIcon(QIcon("icons/fall_icon.png"))
        self.resize(890,500)
        self.center()

        vbox = QVBoxLayout()

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)

        label = QLabel(self)
        label.setText("Human Fall Detection")
        label.setGeometry(0, 0, 500, 50)
        label.setFont(QFont('Arial', 24, QFont.Bold))
        label.setContentsMargins(20, 20, 0, 0)
        vbox.addWidget(label)

        detail = QLabel(self)
        detail.setText("이 서비스는 작업자의 낙상 감지를 위해 제작되었습니다. 동영상 파일 또는 폴더를 선택하거나 웹캠을 이용하여 낙상을 감지할 수 있습니다.")
        detail.setContentsMargins(20, 0, 20, 20)
        vbox.addWidget(detail)

        button = QPushButton("Start", self)
        button.setStyleSheet("background-color: gray; color: white; border: none; border-radius: 5px;")
        button.setFont(QFont('Arial', 16))
        button.setFixedWidth(100)
        button.setFixedHeight(40)
        button.clicked.connect(self.go_to_second_page)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox_images = QHBoxLayout()

        pixmap = QPixmap("icons/fall_icon.png")
        pixmap = pixmap.scaled(170, 170, Qt.AspectRatioMode.KeepAspectRatio)
        label_img = QLabel()
        label_img.setPixmap(pixmap)
        label_img.setAlignment(Qt.AlignHCenter)
        hbox_images.addWidget(label_img)

        pixmap2 = QPixmap("icons/dslr-camera.png")
        pixmap2 = pixmap2.scaled(170, 170, Qt.AspectRatioMode.KeepAspectRatio)
        label_img2 = QLabel()
        label_img2.setPixmap(pixmap2)
        label_img2.setAlignment(Qt.AlignHCenter)
        hbox_images.addWidget(label_img2)

        vbox.addLayout(hbox_images)

        hbox_images2 = QHBoxLayout()

        pixmap3 = QPixmap("icons/warning.png")
        pixmap3 = pixmap3.scaled(170, 170, Qt.AspectRatioMode.KeepAspectRatio)
        label_img3 = QLabel()
        label_img3.setPixmap(pixmap3)
        label_img3.setAlignment(Qt.AlignHCenter)
        hbox_images2.addWidget(label_img3)

        pixmap4 = QPixmap("icons/group.png")
        pixmap4 = pixmap4.scaled(170, 170, Qt.AspectRatioMode.KeepAspectRatio)
        label_img4 = QLabel()
        label_img4.setPixmap(pixmap4)
        label_img4.setAlignment(Qt.AlignHCenter)
        hbox_images2.addWidget(label_img4)

        vbox.addLayout(hbox_images2)

        self.setLayout(vbox)

        self.show()

    def go_to_second_page(self):
        self.hide()
        self.second = SecondPage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
    