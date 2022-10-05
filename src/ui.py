from PyQt5.QtGui import QPalette, QColor, QTextCursor
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDateEdit, QFrame, QTextEdit,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton,
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QToolBar, QAction, QStatusBar, QWidget
)

def setup(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        #file_menu.addAction(button_action)


        # selector
        wbs_num_select = QComboBox()
        wbs_num_select.addItems(["WBS 100", "WBS 140", "WBS 160", "WBS 180"])

        firstname_input = QLineEdit()
        firstname_input.setPlaceholderText("First name")
        necessary_field_pal = firstname_input.palette()
        necessary_field_pal.setColor(QPalette.PlaceholderText, QColor(170,0,0,190))
        firstname_input.setPalette(necessary_field_pal)

        lastname_input = QLineEdit()
        lastname_input.setPlaceholderText("Last name")
        lastname_input.setPalette(necessary_field_pal)

        street_input   = QLineEdit()
        street_input.setPlaceholderText("Street name and house number")

        zip_code_input = QLineEdit()
        zip_code_input.setMaxLength(5)
        zip_code_input.setPlaceholderText("Zip code")
        
        city_input     = QLineEdit()
        city_input.setPlaceholderText("City name")

        email_input    = QLineEdit()
        email_input.setPlaceholderText("Email address")
        email_input.setPalette(necessary_field_pal)

        phone_input    = QLineEdit()
        phone_input.setPlaceholderText("Phone number")

        filter_input   = QLineEdit()
        filter_input.setPlaceholderText("Keywords for filtering")

        wbs_bool_input = QCheckBox("I have a WBS (Wohnberechtigungsschein)")
        wbs_bool_input.setCheckState(Qt.Unchecked)
        wbs_bool_input.stateChanged.connect(self.show_wbs_conf_box)
        
        wbs_date_input = QDateEdit()

        wbs_rooms_input= QSpinBox()
        wbs_rooms_input.setMinimum(1)
        wbs_rooms_input.setMaximum(100)

        start_bot_btn = QPushButton("Start bot")
        self.console_out   = QTextEdit(readOnly=True)


        # Sends the current index (position) of the selected item.
        #wbs_num_select.currentIndexChanged.connect( self.index_changed )

        # There is an alternate signal to send the text.
        #wbs_num_select.currentTextChanged.connect( self.text_changed )

        main            = QVBoxLayout()
        conf_box        = QHBoxLayout()
        console_box     = QHBoxLayout()
        conf_box_left   = QVBoxLayout()
        conf_box_right  = QVBoxLayout()
        zip_city_layout = QHBoxLayout()

        self.wbs_conf_frame = QFrame()

        wbs_conf_box       = QHBoxLayout()
        wbs_conf_box_left  = QVBoxLayout()
        wbs_conf_box_right = QVBoxLayout()
        print('test')

        conf_box_left.addWidget(firstname_input)
        conf_box_right.addWidget(lastname_input)
        conf_box_left.addWidget(street_input)
        zip_city_layout.addWidget(zip_code_input)
        zip_city_layout.addWidget(city_input)
        conf_box_right.addLayout(zip_city_layout)
        conf_box_left.addWidget(email_input)
        conf_box_right.addWidget(phone_input)
        conf_box_left.addWidget(wbs_bool_input)
        conf_box_right.addWidget(start_bot_btn)
        
        wbs_conf_box_left.addWidget(wbs_num_select)
        wbs_conf_box_right.addWidget(wbs_date_input)
        wbs_conf_box.addLayout(wbs_conf_box_left)
        wbs_conf_box.addLayout(wbs_conf_box_right)
        self.wbs_conf_frame.setLayout(wbs_conf_box)
        self.wbs_conf_frame.hide()

        conf_box.addLayout(conf_box_left)
        conf_box.addLayout(conf_box_right)
        console_box.addWidget(self.console_out)
        main.addLayout(conf_box, 6)
        main.addWidget(self.wbs_conf_frame, 4)
        main.addLayout(console_box, 20)

        widget = QWidget()
        widget.setLayout(main)


        self.setCentralWidget(widget)


                # text input
        # widget = QLineEdit()

        # int input
        # widget = QSpinBox()
        # widget.setMinimum(-10)
        # widget.setMaximum(3)
        # Or: widget.setRange(-10,3)
        # widget.setPrefix("$")
        # widget.setSuffix("c")