
from defs import core, process_input
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import os, sys
import pyperclip

def load_file(node_name, node_key, node_address):
    if not os.path.isdir("nodes"):
        print("Invalid File!")

    try:
        # Both are Encrypted in cSHAKE256
        node_name_bytes = process_input(node_name, node_address)
        node_key_bytes = process_input(node_key, node_address)
        
        with open(f"nodes/{node_name_bytes.hex()}", "r") as file:
            header = file.readline().split("\x01")
            if(core.debug):   
                print(f"Full Header: ({header})")
                # print(f"File Version: (${header[1]})")

            if header != core.header:
                raise ValueError("Invalid Header! The file read is not a CryptoDot file or the Header is corrupt!")

            # If the file_version is 1, use this to set nonce
            if header[1] == 1:
                file_nonce = header[1].replace("\n", "")

            # For loop to read the rest of the file
            file_content = ""
            for line in file.readline():
                #print(line)
                file_content += line

            try:
                node_signature = sys.argv[5]

            except IndexError:
                print("")

            if(core.debug):   
                print(f"NONCE: {file_nonce}")
                print(f"Encrypted Content: {file_content}")
                print(f"Signature: {node_signature}\n")

            cipher = AES.new(node_key_bytes, AES.MODE_GCM, nonce=b64decode(file_nonce))
            decrypted_node = cipher.decrypt(b64decode(file_content))

            pyperclip.copy(bytes.decode(decrypted_node))
            print("Ok! Decryption was a success! Contents copied to Clipboard.")

            if(node_signature != None):
                cipher.hexverify(node_signature)

            else:
                print("No Signature value was passed, therefore no check will be run.")

    except FileNotFoundError as error:
        print("Invalid Node! File does not exist!")