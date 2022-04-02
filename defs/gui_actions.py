# Sounds
from defs.gui_sounds import *

# Node-Related
from defs.load_node import verify_node

# Defs
from defs.japa4551 import *


def validate_forms(self):
    valid_key = len(self.node_key_field.text()) >= 3
    valid_address = len(self.node_address_field.text()) >= 3

    self.save_node_button.setEnabled(valid_key and valid_address)
    self.load_node_button.setEnabled(valid_key and valid_address)


def is_node_loaded(self):
    # If a node is loaded and the node_signature Field is at least 3
    # Enables the Verify Signature Button

    try:
        valid_signature = len(self.node_key_field.text()) >= 3
        valid_cipher_object = self.current_cipher_object != None

        self.verify_signature_button.setEnabled(valid_signature and valid_cipher_object)

    except:
        # Does abso-fucking-lutely nothing
        None


def clear_button_pressed(self):
    print_debug("Clear Button pressed! Clearing Sensitive Data...")

    self.node_key_field.clear()
    self.node_address_field.clear()
    self.node_signature_field.clear()
    self.node_content_field.clear()
    self.current_cipher_object = None


def verify_node_signature_button_pressed(self):
    is_node_valid = verify_node(self.current_cipher_object, self.node_signature_field.text()),

    if is_node_valid:
        PlaySound.Success()

    else:
        PlaySound.Failed()