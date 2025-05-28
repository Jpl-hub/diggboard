import os
import datetime
import json
import shutil
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import urllib3
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pandas as pd
import random_string
import requests
from sqlalchemy import create_engine
import pymysql
import certifi

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


times = generate_year_month_array()

# 从环境变量获取数据库配置
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'dashboard')

uri = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
resp_url_base = 'https://api.github.com/users/{username}/repos?per_page=100&page=1'
info_url_base = 'https://api.github.com/users/{username}'
attrUrl = 'https://oss.open-digger.cn/{platform}/{name}/{attr}'
engine = create_engine(uri)

# 从环境变量获取GitHub Token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Python-Dashboard-App'
}

def safe_api_request(url, headers, timeout=30, max_retries=3):
    """安全的API请求函数，带重试机制"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout, verify=False)
            
            # 检查响应状态码
            if response.status_code == 200:
                # 检查响应内容是否为空
                if not response.text.strip():
                    print(f"警告: API返回空响应 - {url}")
                    return None
                return response.json()
            elif response.status_code == 403:
                print(f"API限制错误 (403) - {url}")
                if 'rate limit' in response.text.lower():
                    print("GitHub API访问限制，等待60秒...")
                    time.sleep(60)
                    continue
                return None
            elif response.status_code == 404:
                print(f"资源未找到 (404) - {url}")
                return None
            else:
                print(f"API请求失败，状态码: {response.status_code} - {url}")
                print(f"响应内容: {response.text[:200]}...")
                return None
                
        except requests.exceptions.Timeout:
            print(f"请求超时 (尝试 {attempt + 1}/{max_retries}) - {url}")
        except requests.exceptions.ConnectionError:
            print(f"连接错误 (尝试 {attempt + 1}/{max_retries}) - {url}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 (尝试 {attempt + 1}/{max_retries}) - {url}")
            print(f"响应内容: {response.text[:200] if 'response' in locals() else 'No response'}...")
        except Exception as e:
            print(f"未知错误 (尝试 {attempt + 1}/{max_retries}) - {url}: {str(e)}")
        
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 2  # 递增等待时间
            print(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    print(f"所有重试失败 - {url}")
    return None

def generate_proj():
    def proj(row):
        try:
            name = row['repo_name']
            platform = row['platform']
            pk = row['id']

            obj = {
                'projectId': pk,
                'name': name,
                'platform': platform,
            }

            attrMap = {}
            for j in attrArr:
                column = j.split('.')[0]
                obj[column] = 0
                url = attrUrl.format(platform=platform, name=name, attr=j)
                
                # 使用安全的API请求
                data = safe_api_request(url, headers, timeout)
                if data is None:
                    attrMap[column] = {}
                    continue
                    
                obj[column] = round(sum(data.values()), 1)
                attrMap[column] = data
                
            projArr.append(obj)
            
            for t in times:
                t = str(t)
                tmp = {'projectId': pk,
                       'label': name,
                       'tt': int(t.replace('-', '')),
                       'ttType': 'y' if len(t) == 4 else 'm',
                       }
                for k, v in attrMap.items():
                    value = v.get(t, 0)
                    tmp[k] = value

                if not all([tmp.get('openrank'), tmp.get('activity')]):
                    continue
                projDataArr.append(tmp)
        except Exception as e:
            print(f"处理项目 {row.get('repo_name', 'unknown')} 时出错: {str(e)}")
            print(traceback.format_exc())

    df_repo = pd.read_csv('repo_list.csv')
    df_repo = df_repo[df_repo['repo_name'].apply(lambda x: len(str(x)) < 15)]
    df_repo = df_repo[df_repo['platform'] == 'github'].sample(sample)

    attrArr = ['openrank.json',
               'activity.json',
               'stars.json',
               'attention.json',
               'technical_fork.json',
               ]

    projDataArr = []
    projArr = []

    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        origin_data = df_repo.to_dict(orient='records')
        for i in origin_data:
            exe.submit(proj, i)

    if projDataArr:
        df_proj = pd.DataFrame(projDataArr)
        df_proj.to_sql('proj_data', engine, if_exists='replace')

    if projArr:
        df_sql_proj = pd.DataFrame(projArr)
        df_sql_proj.to_sql('project', engine, if_exists='replace')


def generate_devuser():
    def devUser(_index, row):
        try:
            name = row['actor_login']
            platform = row['platform']
            pk = row['id']
            
            print(f"处理用户 {_index}: {name}")
            
            obj = {
                'devUserId': pk,
                'name': name,
                'platform': platform,
            }
            
            info_url = info_url_base.format(username=name)
            
            # 使用安全的API请求获取用户信息
            info = safe_api_request(info_url, headers, timeout)
            if info is None:
                print(f"跳过用户 {name} - 无法获取用户信息")
                return
            
            # 下载头像
            filename = random_string.generate(min_length=8, max_length=8) + '.png'
            filePath = dirPath.joinpath(filename)
            avatar_url = info.get('avatar_url', '')
            if avatar_url:
                try:
                    avatar_response = requests.get(avatar_url, verify=False, timeout=10)
                    if avatar_response.status_code == 200:
                        with open(filePath, 'wb') as f:
                            f.write(avatar_response.content)
                        obj['avatar_url'] = str(filePath)
                    else:
                        obj['avatar_url'] = ''
                except Exception as e:
                    print(f"下载头像失败 {name}: {str(e)}")
                    obj['avatar_url'] = ''
            else:
                obj['avatar_url'] = ''
                
            obj['followers'] = info.get('followers', 0)
            obj['following'] = info.get('following', 0)
            
            # 获取用户仓库信息
            resp_url = resp_url_base.format(username=name)
            all_repos = []
            page = 1
            
            while page <= 5:  # 限制最多5页，避免无限循环
                repos_data = safe_api_request(f"{resp_url}&page={page}", headers, timeout)
                if repos_data is None or not repos_data:
                    break
                all_repos.extend(repos_data)
                page += 1
                
                # 如果返回的仓库数量少于100，说明已经是最后一页
                if len(repos_data) < 100:
                    break
            
            repos = len(all_repos)
            stars = 0
            technical_fork = 0
            forks = 0
            template_count = 0
            issues_count = 0
            
            for repo in all_repos:
                stars += repo.get("stargazers_count", 0) or 0
                technical_fork += repo.get("forks_count", 0) or 0
                issues_count += repo.get("open_issues", 0) or 0
                if repo.get('is_template'):
                    template_count += 1
                if repo.get('fork'):
                    forks += 1
                    
            obj['repos'] = repos
            obj['stars'] = stars
            obj['technical_fork'] = technical_fork
            obj['issues_count'] = issues_count
            obj['template_count'] = template_count
            obj['forks'] = forks
            
            attrMap = {}
            for j in attrArr:
                column = j.split('.')[0]
                obj[column] = 0
                url = attrUrl.format(platform=platform, name=name, attr=j)
                
                data = safe_api_request(url, headers, timeout)
                if data is None:
                    attrMap[column] = {}
                    continue
                    
                obj[column] = round(sum(data.values()), 1)
                attrMap[column] = data
                
            userArr.append(obj)

            for t in times:
                t = str(t)
                tmp = {'devUserId': pk,
                       'label': name,
                       'tt': int(t.replace('-', '')),
                       'ttType': 'y' if len(t) == 4 else 'm',
                       }
                for k, v in attrMap.items():
                    value = v.get(t, 0)
                    tmp[k] = value

                if not all([tmp.get('openrank'), tmp.get('activity')]):
                    continue
                dataArr.append(tmp)
                
        except Exception as e:
            print(f"处理用户 {row.get('actor_login', 'unknown')} 时出错: {str(e)}")
            print(traceback.format_exc())
            
        print(f'{_index} 完毕')

    dataArr = []
    userArr = []
    df_user = pd.read_csv('user_list.csv')
    df_user = df_user[df_user['actor_login'].apply(lambda x: len(str(x)) < 15)]
    df_user = df_user[df_user['platform'] == 'github'].sample(sample)

    attrArr = ['openrank.json', 'activity.json']
    
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        origin_data = df_user.to_dict(orient='records')
        for index, i in enumerate(origin_data):
            exe.submit(devUser, index, i)
            
    print('开始插入数据...')
    
    if dataArr:
        df_proj = pd.DataFrame(dataArr)
        df_proj.to_sql('devuser_data', engine, if_exists='replace')

    if userArr:
        df_sql_user = pd.DataFrame(userArr)
        df_sql_user.to_sql('devuser', engine, if_exists='replace')


if __name__ == '__main__':
    dirPath = Path('static/avatar')
    if dirPath.exists():
        shutil.rmtree(dirPath)
    dirPath.mkdir(exist_ok=True, parents=True)
    
    conn = pymysql.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
        autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute('truncate table user_devuser_map;')
    cursor.execute('truncate table user_proj_map;')

    max_workers = 20  # 减少并发数，避免API限制
    timeout = 30
    sample = 100  # 减少样本数量进行测试
    
    print("开始生成用户数据...")
    t1 = time.time()
    generate_devuser()
    t2 = time.time()
    print('生成用户数据用时：', t2 - t1)

    print("开始生成项目数据...")
    generate_proj()
    t3 = time.time()
    print('生成项目数据用时：', t3 - t2)
    print('总用时：', t3 - t1)