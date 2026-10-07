# CY2550 Project 2 — Cryptography

## Part 1: Symmetric Encryption

### 1.1 Encrypt and Decrypt a File

PBKDF2 takes the password I entered and turns it into a key that AES can actually use. It also uses a salt and repeats the process many times, which makes it harder for someone to just guess passwords until they find the right one.

### 1.2 Encrypt the Same File Twice

The checksums are different because each encryption uses randomness, so even though I encrypted the same file with the same password, I didn't get the exact same ciphertext both times.

If they were identical, someone could start recognizing when the same information is being encrypted. They still might not know what the information actually says, but they could learn patterns from seeing the same ciphertext appear again.

### 1.3 Watching ECB Leak Information

1. ECB produced 3 distinct blocks, and the most common block repeated 24 times. CBC produced 37 distinct blocks, with each block only appearing once.

2. ECB leaked the pattern of the data. Since the same plaintext blocks turned into the same encrypted blocks, someone looking at the ciphertext could tell that certain parts of the original data repeated. They wouldn't know exactly what the data says, but the pattern itself could still give them useful information.

3. I would ask what AES mode the system is using and how it handles its IV or nonce. Just saying that something uses AES doesn't automatically mean it is secure because the way AES is being used matters too.


## Part 2: Integrity

### 2.2 Keyed Hashing

A regular SHA-256 hash wouldn't protect the file in this situation because the attacker controls the same channel that the file and hash are being sent through. They could change the file, calculate a new hash for their changed version, and send both to my colleague. The new hash would match, so my colleague wouldn't know anything was changed.

An HMAC is different because you need the secret key to create the correct tag. An attacker could still change the file or send a fake tag, but without the secret key they wouldn't be able to create a valid HMAC for the changed file. That gives my colleague a way to tell if the file was tampered with.


## Part 3: Cryptographic Keys

### 3.3 Fingerprints

1. Clicking the verification link proves that whoever published the key has access to that email address. It doesn't prove that they are actually the person they claim to be or that I should automatically trust the key.

2. I would contact my classmate through a different trusted method, like asking them in person, and compare the full 40-character fingerprint with them. If the fingerprints match, I can be more confident that I downloaded their real public key. This would work even if someone was controlling the network because I'm verifying the fingerprint through a separate method that the attacker doesn't control.


## Part 4: Asymmetric Encryption in Use

### 4.2 Find the Hybrid Encryption

1. The public-key encrypted packet contains the session key, while the OCB encrypted packet contains the actual encrypted message.

2. GPG doesn't encrypt the entire message with RSA because RSA is slower and isn't really meant for encrypting large amounts of data. Instead, it uses RSA to protect the smaller session key and then uses faster symmetric encryption for the actual message.

3. This is called hybrid encryption.

### 4.3 Sign, Verify, and Break

1. My private key is used to sign the file.

2. My public key is used to verify the signature.

3. The recipient's public key is used to encrypt something for them.

4. The recipient's private key is used to decrypt it.

5. Signing gives authenticity and integrity. It lets someone check who signed the message and whether the message was changed afterward, which encryption by itself doesn't necessarily provide.


## Part 5: SSH Keys

RSA and Ed25519 are based on different mathematical problems, so I can't compare their security just by looking at the number of bits. Elliptic-curve cryptography can provide strong security with much smaller keys, so the smaller Ed25519 key isn't automatically weaker than my 4096-bit RSA key.


## Part 7: Grading the Machine

### 7.1 Generate Cryptographic Code

**AI Assistant Used:** ChatGPT

**Exact Prompt:**  
"Write me a Python function that encrypts a file with AES."

### 7.2 Critique the AI Code

#### Defect 1: CBC doesn't check if the encrypted data was changed

**What is wrong:**  
The code uses AES-CBC to encrypt the file, but there isn't anything checking whether someone changed the ciphertext afterward.

**Attacker impact:**  
An attacker could modify the encrypted file and the program wouldn't have a reliable way to tell that it had been tampered with.

**Lecture concept:**  
This relates to confidentiality vs. integrity. Encryption can hide the contents of something, but that doesn't automatically mean it can detect when the data has been changed.

#### Defect 2: The key isn't really being managed

**What is wrong:**  
The function expects me to give it an AES key, but it doesn't say anything about how that key should be created, stored, or protected.

**Attacker impact:**  
If someone hard-coded the key or stored it somewhere insecure, an attacker who found the key could decrypt the files.

**Lecture concept:**  
This relates to key management. The encryption itself can be strong, but that doesn't help much if the secret key isn't protected.

#### Defect 3: There is no safe way to turn a password into a key

**What is wrong:**  
The code expects an AES key instead of handling a normal password. If someone tried to turn their password directly into a key themselves, they could end up using something weak or predictable.

**Attacker impact:**  
That could make it easier for someone to guess the password or key and decrypt the file.

**Lecture concept:**  
This relates to password-based key derivation. Earlier in the project I used PBKDF2, which uses a salt and repeated work to make password guessing harder.

### 7.3 Fix the Code

I changed the code from AES-CBC to AES-GCM because I wanted the program to protect the file from being changed, not just hide what is inside it. GCM gives me encryption along with an authentication check, so if someone tampers with the ciphertext, the program can detect it. This addresses the integrity problem from the original code.

I also changed it so that I can give the program a password and have PBKDF2 derive the AES key from it. It uses a random salt and a large number of iterations, which makes guessing the password more expensive. This addresses the password-to-key issue and makes the way the key is created safer.

To make sure the fixed version actually worked, I encrypted a test file and then decrypted it again. I compared the original file to the decrypted one with diff, and no output meant that the two files were identical.
