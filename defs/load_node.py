# Defs
from defs import config
from defs.process_input import process_input
from defs.japa4551 import *

# Cryptography Related
from Crypto.Cipher import AES
from base64 import b64decode

# Others
import binascii

def load_node(node_name, node_key, node_address = "", node_signature = "NONE", node_path = ""):
    try:
        node_key_bytes = process_input(node_key, node_address)

        if node_path == "":
            node_path = f"nodes/{node_name}"

        print_debug(f"Trying to Opening {node_path}")
        
        with open(node_path, "r") as file:
            header = file.readline(9)
            file_version = bytes(file.readline().replace("\n", ""), "utf-8").hex()
            file_nonce = ""
              
            print_debug(f"Header: {header}", False)
            print_debug(f"File Version: {file_version}")

            if header != config["dev"]["format_header"]:
                raise ValueError("Invalid Header! The file read is not a CryptoDot file or the Header is invalid/corrupt!")

            # Set the nonce based on the file_version
            match file_version:
                case "01":
                    file_nonce = file.readline().replace("\n", "")

                    # print("File version: 1")

                case "02":
                    node_signature = file.readline().replace("\n", "")
                    file_nonce = file.readline().replace("\n", "")

                case _:
                    raise ValueError("Invalid File Version!")

            # For loop to read the rest of the file
            file_content = ""
            for line in file.readline():
                #print(line)
                file_content += line

            print_debug(f"NONCE: {file_nonce}", False)
            print_debug(f"Encrypted Content: {file_content}", False)

            try:
                cipher = AES.new(node_key_bytes, AES.MODE_GCM, nonce=b64decode(file_nonce))
                decrypted_node = cipher.decrypt(b64decode(file_content))
                node_content = bytes.decode(decrypted_node)

                print("Ok! Node was successfully decrypted!\n")

                return node_content, node_signature, cipher

            except (ValueError, KeyError):
                print("Decryption Failed: Invalid Key!")

    except FileNotFoundError as error:
        print("Invalid Node! File does not exist!")

def verify_node(cipher, signature):
    try:
        print("Checking File Signature... ", end="")

        cipher.hexverify(signature)
        
        print("Ok! Signature is valid!")

        return True

    except binascii.Error:
        print("Signature Check Failed: Invalid Hash!")

    except ValueError:
            print("Signature Check Failed: Wrong Hash!")