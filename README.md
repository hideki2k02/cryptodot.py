# CryptoDot.py: Revival of CryptoDot.JS

Cryptography made simple, open-source, and free!

## What is CryptoDot and how was it made?
CryptoDot was made to simplify your Encryption needs.

Originally made with [GODOT Engine](https://godotengine.org/) it was too resource intensive for a text app.

There was an attempt to rebuild it in [Electron.js](https://en.wikipedia.org/wiki/Electron_(software_framework)) but it was abandoned.

Now that i've "gotten back on my feet" i want to finish what i've started a long time ago: CryptoDot.

## How does the program work?
You can Encrypt any Text Data using: a **Node Key** and a **Node Address**.

The same goes for Decryption, but Decryption (optionally) requires the **Node Signature** to verify the file's authenticity.

## Is it safe?
Yes. Theoretically not even [Fugaku (AKA World's Strongest Computer)](https://www.bbc.com/news/world-asia-53147684#:~:text=The%20newly%20crowned%20world's%20fastest,IBM%20machine%20in%20the%20US.) should be able to crack your Node any time soon (He's also busy fighting a Pandemic).

CryptoDot.py uses [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) which is the same Cryptography Standard used by the NSA.

## Nodes explained
Nodes are just Fancy names. Thats all.

**Node Key: Encryption Key (Converted to a [cSHAKE256 Hash](https://www.pycryptodome.org/en/latest/src/hash/cshake256.html))**

**Node Address: An extra parameter used to make the Hashes stronger (Not the [Salt](https://en.wikipedia.org/wiki/Salt_(cryptography)))**

**Node Content: Data Input/Output (depends on the operation; Will create [AES data](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) if you are encrypting)**

**Node Signature (Optional): Hash generated when Encrypting a Node. Used to validate the authenticity of the file**

Just don't use something simple as your Birthday, your Friends may guess it.

## Credits
**10c8 (My Teacher)**

**[pyperclip 1.8.2](https://pypi.org/project/pyperclip/) for Clipboard Access (CLI Mode)**

**[pyqt5 5.15.6](https://pypi.org/project/PyQt5/) for GUI**

**[PyCryptodome 3.12.0](https://pypi.org/project/pycryptodome/) for generating Hashes and AES**

**[TOML 0.10.2](https://pypi.org/project/toml/) for generating the config file**

## To-do list (Feel free to suggest anything)
- [X] Finish the base code
- [X] Rework the file format and how the functions work
- [X] Implement the GUI
- [X] Implement a Clear Node Button
- [ ] Implement a decent config system using TOML
- [ ] Implement Dark Mode
- [ ] Fix my code