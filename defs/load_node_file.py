
from defs import core, process_input
from Crypto.Cipher import AES
from base64 import b64decode
import sys
import binascii

def load_file(node_name, node_key, node_address = "", node_signature = "", node_path = ""):
    try:
        node_key_bytes = process_input(node_key, node_address)

        if node_path == "":
            node_path = f"nodes/{node_name}"
        
        with open(node_path, "r") as file:
            header = file.readline(9)
            file_version = bytes(file.readline().replace("\n", ""), "utf-8").hex()
            file_nonce = ""
            
            if(core.debug):   
                print(f"Header: {header}")
                print(f"File Version: {file_version}")

            if header != core.header:
                raise ValueError("Invalid Header! The file read is not a CryptoDot file or the Header is invalid/corrupt!")

            # Set the nonce based on the file_version
            match file_version:
                case "01":
                    file_nonce = file.readline().replace("\n", "")

                    # print("File version: 1")

                case _:
                    raise ValueError("Invalid File Version!")

            # For loop to read the rest of the file
            file_content = ""
            for line in file.readline():
                #print(line)
                file_content += line

            if len(node_signature) == 0:
                empty_signature = "No Signature value was passed, therefore no check will be run.\n"

                if(core.debug):
                    print("Current Node Signature is Empty!")
                    print(f"Sys.argv4 Length: {len(sys.argv[4])}")

                try:
                    if len(sys.argv[4]) > 0:
                        node_signature = sys.argv[4]

                    else: 
                        print(empty_signature)

                except IndexError:
                    print(empty_signature)

            if(core.debug):   
                print(f"NONCE: {file_nonce}")
                print(f"Encrypted Content: {file_content}")
                print(f"Signature: {node_signature}\n")

            try:
                cipher = AES.new(node_key_bytes, AES.MODE_GCM, nonce=b64decode(file_nonce))
                decrypted_node = cipher.decrypt(b64decode(file_content))
                node_content = bytes.decode(decrypted_node)

                print("Ok! Node was successfully decrypted!")

                if(len(node_signature) > 0):
                    try:
                        print("\nChecking File Signature... ", end="")

                        cipher.hexverify(node_signature)
                        
                        print("Ok! Signature is valid!")

                    except binascii.Error:
                        print("Signature Check Failed: Invalid Hash!")

                    except ValueError:
                            print("Signature Check Failed: Wrong Hash!")

                return node_content

            except (ValueError, KeyError):
                print("Decryption Failed: Invalid Key!")

    except FileNotFoundError as error:
        print("Invalid Node! File does not exist!")