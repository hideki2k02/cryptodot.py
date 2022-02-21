import os, toml

config_file = "cryptodot.toml"


def fetch_config():
    if not os.path.isfile(config_file):
        generate_config()

    current_config = load_config()

    return current_config


def generate_config():
    print("No Config file was found! Generating one...")

    config_template = {
        "user": {
            "dark_mode": False
        },

        "dev": {
            "format_header": "CRYPTODOT",
            "debug": False
        }
    }

    file = open(config_file, "w")
    file.write("# CryptoDot.py Config\n\n")
    file.write(toml.dumps(config_template))
    file.close()


def load_config():
    file = open(config_file, "r")
    program_config = toml.load(file)

    print(f"Config File loaded!")

    # print(program_config)
    # print(program_config["dev"])

    return program_config