# PyQt5 GUI Layout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,  QHBoxLayout, QVBoxLayout, QWidget

# PyQt5 User Input
from PyQt5.QtWidgets import QLineEdit , QPushButton, QPlainTextEdit, QFileDialog
from PyQt5.QtWidgets import QAction

# PyQt5 Fancy-Stuff
from PyQt5.QtGui import QIcon

# GUI Actions
from defs.gui_actions import *

# Node-Related
from defs.new_node import new_node, write_node_file
from defs.load_node import load_node

# Defs
from defs import config, program_version, images_path
from defs.japa4551 import *

# Others
from functools import partial
import sys


class Toolbar():
    def Create(widget):
        # Creates the Toolbar
        widget.toolbar = widget.addToolBar("Toolbar")
        widget.toolbar.setMovable(False)

    def AddAction(action_name, icon_path, on_triggered, window, start_enabled):
        # It looks cleaner i guess
        action = QAction(QIcon(icon_path), action_name, window)
        action.setEnabled(start_enabled)

        if on_triggered != None:
            action.triggered.connect(on_triggered)
            
        window.toolbar.addAction(action)

        return action


class Inputs():
    def CreateButton(input_name, action, destionation_layout, start_enabled=True):
        # Creates the layout
        layout = QVBoxLayout()

        # Creates the button, check if its enabled, sets its action and adds it to the layout
        button = QPushButton(input_name)
        button.setEnabled(start_enabled)

        if action != None:
            button.clicked.connect(action)

        layout.addWidget(button)
        destionation_layout.addLayout(layout)

        return button


    def CreateTextEdit(input_name, action, destination_layout):
        # Creates the layout
        layout = QVBoxLayout()

        # Creates the Label and adds it to the layout
        label = QLabel(input_name)
        layout.addWidget(label)

        # Creates the TextEdit, defines it action (if possible) and adds it to the button_layout
        textEdit = QPlainTextEdit()

        if action != None:
            textEdit.textEdited.connect(action)

        layout.addWidget(textEdit)
        destination_layout.addLayout(layout)
        
        return textEdit


    def CreateLineEdit(input_name, action, destination_layout, return_layout=False):
        # Creates the Layout
        layout = QHBoxLayout()

        # Creates the Label and adds it to the layout
        label = QLabel(input_name)
        layout.addWidget(label)

        # Creates the LineEdit, defines it action (if possible) and adds it to the button_layout
        lineEdit = QLineEdit()

        if action != None:
            lineEdit.textChanged.connect(action)

        layout.addWidget(lineEdit)

        destination_layout.addLayout(layout)

        if return_layout:
            return lineEdit, layout

        else:
            return lineEdit

    def CreatePasswordInput(input_name, action, destination_layout, start_shown=False):
        def show_hide_password(boolean):
            if boolean:
                lineEdit.setEchoMode(QLineEdit.Normal)
                show_password_button.setIcon(QIcon(images_path + "hidden.png"))


            else: 
                lineEdit.setEchoMode(QLineEdit.Password)
                show_password_button.setIcon(QIcon(images_path + "eye.png"))


        lineEdit, lineEdit_layout = Inputs.CreateLineEdit(input_name, action, destination_layout, True)

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

        # Creates the Toolbar and defines all Actions
        Toolbar.Create(self)

        # Note to future self: partial() is the only way to pass arguments 
        # to a function in .connect(event), you cant just .connect(foo(bar))

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
            "Settings", (images_path + "settings.png"), None,
            self, start_enabled=True
        )



        # Node Key (Key used to make the AES Cipher)
        self.node_key_field = Inputs.CreatePasswordInput(
            "Node Key (Password)", partial(validate_forms, self), self.base_layout,
        )

        # Node Address (Extra parameter for the Hashes)
        self.node_address_field = Inputs.CreatePasswordInput(
            "Node Address (Salt)", partial(validate_forms, self), self.base_layout,
        )

        # Node Signature (Signature for the AES Cipher, Check if it was not tampered)
        self.node_signature_field = Inputs.CreatePasswordInput(
            "Node Signature", partial(is_node_loaded, self), self.base_layout, 
            start_shown=True
        )

        self.node_signature_field.setPlaceholderText("NONE")
        self.node_signature_field.setAlignment(Qt.AlignCenter)

        # Node Content
        self.node_content_field = Inputs.CreateTextEdit(
            "Node Content", None, self.base_layout
        )



        # Verify Signature Button
        self.verify_signature_button = Inputs.CreateButton(
            "Verify Signature", partial(verify_node_signature_button_pressed, self), self.base_layout,
            start_enabled=False
        )

        # Clear Button
        Inputs.CreateButton(
            "Clear Everything", partial(clear_button_pressed, self), self.base_layout, 
            start_enabled=True
        )

        # Sets the Window layout and info (like minimum size, title and icon) Then displays it.
        self.window.setLayout(self.base_layout)
        self.setCentralWidget(self.window)

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
            self.node_key_field.text(), 
            self.node_key_field.text(), 
            self.node_content_field.toPlainText()
        )

        node_path = QFileDialog.getSaveFileName(self, "ITS NOT RECOMMENDED TO CHANGE THE FILE NAME", 
            f"nodes/{node_name_bytes}"
        )

        if node_path[0] != "":
            write_node_file(node_path[0], cipher_nonce, cipher_text, cipher_signature, False)

            PlaySound.Success()
            self.node_signature_field.setText(cipher_signature)


        else:
            print_debug("Node Creation Cancelled!")

    def on_load_node_button_press(self):
        print_debug("Load File Button was pressed! Opening File Dialog...")

        node_path = QFileDialog.getOpenFileName(self, "Select the Node File you want to open", "nodes")

        if node_path[0] != "":
            print_debug(f"Passed Node Path: {node_path[0]}")

            try:
                decrypted_node, node_signature, self.current_cipher_object = load_node(
                None, # Would be node_name if it was CLI Mode
                self.node_key_field.text(), 
                self.node_address_field.text(), 
                None, # Would be node_signature if it was CLI Mode
                node_path[0]
                )

                print_debug(f"Node Signature on File: {node_signature}")

                PlaySound.Success()

                self.node_signature_field.setText(node_signature)
                self.node_content_field.setPlainText(decrypted_node)

            # In case it fails (probably invalid key)
            except:
                PlaySound.Failed()

        else:
            print_debug("Node Loading Cancelled!")


def initialize_gui():
    app = QApplication(sys.argv)
    keep_window_open = App_GUI()

    sys.exit(app.exec_())
