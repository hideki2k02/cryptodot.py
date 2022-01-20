from defs import core, process_input
from Crypto.Cipher import AES
from base64 import b64encode
import os
import pyperclip

def new_file(node_name, node_key, node_address):
    # Both are Encrypted in cSHAKE256
    node_name_bytes = process_input(node_name, node_address)
    node_key_bytes = process_input(node_key, node_address)

    clipboard = pyperclip.paste()
    
    if(core.debug):
        print("Node Name: ", node_name_bytes.hex())
        print("Node Key: ", node_key_bytes.hex())
        print(f"Clipboard: {clipboard}\n")

    if clipboard is None:
        print("You Clipboard is empty!")
        return

    cipher = AES.new(node_key_bytes, AES.MODE_GCM)
    node_content, node_signature = cipher.encrypt_and_digest(bytes(clipboard, "utf-8"))

    cipher_nonce = b64encode(cipher.nonce).decode("utf-8")
    cipher_text = b64encode(node_content).decode("utf-8")

    if not os.path.isdir("nodes"):
        os.mkdir("nodes")

    current_format_version = chr(0x01)

    file = open(f"nodes/{node_name_bytes.hex()}", "w")
    file.write(f"CRYPTODOT{core.empty_hex}{current_format_version}\n{cipher_nonce}\n{cipher_text}")
    file.close()

    print("Ok! Node was successfully created!")
    print(f"Unique Signature: {node_signature.hex()}")