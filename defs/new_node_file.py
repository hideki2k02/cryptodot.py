from defs import core, process_input
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
import pyperclip
import os

current_format_version = chr(0x01)

def new_file(node_name, node_key, node_address, node_content = pyperclip.paste()):
    if not os.path.isdir("nodes"):
        os.mkdir("nodes")

    # Hash is in cSHAKE256
    node_key_bytes = process_input(node_key, node_address)

    if node_name == None:
        node_name = process_input(f"{get_random_bytes(16)}", f"{get_random_bytes(16)}")

    if node_content == None:
        print("Your Node Content/Clipboard is empty!")
        return
    
    if(core.debug):
        print("Node Key: ", node_key_bytes.hex())
        print("Node Name: ", node_name)
        print(f"Node Content: {node_content}\n")

    cipher = AES.new(node_key_bytes, AES.MODE_GCM)
    encrypted_content, node_signature = cipher.encrypt_and_digest(bytes(node_content, "utf-8"))

    # Converts the encrypted_content from Raw Bytes to UTF-8
    cipher_nonce = b64encode(cipher.nonce).decode("utf-8")
    cipher_text = b64encode(encrypted_content).decode("utf-8")

    print(f"AES Cipher Generated! Unique Signature: {node_signature.hex()}")

    return node_name.hex(), cipher_nonce, cipher_text



def write_file(node_file_path, cipher_nonce, cipher_text):
    if(core.debug):
        print(f"\nFile Path Passed to write_file: {node_file_path}")

    file = open(node_file_path, "w")
    file.write(f"CRYPTODOT{current_format_version}\n{cipher_nonce}\n{cipher_text}")
    file.close()