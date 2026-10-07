from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def encrypt_file(input_file, output_file, key):
    """
    Encrypts a file using AES encryption.

    Args:
        input_file: Path to the file to encrypt.
        output_file: Path where the encrypted file will be saved.
        key: AES key (must be 16, 24, or 32 bytes).
    """
    with open(input_file, "rb") as f:
        plaintext = f.read()

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_file, "wb") as f:
        f.write(iv + ciphertext)
