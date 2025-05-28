import os
import datetime
import json

import requests
from jose.constants import ALGORITHMS
from jose import jwt
from dotenv import load_dotenv

from server.conf import session
from server.models import User

# 加载环境变量
load_dotenv()


class Const:
    # 从环境变量获取数据库配置
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc123')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'dashboard')
    
    uri = f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # JWT配置
    LOGIN_DELTA = datetime.timedelta(hours=int(os.getenv('JWT_EXPIRE_HOURS', '30')))
    HEADER_PREFIX = 'Bearer '
    ALGORITHM = os.getenv('JWT_ALGORITHM', ALGORITHMS.HS256)
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'django-insecure-l%mqno@^^-3+k-@7hh$_98r4nwe*qhv9!0bd6n)h(#vv=date2')

    cache = {}


def create_token(payload, delta=datetime.timedelta(days=10)):
    claims = payload.copy()
    expire = datetime.datetime.now() + delta
    # 添加失效时间
    claims.update({"exp": expire})
    token = jwt.encode(claims, Const.SECRET_KEY, algorithm=Const.ALGORITHM)
    return token


def verify_token(token):
    """
    验证token
    :param token:
    :return: 返回用户信息
    """
    user = None
    try:
        token = token.removeprefix(Const.HEADER_PREFIX)
        payload = jwt.decode(token, Const.SECRET_KEY, algorithms=Const.ALGORITHM)
        with session() as db:
            user = db.query(User).filter_by(userId=payload['userId'], flag=True).first()
        return user
    except:
        pass
    return user


def bad_res(msg='', code=400, ):
    return {'code': code, 'message': msg}


def success_res(data=None, msg=None, code=0):
    return {'code': code, 'message': msg, 'data': data}


def generate_year_month_array():
    start_year = 2015
    start_month = 1
    now = datetime.datetime.now()
    end_year = now.year
    end_month = now.month
    arr = []
    for year in range(start_year, end_year + 1):
        arr.append(year)

    # 生成年份-月份数组
    for year in range(start_year, end_year + 1):
        month_start = start_month if year == start_year else 1
        month_end = end_month if year == end_year else 12
        for month in range(month_start, month_end + 1):
            arr.append(f"{year}-{month:02d}")

    return arr


class OpenDigger:
    def __init__(self):
        self.url = 'https://api.github.com/users/{username}/repos?per_page=100&page=1'
        self.headers = {
            'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN", "")}'
        }

    def get_user_repos(self, username, platform='github'):
        res = {
            'total': 0,
            'avatar': 0,
        }
        try:
            if platform == 'github':
                url = self.url.format(username=username)
                all_repos = []
                page = 1
                while True:
                    resJ = requests.get(url, headers=self.headers, params={"per_page": 100, "page": page})
                    repos = resJ.json()
                    if not repos:
                        break
                    all_repos.extend(repos)
                    page += 1
                print(len(all_repos))
                total_stars = sum(repo["stargazers_count"] for repo in all_repos)
                total_forks = sum(repo["forks_count"] for repo in all_repos)
                print(total_stars)
                print(total_forks)
            else:
                return {}
        except:
            return {}


openDigger = OpenDigger()
