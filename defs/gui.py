# PyQt5 GUI Layout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,  QHBoxLayout, QVBoxLayout, QWidget

# PyQt5 User Input
from PyQt5.QtWidgets import QLineEdit , QPushButton, QPlainTextEdit, QFileDialog, QInputDialog
from PyQt5.QtWidgets import QAction, QMenu, QCheckBox

# PyQt5 Fancy-Stuff
from PyQt5.QtGui import QIcon
from PyQt5 import QtMultimedia

# Node-Related
from defs.new_node import new_node, write_node_file
from defs.load_node import load_node, verify_node

# Defs
from defs import config, program_version, images_path, sounds_path
from defs.japa4551 import *

# Others
import sys


class Toolbar():
    def Create(widget):
        # Creates the Toolbar
        widget.toolbar = widget.addToolBar("Toolbar")
        widget.toolbar.setMovable(False)

    def AddAction(action_name, icon_path, action_on_triggered, window, start_enabled):
        # It looks cleaner i guess
        action = QAction(QIcon(icon_path), action_name, window)
        action.setEnabled(start_enabled)
        action.triggered.connect(action_on_triggered)
        window.toolbar.addAction(action)

        return action


class Button():
    def CreateLineEdit(button_name, action, destination_layout, return_layout=False):
        # Creates the Layout
        layout = QHBoxLayout()

        # Creates the Button Label and adds it to the button_layout
        label = QLabel(button_name)
        layout.addWidget(label)

        # Creates the LineEdit, defines it action (if possible) and adds it to the button_layout
        lineEdit = QLineEdit()

        if action != None:
            lineEdit.textEdited.connect(action)

        layout.addWidget(lineEdit)

        destination_layout.addLayout(layout)

        if return_layout:
            return lineEdit, layout

        else:
            return lineEdit

    def CreatePasswordInput(button_name, action, destination_layout, start_shown=False):
        def show_hide_password(boolean):
            if boolean:
                lineEdit.setEchoMode(QLineEdit.Normal)
                show_password_button.setIcon(QIcon(images_path + "hidden.png"))


            else: 
                lineEdit.setEchoMode(QLineEdit.Password)
                show_password_button.setIcon(QIcon(images_path + "eye.png"))


        lineEdit, lineEdit_layout = Button.CreateLineEdit(button_name, action, destination_layout, True)
        lineEdit.setEchoMode(QLineEdit.Password)

        # Creates the show_password_button and makes it a toggle button
        show_password_button = QPushButton()
        show_password_button.setCheckable(True)

        # Runs the show_hide_password check to set the icon
        show_hide_password(start_shown)

        # If the Button is Checked, Show/Hide the Password and Change the Button's icon
        show_password_button.clicked.connect(
            show_hide_password, show_password_button.isChecked()
        )

        show_password_button.setStyleSheet("""
            padding: 0;
            border: none;
            background: none;
        """)

        lineEdit_layout.addWidget(show_password_button)

        return lineEdit

class App_GUI(QMainWindow):
    def __init__(self):
        # I dont know what the fuck this does, but i guess its basically the Main() in C#
        
        # I've done my research and im starting to understand 
        # (TLDR still dont know what the fuck this does exactly)
        super().__init__()

        # Creates the Base Layout
        self.window = QWidget()
        self.base_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        # Creates the Toolbar and defines all Actions
        Toolbar.Create(self)

        # Save Node Button
        self.save_node_button = Toolbar.AddAction(
            "Save Node", (images_path + "save.png"), self.on_save_node_button_press,
            self, start_enabled=False
        )

        # Load Node Button
        self.load_node_button = Toolbar.AddAction(
            "Load Node", (images_path + "folder.png"), self.on_load_node_button_press,
            self, start_enabled=False
        )

        # Settings Button
        Toolbar.AddAction(
            "Settings", (images_path + "settings.png"), self.on_load_node_button_press,
            self, start_enabled=True
        )



        # Node Key LineEdit
        self.node_key_field = Button.CreatePasswordInput(
            "Node Key (Password)", self.validate_form, self.base_layout,
        )

        # Node Address LineEdit
        self.node_address_field = Button.CreatePasswordInput(
            "Node Address (Password)", self.validate_form, self.base_layout,
        )

        # Node Signature LineEdit
        self.node_signature_lineEdit = Button.CreatePasswordInput(
            "Node Signature", None, self.base_layout, start_shown=True
        )

        self.node_signature_lineEdit.setPlaceholderText("NONE")
        self.node_signature_lineEdit.setAlignment(Qt.AlignCenter)



        # Node Content Label (Node Address is an extra parameter for the Hashes)
        self.node_content_label = QLabel("Node Content")
        # self.base_layout.addWidget(self.node_content_label)

        # Node Content Text Box
        self.node_content_textEdit = QPlainTextEdit()
        # self.base_layout.addWidget(self.node_content_textEdit)

        # Verify Button and its Events
        self.verify_node_button = QPushButton("Verify Signature")
        self.verify_node_button.setEnabled(False)
        # self.verify_node_button.clicked.connect(self.on_clear_content_button_press)
        self.buttons_layout.addWidget(self.verify_node_button)

        # Clear Button and its Events
        self.clear_content_button = QPushButton("Clear Content")
        self.clear_content_button.clicked.connect(self.on_clear_content_button_press)
        self.buttons_layout.addWidget(self.clear_content_button)
        
        # Set the Layout Alignment
        self.base_layout.setAlignment(Qt.AlignTop)

        # This will add the button_layout below the base_layout
        self.base_layout.addLayout(self.buttons_layout)
        self.window.setLayout(self.base_layout)
        self.setCentralWidget(self.window)

        # Sets the Window info, like minimum size, title and icon; Then displays it.
        self.resize(500, 500)
        self.setMinimumSize(325, 300)
        self.setWindowTitle(f"CryptoDot.py - Version {program_version}")
        self.setWindowIcon(QIcon(images_path + 'cryptography.png'))

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

                QtMultimedia.QSound.play(sounds_path + "success_bell-6776.wav")                

                if node_signature == None:
                        # QInputDialog.getText() returns a "string" and a "boolean", we only want the "string" for now
                        node_signature = QInputDialog.getText(self, "Insert the File Signature:", "File Signature:")[0]

                print_debug(f"Passed Node Signature: {node_signature}")
                verify_node(cipher_object, node_signature)

                self.node_content_textEdit.setPlainText(decrypted_node)

            # In case it fails (probably invalid key)
            except:
                QtMultimedia.QSound.play(sounds_path + "mixkit-electric-buzz-glitch-2594.wav")
                return

        else:
            print_debug("Node Loading Cancelled!")

    def on_clear_content_button_press(self):
        print_debug("Clear Button pressed! clearing Node Content...")

        self.node_content_textEdit.clear()

    def validate_form(self):
        valid_key = len(self.node_key_field.text()) >= 3
        valid_address = len(self.node_address_field.text()) >= 3

        self.save_node_button.setEnabled(valid_key and valid_address)
        self.load_node_button.setEnabled(valid_key and valid_address)

def initialize_gui():
    app = QApplication(sys.argv)
    keep_window_open = App_GUI()

    sys.exit(app.exec_())
