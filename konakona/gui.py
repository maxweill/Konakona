import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QSlider,
    QPushButton,
    QComboBox,
    QCheckBox,
    QGroupBox,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ----------------------- Widgets -----------------------

        # Name of window title
        self.setWindowTitle('konakona-gui')

        # Basic Label saying Konakona, Replacing it with image
        self.konakona_label = QLabel('konakona-setup')
        font = self.konakona_label.font()
        font.setPointSize(20)
        self.konakona_label.setFont(font)
        self.konakona_label.setAlignment(Qt.AlignHCenter)

        # Line Edit to enter video path + Button for directory search
        self.video_path = QLineEdit()
        self.video_path.setMaxLength(255)
        self.video_path.setPlaceholderText('Enter Video Filepath')

        self.search_button = QPushButton('S')
        self.search_button.setMaximumSize(20, 40)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.video_path)
        layout2.addWidget(self.search_button)

        # Timer slider + label
        self.timer_label = QLabel('Set timer when to post')
        font2 = self.timer_label.font()
        font2.setPointSize(15)
        self.timer_label.setFont(font2)
        self.timer_label.setAlignment(Qt.AlignHCenter)

        self.timer_slider = QSlider(Qt.Horizontal)
        self.timer_slider.setMinimum(0)
        self.timer_slider.setMaximum(60)
        self.timer_slider.setTickPosition(QSlider.TicksBelow)
        self.timer_slider.setTickInterval(5)
        self.timer_slider.setSingleStep(1)

        self.timer_value = QLabel('slider value: 0')
        self.timer_value.setStyleSheet('color: grey')
        font3 = self.timer_value.font()
        font3.setPointSize(10)
        self.timer_value.setFont(font3)
        self.timer_value.setAlignment(Qt.AlignHCenter)

        # Multi chance slider + label
        self.multi_label = QLabel('Multi-image Chance')
        # font2 = self.multi_label.font()
        # font2.setPointSize(15)
        self.multi_label.setFont(font2)
        self.multi_label.setAlignment(Qt.AlignHCenter)

        self.multi_slider = QSlider(Qt.Horizontal)
        self.multi_slider.setMinimum(0)
        self.multi_slider.setMaximum(10)
        self.multi_slider.setTickPosition(QSlider.TicksBelow)
        self.multi_slider.setTickInterval(1)
        self.multi_slider.setSingleStep(1)

        self.multi_value = QLabel('slider value: 0')
        self.multi_value.setStyleSheet('color: grey')
        # font3 = self.multi_value.font()
        # font3.setPointSize(10)
        self.multi_value.setFont(font3)
        self.multi_value.setAlignment(Qt.AlignHCenter)

        # Multi-image number ComboBox
        self.multi_box_label = QLabel('Choose Multi-Image number:')
        font4 = self.multi_box_label.font()
        font4.setPointSize(10)

        self.multi_box = QComboBox()
        self.multi_box.addItems(['Random', '2', '3', '4'])

        layout3 = QHBoxLayout()
        layout3.addWidget(self.multi_box_label)
        layout3.addWidget(self.multi_box)

        # Video chance slider + label
        self.video_label = QLabel('Video Chance')
        # font2 = self.multi_label.font()
        # font2.setPointSize(15)
        self.video_label.setFont(font2)
        self.video_label.setAlignment(Qt.AlignHCenter)

        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setMinimum(0)
        self.video_slider.setMaximum(10)
        self.video_slider.setTickPosition(QSlider.TicksBelow)
        self.video_slider.setTickInterval(1)
        self.video_slider.setSingleStep(1)

        self.video_value = QLabel('slider value: 0')
        self.video_value.setStyleSheet('color: grey')
        # font3 = self.multi_value.font()
        # font3.setPointSize(10)
        self.video_value.setFont(font3)
        self.video_value.setAlignment(Qt.AlignHCenter)

        self.save_checkbox = QCheckBox('Save images and clips')
        layout4 = QHBoxLayout()
        layout4.addWidget(self.save_checkbox)
        layout4.setAlignment(Qt.AlignHCenter)

        # Keys lineEdit
        self.consumer_key = QLineEdit()
        self.consumer_key.setMaxLength(255)
        self.consumer_key.setPlaceholderText('Enter Consumer Key')
        self.consumer_key.setEchoMode(QLineEdit.Password)

        self.consumer_secret = QLineEdit()
        self.consumer_secret.setMaxLength(255)
        self.consumer_secret.setPlaceholderText('Enter Consumer Secret')
        self.consumer_secret.setEchoMode(QLineEdit.Password)

        self.access_key = QLineEdit()
        self.access_key.setMaxLength(255)
        self.access_key.setPlaceholderText('Enter Access Key')
        self.access_key.setEchoMode(QLineEdit.Password)

        self.access_secret = QLineEdit()
        self.access_secret.setMaxLength(255)
        self.access_secret.setPlaceholderText('Enter Access Secret')
        self.access_secret.setEchoMode(QLineEdit.Password)

        # Etc. comboBox and label
        self.outfile_img_label = QLabel('Choose image output format:')
        font4 = self.outfile_img_label.font()
        font4.setPointSize(10)

        self.outfile_img = QComboBox()
        self.outfile_img.addItems(['jpg', 'png'])

        layout5 = QHBoxLayout()
        layout5.addWidget(self.outfile_img_label)
        layout5.addWidget(self.outfile_img)

        self.outfile_vid_label = QLabel('Choose video output format:')
        font4 = self.outfile_vid_label.font()
        font4.setPointSize(10)

        self.outfile_vid = QComboBox()
        self.outfile_vid.addItems(['mp4', 'mkv', 'avi'])

        layout6 = QHBoxLayout()
        layout6.addWidget(self.outfile_vid_label)
        layout6.addWidget(self.outfile_vid)

        self.apply_button = QPushButton('Apply')

        # ------ When something is done connects the functions ------
        self.timer_slider.valueChanged.connect(self.timer_slider_value)
        self.search_button.clicked.connect(self.search_button_clicked)
        self.multi_slider.valueChanged.connect(self.multi_slider_value)
        # self.multi_box.currentIndexChanged.connect(self.multi_box_int)
        self.multi_box.currentTextChanged.connect(self.multi_box_str)
        self.video_slider.valueChanged.connect(self.video_slider_value)
        self.save_checkbox.stateChanged.connect(self.save_checkbox_state)

        # -------- Laying out window structure --------
        layout = QVBoxLayout()
        layout.addWidget(self.konakona_label)

        groupbox1 = QGroupBox('General')
        groupbox2 = QGroupBox('Keys')
        groupbox3 = QGroupBox('Etc.')
        layout.addWidget(groupbox1)
        layout.addWidget(groupbox2)
        layout.addWidget(groupbox3)

        layout.addWidget(self.apply_button)

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()
        groupbox1.setLayout(vbox1)
        groupbox2.setLayout(vbox2)
        groupbox3.setLayout(vbox3)

        # Real layout
        vbox1.addLayout(layout2)

        vbox1.addWidget(self.timer_label)
        vbox1.addWidget(self.timer_slider)
        vbox1.addWidget(self.timer_value)

        vbox1.addWidget(self.multi_label)
        vbox1.addWidget(self.multi_slider)
        vbox1.addWidget(self.multi_value)

        vbox1.addLayout(layout3)

        vbox1.addWidget(self.video_label)
        vbox1.addWidget(self.video_slider)
        vbox1.addWidget(self.video_value)

        vbox1.addLayout(layout4)

        vbox2.addWidget(self.consumer_key)
        vbox2.addWidget(self.consumer_secret)
        vbox2.addWidget(self.access_key)
        vbox2.addWidget(self.access_secret)

        vbox3.addLayout(layout5)
        vbox3.addLayout(layout6)

        # --------- Qt stuff that needs to be here ---------
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # ---------------- A bunch of functions ----------------
    def search_button_clicked(self):
        print('clicked')

    def timer_slider_value(self, i):
        self.timer_value.setText('slider value: {}'.format(i))
        # if value == 0 then make it gray

    def multi_slider_value(self, i):
        self.multi_value.setText('slider value: {}'.format(i))
        # if value == 0 then make it gray

    def multi_box_int(self, i):
        print('multi-box int: {}'.format(i))

    def multi_box_str(self, s):
        print('multi-box str: {}'.format(s))

    def video_slider_value(self, i):
        self.video_value.setText('slider value: {}'.format(i))
        # if value == 0 then make it gray

    def save_checkbox_state(self, s):
        print('Save-Checkbox: {}'.format(s == Qt.Checked))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
