from defs import config
from defs.verify_input import verify_input

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
import pyperclip
import os

current_format_version = chr(0x01)

def new_node(node_name, node_key, node_address, node_content = pyperclip.paste()):
    # Hash is in cSHAKE256
    node_key_bytes = verify_input(node_key, node_address)

    # If Nodes folder does not exist, create one
    if not os.path.isdir("nodes"):
        os.mkdir("nodes")

    # Generates a random cSHAKE256 hash if no node_name parameter was received
    if node_name == None:
        random_hash = verify_input(f"{get_random_bytes(16)}", f"{get_random_bytes(16)}")
        node_name = random_hash.hex()

    if node_content == None:
        print("Your Node Content/Clipboard is empty!")
        return
    
    if(config["dev"]["debug"]):
        print("Node Key: ", node_key_bytes.hex())
        print("Node Name: ", node_name)
        print(f"Node Content: {node_content}\n")

    print("Generating Cipher... ", end="")

    cipher = AES.new(node_key_bytes, AES.MODE_GCM)
    encrypted_content, node_signature = cipher.encrypt_and_digest(bytes(node_content, "utf-8"))

    # Converts the encrypted_content from Raw Bytes to UTF-8
    cipher_nonce = b64encode(cipher.nonce).decode("utf-8")
    cipher_text = b64encode(encrypted_content).decode("utf-8")

    print(f"AES Cipher Generated! Unique Signature: {node_signature.hex()}")

    return node_name, cipher_nonce, cipher_text



def write_node_file(node_file_path, cipher_nonce, cipher_text, cli_overwrite_warning):
    if(config["dev"]["debug"]):
        print(f"\nFile Path Passed to write_file: {node_file_path}")

    if cli_overwrite_warning:
        if os.path.exists(node_file_path):
            print("\nA Node with that name already exists! Are you sure you want to overwrite it? Type YES to confirm.")
            
            if input("Confirmation: ") != "YES":
                print("\nNode Creation cancelled!")
                return

            # Small workaround ^^'
            print("")

    file = open(node_file_path, "w")
    file.write(f"CRYPTODOT{current_format_version}\n{cipher_nonce}\n{cipher_text}")
    file.close()

    print("Node Created!")