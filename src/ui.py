from PyQt5.QtGui import QPalette, QColor, QTextCursor, QKeySequence
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDateEdit, QFrame, QTextEdit,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton,
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QToolBar, QAction, QStatusBar, QWidget
)

def setup(self):

        ### Menu
        menu = self.menuBar()

        ## File
        file_menu = menu.addMenu("&File")

        # Load config from condig file
        load_config_btn = QAction("&Load config file", self)
        load_config_btn.setStatusTip("Load configuration to run the bot with from configuration file.")
        load_config_btn.setShortcut(QKeySequence("Ctrl+l"))

        file_menu.addAction(load_config_btn)

        # Save config to condig file
        save_config_btn = QAction("&Save config to file", self)
        save_config_btn.setStatusTip("Save current configuration to configuration file.")
        save_config_btn.setShortcut(QKeySequence("Ctrl+s"))
        file_menu.addAction(save_config_btn)

        ## Settings
        settings_menu = menu.addMenu("&Settings")
        set_test_run_btn = QAction("&Test run", self)
        set_test_run_btn.setStatusTip("Only run on test-data, this does not require a network connection.")
        set_test_run_btn.setCheckable(True)
        set_test_run_btn.triggered.connect(self.set_test_run)
        settings_menu.addAction(set_test_run_btn)


        firstname_input = QLineEdit()
        firstname_input.setPlaceholderText("First name")
        necessary_field_pal = firstname_input.palette()
        necessary_field_pal.setColor(QPalette.PlaceholderText, QColor(170,0,0,190))
        firstname_input.setPalette(necessary_field_pal)
        firstname_input.textEdited.connect(lambda text: self.text_edited(text, 0))

        lastname_input = QLineEdit()
        lastname_input.setPlaceholderText("Last name")
        lastname_input.setPalette(necessary_field_pal)
        lastname_input.textEdited.connect(lambda text: self.text_edited(text, 1))

        street_input   = QLineEdit()
        street_input.setPlaceholderText("Street name and house number")
        street_input.textEdited.connect(lambda text: self.text_edited(text, 2))

        zip_code_input = QLineEdit()
        zip_code_input.setMaxLength(5)
        zip_code_input.setPlaceholderText("Zip code")
        #zip_code_input.setInputMask('00000;_')
        zip_code_input.textEdited.connect(lambda text: self.text_edited(text, 3))
        
        city_input     = QLineEdit()
        city_input.setPlaceholderText("City name")
        city_input.textEdited.connect(lambda text: self.text_edited(text, 4))

        email_input    = QLineEdit()
        email_input.setPlaceholderText("Email address")
        email_input.setPalette(necessary_field_pal)
        email_input.textEdited.connect(lambda text: self.text_edited(text, 5))

        phone_input    = QLineEdit()
        phone_input.setPlaceholderText("Phone number")
        phone_input.textEdited.connect(lambda text: self.text_edited(text, 6))

        wbs_bool_input = QCheckBox("I have a WBS (Wohnberechtigungsschein)")
        wbs_bool_input.setCheckState(Qt.Unchecked)
        wbs_bool_input.stateChanged.connect(self.show_wbs_conf_box)
        
        wbs_date_input = QDateEdit(calendarPopup=True)

        wbs_rooms_input= QSpinBox()
        wbs_rooms_input.setMinimum(1)
        wbs_rooms_input.setMaximum(100)

        filter_input   = QLineEdit()
        filter_input.setPlaceholderText("Keywords for filtering")
        filter_input.textEdited.connect(lambda text: self.text_edited(text, 10))

        wbs_num_select = QComboBox()
        wbs_num_select.addItems(["WBS 100", "WBS 140", "WBS 160", "WBS 180"])
        wbs_num_select.currentTextChanged.connect(lambda text: self.text_edited(text, 11))

        self.start_bot_btn = QPushButton("Start bot")
        self.start_bot_btn.clicked.connect(self.handle_start_stop_btn)
        self.start_bot_btn.setStyleSheet("background-color: rgb(128,242,159)")

        self.console_out   = QTextEdit(readOnly=True)
        self.console_out.setLineWrapMode(QTextEdit.NoWrap)


        # Sends the current index (position) of the selected item.
        #wbs_num_select.currentIndexChanged.connect( self.index_changed )

        # There is an alternate signal to send the text.
        #wbs_num_select.currentTextChanged.connect( self.text_changed )

        main                = QVBoxLayout()
        conf_box            = QHBoxLayout()
        console_box         = QHBoxLayout()
        conf_box_left       = QVBoxLayout()
        conf_box_right      = QVBoxLayout()
        zip_city_layout     = QHBoxLayout()
        phone_filter_layout = QHBoxLayout()
        wbs_date_pick_label = QHBoxLayout()
        wbs_rooms_label     = QHBoxLayout()

        self.wbs_conf_frame = QFrame()

        wbs_conf_box        = QHBoxLayout()
        wbs_conf_box_left   = QVBoxLayout()
        wbs_conf_box_right  = QVBoxLayout()

        conf_box_left.addWidget(firstname_input)
        conf_box_right.addWidget(street_input)
        conf_box_left.addWidget(lastname_input)
        zip_city_layout.addWidget(zip_code_input)
        zip_city_layout.addWidget(city_input)
        conf_box_right.addLayout(zip_city_layout)
        conf_box_left.addWidget(email_input)
        phone_filter_layout.addWidget(phone_input)
        phone_filter_layout.addWidget(filter_input)
        conf_box_right.addLayout(phone_filter_layout)
        conf_box_left.addWidget(wbs_bool_input)
        conf_box_right.addWidget(self.start_bot_btn)
        
        wbs_date_pick_label.addWidget(QLabel('WBS is valid until date:'))
        wbs_date_pick_label.addWidget(wbs_date_input)
        wbs_conf_box_left.addLayout(wbs_date_pick_label)
        wbs_conf_box_right.addWidget(wbs_num_select)
        
        wbs_rooms_label.addWidget(QLabel('WBS is valid for rooms:'))
        wbs_rooms_label.addWidget(wbs_rooms_input)
        wbs_conf_box_left.addLayout(wbs_rooms_label)

        #wbs_conf_box_right.addWidget(wbs_date_input)
        wbs_conf_box_right.addWidget(QLabel("              Hier könnte Ihre Werbung stehen!"))#.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter))
        wbs_conf_box.addLayout(wbs_conf_box_left)
        wbs_conf_box.addLayout(wbs_conf_box_right)
        self.wbs_conf_frame.setLayout(wbs_conf_box)
        self.wbs_conf_frame.hide()

        conf_box.addLayout(conf_box_left)
        conf_box.addLayout(conf_box_right)
        console_box.addWidget(self.console_out)
        main.addLayout(conf_box, 6)
        main.addWidget(self.wbs_conf_frame, 4)
        main.addWidget(QLabel(' Console output:'))
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