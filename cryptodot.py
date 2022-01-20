from defs.new_file import new_file
from defs.load_file import load_file
import sys

if __name__ == "__main__":
    def help_message():
        print("Usage: cryptodot.py [operation] [node_name] [node_key] [node_address] [node_signature]\n")

        print("""operation: The operation that will be done. Currently either "encrypt" or "decrypt".""")
        print("node_name: Original File Name.")
        print("node_key: The Password for the file.")
        print("node_address: Additional parameter to make the hashes stronger.")
        print("node_signature: Hash to verify the File's Integrity. Not necessary for Encryption.")

    try:
        operation = sys.argv[1]

        match operation:
            case "encrypt" | "decrypt":
                node_name = sys.argv[2]
                node_address = sys.argv[3]
                node_key = sys.argv[4]

                if(operation == "encrypt"):
                    print("Operation: Encrypt New Node\n")
                    new_file(node_name, node_key, node_address)
                
                else:
                    print("Operation: Decrypt Node\n")
                    load_file(node_name, node_key, node_address)

            case "gui":
                print("Opening GUI...")

                # gui()

            case "help":
                print("CryptoDot.py 1.0 by kodachi41.\n")
                help_message()

            case _:
                print("Invalid Operation! See the command below for correct usage:\n")
                help_message()

    except IndexError as error:
        print("None of the parameters must be empty!")