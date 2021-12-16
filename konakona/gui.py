import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QSlider,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Name of window title
        self.setWindowTitle('gui-setup')

        # Basic Label saying Konakona, Replacing it with image
        self.konakona_label = QLabel('konakona')
        font = self.konakona_label.font()
        font.setPointSize(25)
        self.konakona_label.setFont(font)
        self.konakona_label.setAlignment(Qt.AlignHCenter)

        # Line Edit to enter video path + Button for directory search
        self.video_path = QLineEdit()
        self.video_path.setMaxLength(255)
        self.video_path.setPlaceholderText('Enter Video Filepath')

        self.search_button = QPushButton('S')

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

        # When something is done connects the functions
        self.timer_slider.valueChanged.connect(self.timer_slider_value)
        self.search_button.clicked.connect(self.search_button_clicked)

        # Laying out window structure
        layout = QVBoxLayout()
        layout.addWidget(self.konakona_label)
        layout.addLayout(layout2)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.timer_slider)
        layout.addWidget(self.timer_value)

        # Qt stuff that needs to be here
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def search_button_clicked(self):
        print('clicked')

    def timer_slider_value(self, i):
        self.timer_value.setText('slider value: {}'.format(i))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
