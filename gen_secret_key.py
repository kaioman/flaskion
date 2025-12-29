import secrets
# FlaskのSECRET_KEYやJWT署名用に使用可能な、暗号学的に安全でランダムな秘密鍵を生成する
print(secrets.token_hex(32))
