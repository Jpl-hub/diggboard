import datetime
import json
import shutil
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import urllib3

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
uri = 'mysql+pymysql://root:abc123@localhost/dashboard'
resp_url_base = 'https://api.github.com/users/{username}/repos?per_page=100&page=1'
info_url_base = 'https://api.github.com/users/{username}'
attrUrl = 'https://oss.open-digger.cn/{platform}/{name}/{attr}'
engine = create_engine(uri)

headers = {
    'Authorization': 'Bearer '
}


def generate_proj():
    def proj(row):
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
            # 完全禁用SSL验证
            res = requests.get(url, headers=headers, timeout=timeout, verify=False)
            if res.status_code != 200:
                attrMap[column] = {}
                continue
            text = res.text
            data = json.loads(text)
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

            if not all([tmp['openrank'], tmp['activity']]):
                continue
            projDataArr.append(tmp)

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

    df_proj = pd.DataFrame(projDataArr)
    df_proj.to_sql('proj_data', engine, if_exists='replace')

    df_sql_proj = pd.DataFrame(projArr)
    df_sql_proj.to_sql('project', engine, if_exists='replace')


def generate_devuser():
    def devUser(_index, row):
        try:
            name = row['actor_login']
            platform = row['platform']
            pk = row['id']
            obj = {
                'devUserId': pk,
                'name': name,
                'platform': platform,
            }
            info_url = info_url_base.format(username=name)
            # 完全禁用SSL验证
            info = requests.get(info_url, headers=headers, timeout=timeout, verify=False).json()
            filename = random_string.generate(min_length=8, max_length=8) +'.png'
            filePath = dirPath.joinpath(filename)
            avatar_url = info.get('avatar_url', '')
            if avatar_url:
                with open(filePath, 'wb') as f:
                    # 完全禁用SSL验证
                    f.write(requests.get(avatar_url, verify=False).content)
            obj['avatar_url'] = str(filePath)
            obj['followers'] = info.get('followers', 0)
            obj['following'] = info.get('following', 0)
            resp_url = resp_url_base.format(username=name)
            all_repos = []
            page = 1
            while True:
                # 完全禁用SSL验证
                resJ = requests.get(resp_url, headers=headers, params={"per_page": 100, "page": page},
                                   timeout=timeout, verify=False)
                repos = resJ.json()
                if not repos:
                    break
                all_repos.extend(repos)
                page += 1
            repos = len(all_repos)
            stars = 0
            technical_fork = 0
            forks = 0
            template_count = 0
            issues_count = 0
            for repo in all_repos:
                stars += repo["stargazers_count"] or 0
                technical_fork += repo["forks_count"] or 0
                issues_count += repo["open_issues"] or 0
                if repo.get('is_template'):
                    template_count += 1
                if repo.get('fork'):
                    forks += 1
            obj['repos'] = repos,
            obj['stars'] = stars,
            obj['technical_fork'] = technical_fork
            obj['issues_count'] = issues_count
            obj['template_count'] = template_count
            obj['forks'] = forks
            attrMap = {}
            for j in attrArr:
                column = j.split('.')[0]
                obj[column] = 0
                url = attrUrl.format(platform=platform, name=name, attr=j)
                # 完全禁用SSL验证
                res = requests.get(url, headers=headers, timeout=timeout, verify=False)
                if res.status_code != 200:
                    attrMap[column] = {}
                    continue
                text = res.text
                data = json.loads(text)
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

                if not all([tmp['openrank'], tmp['activity']]):
                    continue
                dataArr.append(tmp)
        except Exception as e:
            print(traceback.format_exc())
        print(_index, '完毕')

    dataArr = []
    userArr = []
    df_user = pd.read_csv('user_list.csv')
    df_user = df_user[df_user['actor_login'].apply(lambda x: len(str(x)) < 15)]
    df_user = df_user[df_user['platform'] == 'github'].sample(sample)

    attrArr = ['openrank.json',
               'activity.json',
               ]
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        origin_data = df_user.to_dict(orient='records')

        for index, i in enumerate(origin_data):
            exe.submit(devUser, index, i)
    print('开始插入数据...')
    df_proj = pd.DataFrame(dataArr)
    df_proj.to_sql('devuser_data', engine, if_exists='replace')

    df_sql_user = pd.DataFrame(userArr)

    df_sql_user.to_sql('devuser', engine, if_exists='replace')


if __name__ == '__main__':
    dirPath = Path('static/avatar')
    if dirPath.exists():
        shutil.rmtree(dirPath)
    dirPath.mkdir(exist_ok=True)
    conn = pymysql.connect(
        user='root',
        password='abc123',
        database='dashboard',
        autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute('truncate table user_devuser_map;')
    cursor.execute('truncate table user_proj_map;')

    max_workers = 20
    timeout = 30
    sample = 100
    t1 = time.time()
    generate_devuser()
    t2 = time.time()
    print('生成用户数据用时：', t2 - t1)

    generate_proj()
    t3 = time.time()
    print('生成项目数据用时：', t3 - t2)