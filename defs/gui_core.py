# PyQt5 GUI Layout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,  QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon

# PyQt5 User Input
from PyQt5.QtWidgets import QLineEdit , QPushButton, QPlainTextEdit, QFileDialog, QInputDialog
from PyQt5.QtWidgets import QAction

# Node-Related
from defs.new_node import new_node, write_node_file
from defs.load_node import load_node, verify_node

# Defs
from defs import config, program_version
from defs.japa4551 import *

# Others
import sys


class App_GUI(QMainWindow):
    def __init__(self):
        # I dont know what the fuck this does, but i guess its basically the Main() in C#
        super().__init__()

        # print(program_config)

        # Creates the Base Layout
        self.window = QWidget()
        self.base_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        # Creates the Toolbar
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)

        # Save Node Button
        self.save_node_button = QAction(QIcon("./defs/gui/icons/save.png"), "Save Node", self)
        self.save_node_button.setEnabled(False)
        self.save_node_button.triggered.connect(self.on_save_node_button_press)

        # Load Node Button
        self.load_node_button = QAction(QIcon("./defs/gui/icons/folder.png"), "Load Node", self)
        self.load_node_button.setEnabled(False)
        self.load_node_button.triggered.connect(self.on_load_node_button_press)

        # Settings Button
        self.settings_button = QAction(QIcon("./defs/gui/icons/settings.png"), "Load Node", self)
        self.settings_button.setEnabled(True)
        # options_button.triggered.connect(buttons_action.on_save_node_button_pressed)

        self.toolbar.addAction(self.save_node_button)
        self.toolbar.addAction(self.load_node_button)
        self.toolbar.addAction(self.settings_button)

        # Set the Layout Alignment
        self.base_layout.setAlignment(Qt.AlignTop)

        # Node Key Label (Node Key is the Password)
        self.node_key_label = QLabel("Node Key (Password)")
        self.base_layout.addWidget(self.node_key_label)

        # Node Key LineEdit and its events
        self.node_key_lineEdit = QLineEdit()
        self.node_key_lineEdit.setEchoMode(QLineEdit.Password)
        self.node_key_lineEdit.textEdited.connect(self.validate_form)
        self.base_layout.addWidget(self.node_key_lineEdit)

        # Node Address Label (Node Address is an extra parameter for the Hashes)
        self.node_address_label = QLabel("Node Address (Hash Modifier)")
        self.base_layout.addWidget(self.node_address_label)

        # Node Address LineEdit and its events
        self.node_address_lineEdit = QLineEdit()
        self.node_address_lineEdit.setEchoMode(QLineEdit.Password)
        self.node_address_lineEdit.textEdited.connect(self.validate_form)
        self.base_layout.addWidget(self.node_address_lineEdit)

        # Node Signatire Label (Node Signature is used mainly to verify the File Authenticity)
        self.node_signature_label = QLabel("Node Signature")
        self.base_layout.addWidget(self.node_signature_label)

        # Node Signature LineEdit
        self.node_signature_lineEdit = QLineEdit()
        self.node_signature_lineEdit.setReadOnly(True)
        self.node_signature_lineEdit.setText("NONE")
        self.node_signature_lineEdit.setAlignment(Qt.AlignCenter)
        self.base_layout.addWidget(self.node_signature_lineEdit)

        # Node Content Label (Node Address is an extra parameter for the Hashes)
        self.node_content_label = QLabel("Node Content")
        self.base_layout.addWidget(self.node_content_label)

        # Node Content Text Box
        self.node_content_textEdit = QPlainTextEdit()
        self.base_layout.addWidget(self.node_content_textEdit)

        # Verify Button and its Events
        self.verify_node_button = QPushButton("Verify Signature")
        self.verify_node_button.setEnabled(False)
        # self.verify_node_button.clicked.connect(self.on_clear_content_button_press)
        self.buttons_layout.addWidget(self.verify_node_button)

        # Clear Button and its Events
        self.clear_content_button = QPushButton("Clear")
        self.clear_content_button.setEnabled(False)
        self.clear_content_button.clicked.connect(self.on_clear_content_button_press)
        self.buttons_layout.addWidget(self.clear_content_button)
        
        # This will add the button_layout below the base_layout
        self.base_layout.addLayout(self.buttons_layout)
        self.window.setLayout(self.base_layout)
        self.setCentralWidget(self.window)

        # Sets the Window info, like minimum size, title and icon; Then displays it.
        self.resize(500, 500)
        self.setMinimumSize(325, 300)
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

    def on_save_node_button_press(self):
     print_debug("Save File Button was pressed! Opening File Dialog...")

     node_name_bytes, cipher_nonce, cipher_text, cipher_signature = new_node(None, 
          self.node_key_lineEdit.text(), 
          self.node_address_lineEdit.text(), 
          self.node_content_textEdit.toPlainText()
     )

     node_path = QFileDialog.getSaveFileName(self, "ITS NOT RECOMMENDED TO CHANGE THE FILE NAME", 
          f"nodes/{node_name_bytes}"
     )

     if node_path[0] != "":
          write_node_file(node_path[0], cipher_nonce, cipher_text, cipher_signature, False)

     else:
          print_debug("Node Creation Cancelled!")

    def on_load_node_button_press(self):
        print_debug("Load File Button was pressed! Opening File Dialog...")

        node_path = QFileDialog.getOpenFileName(self, "Select the Node File you want to open", "nodes")

        if node_path[0] != "":
            print_debug(f"Passed Node Path: {node_path[0]}")

            try:
                decrypted_node, node_signature, cipher_object = load_node(
                None, # Would be node_name if it was CLI Mode
                self.node_key_lineEdit.text(), 
                self.node_address_lineEdit.text(), 
                None, # Would be node_signature if it was CLI Mode
                node_path[0]
                )

                print_debug(f"Node Signature on File: {node_signature}")                

                if node_signature == None:
                        # QInputDialog.getText() returns a "string" and a "boolean", we only want the "string" for now
                        node_signature = QInputDialog.getText(self, "Insert the File Signature:", "File Signature:")[0]

                print_debug(f"Passed Node Signature: {node_signature}")
                verify_node(cipher_object, node_signature)

                self.node_content_textEdit.setPlainText(decrypted_node)

            # In case it fails (probably invalid key)
            except:
                return

        else:
            print_debug("Node Loading Cancelled!")

    def on_clear_content_button_press(self):
        print_debug("Clear Button pressed! clearing Node Content...")

        self.node_content_textEdit.clear()

    def validate_form(self):
        valid_key = len(self.node_key_lineEdit.text()) >= 3
        valid_address = len(self.node_address_lineEdit.text()) >= 3

        self.save_node_button.setEnabled(valid_key and valid_address)
        self.load_node_button.setEnabled(valid_key and valid_address)

def initialize_gui():
    app = QApplication(sys.argv)
    keep_window_open = App_GUI()

    sys.exit(app.exec_())
