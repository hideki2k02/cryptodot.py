import sys
#from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel, QLineEdit, QMainWindow, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class App_GUI(QMainWindow):
    def __init__(self):
        # I dont know what the fuck this does, but i guess its basically the Main() in C#
        super().__init__()

        self.window = QWidget()
        self.inputs_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.inputs_layout.setAlignment(Qt.AlignTop)

        # Node Address LineEdit, Label and its events (Node Address is the Hash)
        self.node_address_label = QLabel("Node Address (Salt Hash)")
        self.node_address = QLineEdit()
        self.inputs_layout.addWidget(self.node_address_label)
        self.inputs_layout.addWidget(self.node_address)
        self.node_address.editingFinished.connect(self.validate_form)

        # Node Key LineEdit, Label and its events (Node Key is the Password)
        self.node_key_label = QLabel("Node Key (Password)")
        self.node_key = QLineEdit()
        self.node_key.setEchoMode(QLineEdit.Password)
        self.inputs_layout.addWidget(self.node_key_label)
        self.inputs_layout.addWidget(self.node_key)
        self.node_key.editingFinished.connect(self.validate_form)

        # Save Button and its Events
        self.save_file_button = QPushButton("Save File")
        self.save_file_button.clicked.connect(self.on_save_file_button_press)
        self.buttons_layout.addWidget(self.save_file_button)
        
        # Load Button and its Events
        self.load_file_button = QPushButton("Load File")
        self.load_file_button.setEnabled(False)
        self.load_file_button.clicked.connect(self.on_load_file_button_press)
        self.buttons_layout.addWidget(self.load_file_button)
        
        # This will add the button_layout below the inputs_layout
        self.inputs_layout.addLayout(self.buttons_layout)
        self.window.setLayout(self.inputs_layout)

        self.resize(500, 500)
        self.setMinimumSize(300, 300)
        self.setWindowTitle(f'CryptoDot Vampyre {vampyre.vampyre_version}')
        self.setWindowIcon(QIcon('data/icons8-virus-free-50.png'))
        self.setCentralWidget(self.window)
        
        self.show()

    def validate_form(self):
        address_valid = len(self.node_address.text()) > 1
        key_valid = len(self.node_key.text()) > 1
        is_valid = address_valid and key_valid

        self.load_file_button.setEnabled(is_valid)
    
    # Self must be included on those below, else it crashes (?)
    def on_save_file_button_press(self):
        print("Save File Button was pressed! Opening File Dialog...")

        QFileDialog.getSaveFileName()

    def on_load_file_button_press(self):
        print("Load File Button was pressed! Opening File Dialog...")

        file = QFileDialog.getOpenFileName()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    keep_window_open = App_GUI()

    sys.exit(app.exec_())
