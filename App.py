import sys
import os
import threading
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDesktopWidget, QProgressBar, QFileDialog, QMessageBox, QMainWindow
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from main import *

class SecondPage(QWidget):  
    finished = pyqtSignal()
    progressed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_threads = [] # video_threads가 비어있는 경우에만 동영상 처리를 진행할 수 있음
        self.selected = "" # select file, select folder, select webcam 중 하나 선택 후 선택된 string값을 저장
        self.select_file_button = QPushButton(self)
        self.select_folder_button = QPushButton(self)
        self.select_webcam_button = QPushButton(self)
        self.result_button = QPushButton("결과 확인하기", self)
        self.selected_file_label = QLabel(self)
        self.finished.connect(self.process_video_finished)
        self.progressed_value = 0 # 진행 정도를 나타내는 변수
        self.progressed.connect(self.update_progress)
        self.initUI()
        self.show()

    def set_progressed_value(self, value):
        self.progressed_value = value
        self.progressed.emit(self.progressed_value)  # 시그널 발생

        if self.progressed_value == 100:    # 진행바 값이 100인 경우
            self.result_button.setStyleSheet(
                'background-color: rgb(52, 152, 219); color: white; border: none; border-radius: 5px;'
            )
            self.result_button.setEnabled(True) # 결과 보기 버튼 활성화
            self.video_threads = []     # video_thread 초기화

    def center(self):
        '''
            화면에 가운데에 위치하도록 하는 함수
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle("Human_Fall_Detection") # 창 제목
        self.setWindowIcon(QIcon("icons/fall_icon.png")) # 창 제목 옆에나오는 아이콘
        self.resize(1000,600) # 창 크기 가로 1000, 세로 600
        self.center() # 가운데에 위치하도록
    
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()    # 옵션 선택, x 버튼 포함

        label = QLabel(self)
        label.setText("옵션 선택")
        label.setFont(QFont('Arial', 16, QFont.Bold))
        label.setContentsMargins(20, 10, 0, 0) # 마진은 왼쪽, 위, 오른쪽, 아래 순서
        label.setFixedHeight(40)
        hbox.addWidget(label)

        close_label = QLabel(self)
        close_label.setPixmap(QPixmap("icons/close.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        close_label.setAlignment(Qt.AlignRight)
        close_label.setFixedHeight(40)
        hbox.addWidget(close_label)

        vbox.addLayout(hbox)
        vbox.addStretch(1) # 필요한 공간을 만들기 위해 사용하는 함수

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

        # 이상행동 감지하기 버튼 

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


        self.selected_file_label.setText("선택된 파일 또는 폴더: ")
        self.selected_file_label.setFixedHeight(20)
        vbox2.addWidget(self.selected_file_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setValue(0)
        vbox2.addWidget(self.progress_bar)

        hbox4.addLayout(vbox2)

        # ResultButton("결과 확인하기", self)
        self.result_button.setFixedWidth(200)
        self.result_button.setFixedHeight(50)
        self.result_button.setFont(QFont('Arial', 12))
        self.result_button.setStyleSheet(
            # 비활성화 상태의 style
            'background-color: gray; color: white; border: none; border-radius: 5px;'
        )
        self.result_button.setEnabled(False) # 비활성화
        self.result_button.clicked.connect(self.show_result) # 버튼을 클릭하는 경우 show_result 함수 실행
        hbox4.addWidget(self.result_button)

        hbox4.setAlignment(Qt.AlignRight)
        hbox4.setContentsMargins(0, 20, 20, 0)  # 위, 오른쪽에 20씩 마진

        vbox.addLayout(hbox4)

        self.setLayout(vbox)

        close_label.mousePressEvent = self.close_window     # close_label(x 버튼)을 클릭하는 경우 close_window 함수 실행
    
    def close_window(self, _event):
        self.close()    # 창 닫기

    def start_detect(self, _event):
        '''
            이상행동 감지하기 버튼을 눌렀을 때 실행되는 함수
        '''
        if self.selected == "Select File":  # 선택된 값이 select file이라면 select_file() 함수 실행
            self.select_file()
        elif self.selected == "Select Folder": # 선택된 값이 select folder select_folder() 함수 실행
            self.select_folder()
        elif self.selected == "Select Webcam": # 선택된 값이 select webcam이라면 select_webcam() 함수 실행
            self.select_webcam()

    def show_result(self, _event):
        '''
            파일 탐색기를 이용해 결과 폴더를 열어준다.
        '''
        current_path = os.getcwd()
        folder_path = os.path.join(current_path, "results")
        subprocess.Popen(f'explorer "{folder_path}"')

    def clicked_select_file(self, _event):
        '''
            선택된 옵션이 select file인 경우
        '''
        self.selected = "Select File" 
        self.set_button_border_color() # 선택된 버튼의 border를 파란색으로 설정

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
        '''
            select folder 버튼을 클릭한 경우 실행되는 함수
        '''
        if self.video_threads: # video_threads가 존재한다면 이미 처리가 진행중인 영상이 존재함을 의미 => 오류 메시지 출력
            show_error_message("A video processing is already in progress.")
            return
        
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", options=QFileDialog.ShowDirsOnly)
        if folder_path:
            self.selected_file_label.setText(f"선택된 파일 또는 폴더: {folder_path}")
            video_files = []
            for file in os.listdir(folder_path):
                if file.endswith(('.mp4', '.avi', '.wmv')):
                    video_path = os.path.join(folder_path, file)
                    video_files.append(video_path)

            if video_files:
                for video_path in video_files:
                    video_thread = threading.Thread(target=self.process_video, args=(video_path,))
                    video_thread.start()
                    self.video_threads.append(video_thread)
            else:
                show_error_message("No video files found in the selected folder.")
        return folder_path

    def select_file(self):
        '''
            select file 버튼을 클릭한 경우 실행되는 함수
        '''
        if self.video_threads:
            show_error_message("A video processing is already in progress.")
            return

        video_path = QFileDialog.getOpenFileName(None, "Select Video File", "", "Video Files (*.mp4 *.avi *.wmv)")[0]
        if video_path:
            self.selected_file_label.setText(f"선택된 파일 또는 폴더: {video_path}")
            video_thread = threading.Thread(target=self.process_video, args=(video_path,))
            video_thread.start()
            self.video_threads.append(video_thread)
        else:
            show_error_message("Invalid video file selection.")
        return video_path

    def select_webcam(self):
        '''
            select webcam 버튼을 클릭한 경우 실행되는 함수
        '''
        if self.video_threads:
            show_error_message("A video processing is already in progress.")
            return
        
        video_thread = threading.Thread(target = process_video2)
        video_thread.start()
        return None
    
    def process_video(self, video_path):
        '''
            select file, select folder의 경우 영상 처리를 위해 실행되는 함수
        '''
        vid_cap = cv2.VideoCapture(video_path)

        if not vid_cap.isOpened():
            show_error_message('Error while trying to read video. Please check path again')
            return

        model, device = get_pose_model()
        vid_out = prepare_vid_out(video_path, vid_cap)

        frames = []
        success, frame = vid_cap.read()
        frame_count = 0
        while success:
            frames.append(frame)
            success, frame = vid_cap.read()
            frame_count += 1

        for i, image in enumerate(frames):
            processed_image = process_frame(image, model, device)
            vid_out.write(processed_image)
            progress = int((i + 1) / frame_count * 100)
            self.set_progressed_value(progress)
            QApplication.processEvents()

        vid_cap.release()
        vid_out.release()
        print("Processing video:", video_path)
        self.finished.emit()
    
    def update_progress(self, value):
        '''
            진행바의 값을 업데이트 하는 함수
        '''
        self.progress_bar.setValue(value)

    def process_video_finished(self):
        # 비동기 작업이 완료될 때 호출되는 콜백 함수
        print("Video processing finished.")
        self.finished.disconnect(self.process_video_finished)
    

    def show_error_message(self, message, _event):
        '''
            에러 메시지를 출력해주는 함수
        '''
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

class MyApp(QWidget):
    '''
        첫 번째 페이지
    '''
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

def main():
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    app.exec_()

if __name__ == "__main__":
    main()