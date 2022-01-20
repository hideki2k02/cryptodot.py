# CryptoDot.py: Revival of CryptoDot.JS

Cryptography made simple, open-source, and free!

## What is CryptoDot and how was it made?
CryptoDot was made to simplify your Encryption needs.

Originally made with [GODOT Engine](https://godotengine.org/) it was too resource intensive for a text app.

There was an attempt to rebuild it in [Electron.js](https://en.wikipedia.org/wiki/Electron_(software_framework)) but it was abandoned.

Now that i've "gotten back on my feet" i want to finish what i've started a long time ago: CryptoDot.

## How does the program work?
You can Encrypt any Text Data using: a **Node Name**, **Node Key** and a **Node Address**.

The same goes for Decryption, but Decryption (optionally) requires the **Node Signature** to verify the file's authenticity.

**Notes for Encryption: If a Node already exists with that name and address, it will OVERWRITE it! so be careful (Currently i don't intend to change this)**

**If you are afraid to acidentally overwrite a Node, you can always save the Node Name and Address somewhere safe. Even if they have the name, they won't know whats inside without the password ;)**

**(Not even me, thats the 🦆ing point anyway).**

## Is it safe?
Yes. Theoretically not even [Fugaku (AKA World's Strongest Computer)](https://www.bbc.com/news/world-asia-53147684#:~:text=The%20newly%20crowned%20world's%20fastest,IBM%20machine%20in%20the%20US.) should be able to crack your Node any time soon (He's also busy fighting a Pandemic).

CryptoDot.py uses [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) which is the same Cryptography Standard used by the NSA.

## Nodes explained
Nodes are just Fancy names. Thats all.

**Node Name: File Name (Converted to a [cSHAKE256 Hash](https://www.pycryptodome.org/en/latest/src/hash/cshake256.html))**

**Node Key: Encryption Key (Converted to a [cSHAKE256 Hash](https://www.pycryptodome.org/en/latest/src/hash/cshake256.html))**

**Node Address: An extra parameter used to make the Hashes stronger (Not the [Salt](https://en.wikipedia.org/wiki/Salt_(cryptography)))**

**Node Content: Data Input/Output (depends on the operation; Will create [AES data](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) if you are encrypting)**

**Node Signature (Optional): The Hash generated when Encrypting a Node. Used to validate the authenticity of the file**

Just don't use something simple as your Birthday, your Friends may guess it.

## Credits
**10c8 (My Teacher)**

**[pyperclip 1.8.2](https://pypi.org/project/pyperclip/) (Clipboard Access)**
**[pyqt5 5.15.6](https://pypi.org/project/PyQt5/) for GUI**
**[PyCryptodome 3.12.0](https://pypi.org/project/pycryptodome/) for generating Hashes and AES**

## To-do list
- [X] Finish the base code
- [ ] Implement the GUI
