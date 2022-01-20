from Crypto.Hash import cSHAKE256

def process_input(input_data, address):
    minimum_required_lenght = len(input_data) >= 3 and len(address) >= 3

    if minimum_required_lenght: 
        # If the required length is met, Turn Input into a cSHAKE256 Hash
        input_hash = cSHAKE256.new(bytes(input_data, "utf-8"))

        # Update Input's Hash with the Address
        input_hash.update(bytes(address, "utf-8"))

        return input_hash.read(16)

    else:
        raise ValueError("Invalid Information! Input must be at least 3 characters long!")