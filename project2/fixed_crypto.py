from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256


def make_key(password, salt):
    return PBKDF2(
        password,
        salt,
        dkLen=32,
        count=600000,
        hmac_hash_module=SHA256
    )


def encrypt_file(input_file, output_file, password):
    salt = get_random_bytes(16)
    key = make_key(password, salt)

    with open(input_file, "rb") as f:
        plaintext = f.read()

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    with open(output_file, "wb") as f:
        f.write(salt + cipher.nonce + tag + ciphertext)


def decrypt_file(input_file, output_file, password):
    with open(input_file, "rb") as f:
        data = f.read()

    salt = data[:16]
    nonce = data[16:32]
    tag = data[32:48]
    ciphertext = data[48:]

    key = make_key(password, salt)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    with open(output_file, "wb") as f:
        f.write(plaintext)
