
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

# import hashlib
#
# print(a, "path=========================")
# with open(r"C:\main project\university_exam_evaluation\media/" + a, "rb") as imageFile:
#     for byte_block in iter(lambda: imageFile.read(4096), b""):
#         sha256_hash.update(byte_block)
#     print(sha256_hash.hexdigest())
#     stri = base64.b64encode(imageFile.read()).decode('utf-8')
#     enc1 = encrypt(stri, key).decode('utf-8')
#
#     fh = open(r"C:\main project\university_exam_evaluation\media/" + a, "wb")
#     fh.write(base64.b64decode(enc1))
#     fh.close()
#
# # filename = r"C:\main project\university_exam_evaluation\media\3.jpg"
# # sha256_hash = hashlib.sha256()
# # with open(filename,"rb") as f:
# #     # Read and update hash string value in blocks of 4K
# #     for byte_block in iter(lambda: f.read(4096),b""):
# #         sha256_hash.update(byte_block)
# #     print(sha256_hash.hexdigest())
# key = "qsdrt"
#
# with open(r"C:\main project\university_exam_evaluation\media\rootkey.csv", "rb") as imageFile:
#             stri = base64.b64encode(imageFile.read()).decode('utf-8')
#
#
#             dec2 = decrypt(stri, key).decode('utf-8')
#
#
#             fh1 = open(r"C:\main project\university_exam_evaluation\media\3.csv", "wb")
#             fh1.write(base64.b64decode(dec2))
#             fh1.close()