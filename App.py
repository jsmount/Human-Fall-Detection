import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDesktopWidget, QProgressBar, QFileDialog, QMessageBox, QMainWindow
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from main import *

class VideoProcessingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.selected = ""

    def run(self):
        process_video(self.video_path)
        self.finished.emit()

class SecondPage(QWidget):  
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_threads = []
        self.finished = pyqtSignal()
        self.selected = ""
        self.select_file_button = QPushButton(self)
        self.select_folder_button = QPushButton(self)
        self.select_webcam_button = QPushButton(self)
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
        self.resize(1000,600)
        self.center()
    
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()

        label = QLabel(self)
        label.setText("옵션 선택")
        label.setFont(QFont('Arial', 16, QFont.Bold))
        label.setContentsMargins(20, 10, 0, 0)
        label.setFixedHeight(40)
        hbox.addWidget(label)

        close_label = QLabel(self)
        close_label.setPixmap(QPixmap("icons/close.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        close_label.setAlignment(Qt.AlignRight)
        close_label.setFixedHeight(40)
        hbox.addWidget(close_label)

        vbox.addLayout(hbox)
        vbox.addStretch(1)

        hbox2 = QHBoxLayout()

        # select file

        self.select_file_button.setFixedWidth(300)
        self.select_file_button.setFixedHeight(350)
        self.select_file_button.clicked.connect(self.clicked_select_file)

        select_filelayout = QVBoxLayout(self.select_file_button)
        select_filelayout.setSpacing(10)

        select_file_title = QLabel("Select File", self)
        select_file_title.setAlignment(Qt.AlignCenter)
        select_file_title.setFont(QFont('Arial', 18, QFont.Bold))
        select_file_title.setStyleSheet("border: none;")
        select_filelayout.addWidget(select_file_title)

        icon = QLabel(self)
        icon.setPixmap(QPixmap("icons/document.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("border: none;")
        select_filelayout.addWidget(icon)

        select_file_detail = QLabel(self)
        select_file_detail.setText("동영상 파일 선택하기")
        select_file_detail.setAlignment(Qt.AlignCenter)
        select_file_detail.setFont(QFont('Arial', 12))
        select_file_detail.setStyleSheet("border: none;")
        select_filelayout.addWidget(select_file_detail)

        self.select_file_button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        hbox2.addWidget(self.select_file_button)

        # select folder

        self.select_folder_button.setFixedWidth(300)
        self.select_folder_button.setFixedHeight(350)
        self.select_folder_button.clicked.connect(self.clicked_select_folder)

        select_folder_layout = QVBoxLayout(self.select_folder_button)
        select_folder_layout.setSpacing(10)

        select_folder_title = QLabel("Select Folder", self)
        select_folder_title.setAlignment(Qt.AlignCenter)
        select_folder_title.setFont(QFont('Arial', 18, QFont.Bold))
        select_folder_title.setStyleSheet("border: none;")
        select_folder_layout.addWidget(select_folder_title)

        select_folder_icon = QLabel(self)
        select_folder_icon.setPixmap(QPixmap("icons/folder.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        select_folder_icon.setAlignment(Qt.AlignCenter)
        select_folder_icon.setStyleSheet("border: none;")
        select_folder_layout.addWidget(select_folder_icon)

        select_folder_detail = QLabel(self)
        select_folder_detail.setText("폴더 내의 동영상 모두 선택하기")
        select_folder_detail.setAlignment(Qt.AlignCenter)
        select_folder_detail.setFont(QFont('Arial', 12))
        select_folder_detail.setStyleSheet("border: none;")
        select_folder_layout.addWidget(select_folder_detail)

        self.select_folder_button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        hbox2.addWidget(self.select_folder_button)

        # select webcam

        self.select_webcam_button.setFixedWidth(300)
        self.select_webcam_button.setFixedHeight(350)
        self.select_webcam_button.clicked.connect(self.clicked_select_webcam)

        select_webcam_layout = QVBoxLayout(self.select_webcam_button)
        select_webcam_layout.setSpacing(10)

        select_webcam_title = QLabel("Select Webcam", self)
        select_webcam_title.setAlignment(Qt.AlignCenter)
        select_webcam_title.setFont(QFont('Arial', 18, QFont.Bold))
        select_webcam_title.setStyleSheet("border: none;")
        select_webcam_layout.addWidget(select_webcam_title)

        select_webcam_icon = QLabel(self)
        select_webcam_icon.setPixmap(QPixmap("icons/dslr-camera-gray.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        select_webcam_icon.setAlignment(Qt.AlignCenter)
        select_webcam_icon.setStyleSheet("border: none;")
        select_webcam_layout.addWidget(select_webcam_icon)

        select_webcam_detail = QLabel(self)
        select_webcam_detail.setText("웹캠 선택하기")
        select_webcam_detail.setAlignment(Qt.AlignCenter)
        select_webcam_detail.setFont(QFont('Arial', 12))
        select_webcam_detail.setStyleSheet("border: none;")
        select_webcam_layout.addWidget(select_webcam_detail)

        self.select_webcam_button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        hbox2.addWidget(self.select_webcam_button)

        vbox.addLayout(hbox2)

        detect_button = QPushButton("이상행동 감지하기", self)
        detect_button.setFixedWidth(200)
        detect_button.setFixedHeight(50)
        detect_button.setFont(QFont('Arial', 12))
        detect_button.setStyleSheet("background-color: rgb(52, 152, 219); color: white; border: none; border-radius: 5px;")
        detect_button.clicked.connect(self.start_detect)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(detect_button)

        hbox3.setAlignment(Qt.AlignRight)
        hbox3.setContentsMargins(0, 0, 20, 0)  # 오른쪽 마진을 10으로 설정합니다.

        vbox.addLayout(hbox3)

        hbox4 = QHBoxLayout()
        
        vbox2 = QVBoxLayout()

        selected_file_label = QLabel(self)
        selected_file_label.setText("선택된 파일: ")
        selected_file_label.setFixedHeight(20)
        vbox2.addWidget(selected_file_label)

        progress_bar = QProgressBar(self)
        progress_bar.setFixedHeight(30)
        vbox2.addWidget(progress_bar)

        hbox4.addLayout(vbox2)

        result_button = ResultButton("결과 확인하기", self)
        result_button.setFixedHeight(50)
        hbox4.addWidget(result_button)

        hbox4.setAlignment(Qt.AlignRight)
        hbox4.setContentsMargins(0, 20, 20, 0)

        vbox.addLayout(hbox4)

        self.setLayout(vbox)

        close_label.mousePressEvent = self.close_window
    
    def close_window(self, _event):
        self.close()

    def start_detect(self, _event):
        if self.selected == "Select File":
            self.select_file()
        elif self.selected == "Select Folder":
            self.select_folder()
        elif self.selected == "Select Webcam":
            self.select_webcam()

    def clicked_select_file(self, _event):
        self.selected = "Select File"
        self.set_button_border_color()

    def clicked_select_folder(self, _event):
        self.selected = "Select Folder"
        self.set_button_border_color()

    def clicked_select_webcam(self, _event):
        self.selected = "Select Webcam"
        self.set_button_border_color()

    def set_button_border_color(self):
    # 모든 버튼의 테두리 색상을 회색으로 초기화
        self.select_file_button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        self.select_folder_button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")
        self.select_webcam_button.setStyleSheet("background-color: #cccccc; color: black; border: none; border-radius: 5px;")

        # 선택된 버튼의 테두리 색상을 파란색으로 설정
        if self.selected == "Select File":
            self.select_file_button.setStyleSheet("background-color: #cccccc; color: black; border: 2px solid #3498db; border-radius: 5px;")
        elif self.selected == "Select Folder":
            self.select_folder_button.setStyleSheet("background-color: #cccccc; color: black; border: 2px solid #3498db; border-radius: 5px;")
        elif self.selected == "Select Webcam":
            self.select_webcam_button.setStyleSheet("background-color: #cccccc; color: black; border: 2px solid #3498db; border-radius: 5px;")

    def select_folder(self):
        if self.video_threads:
            show_error_message("A video processing is already in progress.")
            return
        
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", options=QFileDialog.ShowDirsOnly)
        if folder_path:
            video_files = []
            for file in os.listdir(folder_path):
                if file.endswith(('.mp4', '.avi', '.wmv')):
                    video_path = os.path.join(folder_path, file)
                    video_files.append(video_path)

            if video_files:
                for video_path in video_files:
                    video_thread = VideoProcessingThread(video_path)
                    video_thread.finished.connect(self.process_video_finished)
                    self.video_threads.append(video_thread)
                    video_thread.start()
            else:
                show_error_message("No video files found in the selected folder.")
        return folder_path

    def select_file(self):
        if self.video_threads:
            show_error_message("A video processing is already in progress.")
            return

        video_path = QFileDialog.getOpenFileName(None, "Select Video File", "", "Video Files (*.mp4 *.avi *.wmv)")[0]
        if video_path:
            video_thread = VideoProcessingThread(video_path)
            video_thread.finished.connect(self.process_video_finished)
            self.video_threads.append(video_thread)
            video_thread.start()
        else:
            show_error_message("Invalid video file selection.")
        return video_path
    
    def select_webcam(self):
        if self.video_threads:
            show_error_message("A video processing is already in progress.")
            return
        
        video_thread = threading.Thread(target = process_video2)
        video_thread.start()
        return None

    def process_video_finished(self):
        # 비동기 작업이 완료될 때 호출되는 콜백 함수
        print("Video processing finished.")
        #finished.disconnect(self.process_video_finished)
        self.deleteLater()
    

    def show_error_message(self, message, _event):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

class ResultButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setFixedHeight(40)
        self.value=0
        self.setFont(QFont('Arial', 12))
        self.setStyleSheet(
            'background-color: gray; color: white; border: none; border-radius: 5px;'
        )
        self.setEnabled(False)
        self.setText(text)

    def update_button_state(self, value):
        self.setValue(value)
        if value == 100:
            self.setEnabled(True)
            self.setStyleSheet(
                'background-color: rgb(52, 152, 219); color: white; border: none; border-radius: 5px;'
            )
        else:
            self.setEnabled(False)
            self.setStyleSheet(
            'background-color: gray; color: white; border: none; border-radius: 5px;'
            )

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
        self.resize(1000,600)
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

def run_app():
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    app.exec_()

if __name__ == "__main__":
    app_thread = threading.Thread(target=run_app)
    app_thread.start()
    app_thread.join()
    