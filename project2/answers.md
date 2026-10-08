# CY2550 Project 2 — Cryptography

### 1.1 Encrypt and Decrypt a File

PBKDF2 takes the passphrase I entered and turns it into a stronger key that AES can actually use for encryption. This is needed because a regular password usually is not random or strong enough to be used directly as an encryption key, and PBKDF2 also makes guessing the password more difficult.

### 1.2 Encrypt the Same File Twice

The checksums are different even though I encrypted the same file with the same password because the encryption uses random values, like the salt and IV, so the ciphertext comes out differently each time. If the encrypted files always came out the same, an attacker could notice when the same information is being encrypted and start learning patterns about the data.

### 1.3 Watching ECB Leak Information

1. How many distinct blocks?
We’ll fill this one in using your actual terminal output because the assignment specifically asks for the numbers you got.    Pasted markdown

2. What did ECB leak?
ECB leaked the pattern of the original data. Since the same plaintext blocks turn into the same encrypted blocks, an attacker could see where information repeats even if they do not know the key or what the actual information says. This can still tell them useful things about the structure of the data.

3. Database question
One thing I would ask is what AES mode is being used? Just saying that something uses AES does not automatically mean it is secure. For example, ECB still leaks patterns even though AES itself is secure.

### 2.2 Keyed Hashing

A regular SHA-256 hash would not protect my colleague in this situation because the attacker could change the file and then just calculate a new hash for the changed file. Since there is no secret involved in making a SHA-256 hash, my colleague would not know that both the file and hash were replaced.

With an HMAC, there is a shared secret key that the attacker does not know. The attacker could still intercept or change the file, but they would not be able to create a valid HMAC for their changed version without knowing the key. So with SHA-256, the attacker can replace both the file and its hash, while with HMAC they can change the file but cannot create a matching valid tag

### 3.3 Fingerprints

1. Email verification
The email verification proves that whoever published the key had access to that Northeastern email account and could click the verification link. It does not necessarily prove that the person is who they claim to be in real life or that the public key actually belongs to the person I think it does.

2. Checking my classmate's key
I would verify the fingerprint with my classmate through a different trusted method, preferably by asking them in person to show or read their fingerprint to me. Then I would compare all 40 characters with the fingerprint of the key I downloaded. This works because even if an attacker controls the network and replaces the public key I downloaded, the fingerprint of their fake key would not match the one my classmate gave me separately.    Pasted markdown

### 4.2 Find the Hybrid Encryption

1. What is in each packet?
The public-key encrypted packet contains the session key, which is encrypted using my RSA public key. The encrypted data packet contains my actual message, which was encrypted using that session key.

2. Why does GPG do this?
GPG does this because RSA is not really meant for encrypting an entire file or large amounts of data. Symmetric encryption is much faster and better for encrypting the actual message, so RSA is only used to securely protect the smaller session key.

3. What is this called?
This is called hybrid encryption because it combines asymmetric and symmetric encryption.    Pasted markdown


### 4.3 Sign, Verify, and Break

1. Which key is used for signing?
My private key.

2. Which key is used for verifying?
My public key.

3. Which key is used for encryption?
The recipient's public key.

4. Which key is used for decryption?
The recipient's private key.

5. What does signing provide that encryption doesn't?
Signing gives me integrity and authenticity. It lets someone check that the message actually came from the person who owns the private key and that it was not changed after it was signed. Encryption mainly protects the confidentiality of the message, so it does not automatically prove who created it.


### Part 5: SSH Keys

Ed25519 can have a much smaller key because it uses a different type of cryptography than RSA and gets its security from a different mathematical problem. Because of that, the number of bits cannot be directly compared, so a 256-bit Ed25519 key is not automatically weaker than a 4096-bit RSA key.    Pasted markdown
This version is much closer to how I'd expect you to write it: clear, straightforward, not overly technical, but it still shows that you actually understand what you're saying.

### 7.1 Generate Cryptographic Code

AI Assistant: ChatGPT
Exact Prompt: “Write me a Python function that encrypts a file with AES.”

### 7.2 Critique the AI Code

1. No integrity/authentication check
One issue I noticed is that the code encrypts the file using AES-CBC, but there is nothing checking if the encrypted file was changed afterward. An attacker could modify the ciphertext and the program would have no way of knowing that it was tampered with. This goes against integrity because encryption can hide the contents of a file, but that does not automatically protect it from being changed.

2. The key has to be provided directly
Another issue is that the function expects the user to already have a valid AES key. It does not generate one or safely turn a password into a key using something like PBKDF2. This could become a security problem if someone uses a weak or predictable key. This relates to key management because AES is only as secure as the key being used.

3. There is no decryption or verification
The code also only handles encryption and does not include a secure way to decrypt and verify the file afterward. This matters because AES-CBC does not check whether the ciphertext has been changed. Without some type of authentication during decryption, the program would not have a reliable way to know if someone tampered with the encrypted file.

### 7.3 Fix the Code

I changed the original code from AES-CBC to AES-GCM because the original version encrypted the file but did not have a way to check if someone changed the ciphertext. GCM gives me encryption and authentication, so the authentication tag can be used to detect if the encrypted file was tampered with.

I also changed the way the key is handled. Instead of making the user provide an AES key directly, I use PBKDF2 with SHA-256, a random salt, and 600,000 iterations to turn a password into a 32-byte AES key. This makes the program easier to use without relying on someone to create their own AES key correctly.

Lastly, I added a decryption function that uses decrypt_and_verify(). This lets the program decrypt the file while also checking the authentication tag, so it should fail if the password is wrong or the encrypted data was changed.
