# from werkzeug.security import generate_password_hash, check_password_hash
# hash = generate_password_hash('foobar')
# print(hash)

# # проверка
# print(check_password_hash(hash, 'foobar'))
# print(check_password_hash(hash, 'barfoo'))


# pip install passlib
# pip install bcrypt

# from passlib.hash import bcrypt
# import bcrypt as bcrypt2


# logging.getLogger('passlib').setLevel(logging.ERROR)

# php_hashed='$2y$10$UJ660.pogSbAPICwY3EXiuhmqJkX0pENVV3.T3hzJoCez2RvgDhg2'
# password = 'qDyuoFDLCc5'

# php_hashed = '$2y$10$Hkbw5QhjDZBIRmTZulT6R.MYC47aS8yi/EUZ2FYHJClUvRfQlaGTG'
# password = 'O4uAfDke'

# print(bcrypt.verify(password, php_hashed))
# php_hashed = bcrypt.hash(password)


# php_hashed = '$2b$12$DlZHsZBGXerkX2doDr.k4.NE76bp5eERDP50rFb6mY2kS/8sdlER2'
# print(bcrypt.verify(password, php_hashed))

# import hashlib
# password = 'qDyuoFDLCc5'
# hashlib.sha224(password).hexdigest()

#  ------------------ 2 вариант ------------------
# php_hashed = b'$2y$10$Hkbw5QhjDZBIRmTZulT6R.MYC47aS8yi/EUZ2FYHJClUvRfQlaGTG'
# password = b'O4uAfDke'

# print(bcrypt2.checkpw(password, php_hashed))

# hash = bcrypt2.hashpw(password, bcrypt2.gensalt())
# print(hash)

# print(bcrypt2.checkpw(password, hash))

