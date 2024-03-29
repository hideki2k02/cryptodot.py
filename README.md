# CRYPTODOT HAS BEEN PUT ON HIATUS, YOU SHOULD USE [KeePassXC](https://github.com/keepassxreboot/keepassxc)
### CryptoDot in general has always been a pet project of mine. "My own Cryptography Program" that i knew it was "safe" from backdoors (did not take backdoors on the libraries as a possibility at the time) because i've built it. 

However i've discovered far more robust/efficient alternatives that exists for FAR LONGER (Even before i could think straight) and that have stood the test of time, like [KeePassXC](https://github.com/keepassxreboot/keepassxc) (It is based on KeePass, which itself exists since 2003).

Since i've mainly used CryptoDot to store Links/Passwords, KeePassXC is the _magnum opus_ for me (If compared to CryptoDot it is overkill), heck it even store files! (Fun Fact: Originally i was trying to create a File Encryptor) and have backups so its a win-win. 

Well, goodbye for now. I've learned a lot with CryptoDot but i think it is time to accept defeat haha



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

### [Credits](https://github.com/japa4551/cryptodot.py/blob/main/CREDITS.md)
### [TO-DO List](https://github.com/japa4551/cryptodot.py/blob/main/TO-DO.md)
