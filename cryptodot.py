# Node-Related
from defs.new_node import new_node, write_node_file
from defs.load_node import load_node

# GUI
from defs.gui import initialize_gui

# Others
import pyperclip
import sys

if __name__ == "__main__":
    def help_message():
        print("Usage: cryptodot.py [operation] [node_key] [node_address] [node_signature]\n")

        print("""operation: The operation that will be done. Currently either "encrypt" or "decrypt".""")
        print("node_key: The Password for the file.")
        print("node_address: Additional parameter that make the hashes stronger.")
        print("node_signature: Hash to verify the File's Integrity. Not necessary for Encryption.")

    try:
        operation = sys.argv[1]

        match operation:
            case "gui":
                print("Opening GUI...\n")
                initialize_gui()

            case "help":
                print("CryptoDot.py 1.0 by kodachi41.\n")
                help_message()

            case "encrypt" | "decrypt":
                node_key = sys.argv[2]
                node_address = sys.argv[3]
                input_node_name = input("Node Name: ")

                if(operation == "encrypt"):
                    print("\nOperation: Encrypt New Node\n")
                    node_name, cipher_nonce, cipher_text = new_node(input_node_name, node_key, node_address)

                    write_node_file(f"nodes/{node_name}", cipher_nonce, cipher_text, True)
            
                else:
                    node_signature = sys.argv[4]

                    print("\nOperation: Decrypt Node\n")
                    decrypted_node = load_node(input_node_name, node_key, node_address)

                    pyperclip.copy(decrypted_node)
                    print("Ok! Contents copied to Clipboard.")

            case _:
                print("Invalid Operation! See the command below for correct usage:\n")
                help_message()

    except IndexError as error:
        print("None of the parameters must be empty!")