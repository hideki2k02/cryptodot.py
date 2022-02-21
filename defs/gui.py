# PyQT5 GUI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,  QHBoxLayout, QVBoxLayout, QWidget
# from PyQt5.QtGui import QIcon

# PyQT5 User Input
from PyQt5.QtWidgets import QFileDialog, QLineEdit , QPushButton, QPlainTextEdit, QInputDialog

# New File and Load File Functions
from defs.new_node import new_node, write_node_file
from defs.load_node import load_node

# Others
from defs import config, program_version
from japa4551 import *
import sys


class App_GUI(QMainWindow):
    def __init__(self):
        # I dont know what the fuck this does, but i guess its basically the Main() in C#
        super().__init__()

        # print(program_config)

        self.window = QWidget()
        self.inputs_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.inputs_layout.setAlignment(Qt.AlignTop)

        # Node Key LineEdit, Label and its events (Node Key is the Password)
        self.node_key_label = QLabel("Node Key (Password)")
        self.node_key = QLineEdit()
        self.node_key.setEchoMode(QLineEdit.Password)
        self.inputs_layout.addWidget(self.node_key_label)
        self.inputs_layout.addWidget(self.node_key)
        self.node_key.textEdited.connect(self.validate_form)

        # Node Address LineEdit, Label and its events (Node Address is an extra parameter for the Hashes)
        self.node_address_label = QLabel("Node Address (Hash Modifier)")
        self.node_address = QLineEdit()
        self.node_address.setEchoMode(QLineEdit.Password)
        self.inputs_layout.addWidget(self.node_address_label)
        self.inputs_layout.addWidget(self.node_address)
        self.node_address.textEdited.connect(self.validate_form)

        # Node Content LineEdit, Label (Node Address is an extra parameter for the Hashes)
        self.node_content_label = QLabel("Node Content")
        self.node_content = QPlainTextEdit()
        self.inputs_layout.addWidget(self.node_content_label)
        self.inputs_layout.addWidget(self.node_content)

        # Save Button and its Events
        self.save_file_button = QPushButton("Save File")
        self.save_file_button.setEnabled(False)
        self.save_file_button.clicked.connect(self.on_save_file_button_press)
        self.buttons_layout.addWidget(self.save_file_button)
        
        # Load Button and its Events
        self.load_file_button = QPushButton("Load File")
        self.load_file_button.setEnabled(False)
        self.load_file_button.clicked.connect(self.on_load_file_button_press)
        self.buttons_layout.addWidget(self.load_file_button)

        # Clear Button and its Events
        self.clear_content_button = QPushButton("Clear")
        self.clear_content_button.setEnabled(True)
        self.clear_content_button.clicked.connect(self.on_clear_content_button_press)
        self.buttons_layout.addWidget(self.clear_content_button)
        
        # This will add the button_layout below the inputs_layout
        self.inputs_layout.addLayout(self.buttons_layout)
        self.window.setLayout(self.inputs_layout)
        self.setCentralWidget(self.window)

        # Sets the Window info, like minimum size, title and icon; Then displays it.
        self.resize(500, 500)
        self.setMinimumSize(300, 300)
        self.setWindowTitle(f"CryptoDot.py - Version {program_version}")
        # self.setWindowIcon(QIcon('data/icons8-virus-free-50.png'))

        # Checks if the boolean "dark_mode" is true, if so use the "dark theme"
        if config["user"]["dark_mode"]:
            self.setStyleSheet("""
                QWidget {
                    background-color: #616161;
                }

                QPushButton { 
                    background: yellow; 
                    color: yellow;
                }
            """)
        
        self.show()

    def validate_form(self):
        valid_key = len(self.node_key.text()) >= 3
        valid_address = len(self.node_address.text()) >= 3

        self.save_file_button.setEnabled(valid_key and valid_address)
        self.load_file_button.setEnabled(valid_key and valid_address)
        
    # Self must be included on those below, else it crashes (?)
    def on_save_file_button_press(self):
        print_debug("Save File Button was pressed! Opening File Dialog...")

        node_name_bytes, cipher_nonce, cipher_text, cipher_signature = new_node(None, 
            self.node_key.text(), 
            self.node_address.text(), 
            self.node_content.toPlainText()
        )

        node_path = QFileDialog.getSaveFileName(self, "ITS NOT RECOMMENDED TO CHANGE THE FILE NAME", 
            f"nodes/{node_name_bytes}"
        )

        if node_path[0] != "":
            write_node_file(node_path[0], cipher_nonce, cipher_text, cipher_signature, False)

        else:
            print_debug("Node Creation Cancelled!")

    def on_load_file_button_press(self):
        print_debug("Load File Button was pressed! Opening File Dialog...")

        node_path = QFileDialog.getOpenFileName(self, "Select the Node File you want to open", "nodes")

        if node_path[0] != "":
            node_signature = QInputDialog.getText(self, "Insert the File Signature:", "File Signature:")
            
            decrypted_node = load_node(None, 
                self.node_key.text(), 
                self.node_address.text(), 
                node_signature[0], 
                node_path[0]
            )

            self.node_content.setPlainText(decrypted_node)

    def on_clear_content_button_press(self):
        print_debug("Clear Button pressed! clearing Node Content...")

        self.node_content.clear()

def gui():
    app = QApplication(sys.argv)
    keep_window_open = App_GUI()

    sys.exit(app.exec_())
