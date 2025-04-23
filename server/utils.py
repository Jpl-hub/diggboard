import bcrypt


# 原始密码
def make_pwd(pwd):
    # 加密（生成哈希）
    hashed_password = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

    # 存入数据库（转为 str）
    hashed_password_str = hashed_password.decode('utf-8')
    return hashed_password_str


def check_pwd(input_pwd, hashed_pwd):
    # 验证密码
    try:
        return bcrypt.checkpw(input_pwd.encode('utf-8'), hashed_pwd.encode('utf-8'))
    except:
        return False
