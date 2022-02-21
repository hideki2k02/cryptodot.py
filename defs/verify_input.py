from Crypto.Hash import cSHAKE256
from defs import config

def verify_input(input_data, modifier):
    minimum_required_lenght = len(input_data) >= 3 and len(modifier) >= 3

    if minimum_required_lenght: 
        # If the required length is met, Turn Input into a cSHAKE256 Hash
        input_hash = cSHAKE256.new(bytes(input_data, "utf-8"))

        # Update Input's Hash with a modifier (Normally the address)
        input_hash.update(bytes(modifier, "utf-8"))

        if(config["dev"]["debug"]):
            print(f"Minimum Required Length reached! Processed Input Hash: {input_hash}")

        return input_hash.read(16)

    else:
        raise ValueError("Invalid Input! Input must be at least 3 characters long!")