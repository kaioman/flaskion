from cryptography.fernet import Fernet
# Fernet暗号化に使用する共有鍵（対象鍵）を生成する
print(Fernet.generate_key().decode())
