import json
import random
import sys
import time
from typing import List

import httpx
import random_string
import requests
from fastapi import UploadFile
from fastapi.params import Query, File
from pydantic import BaseModel, constr
from sqlalchemy import desc, column, asc, select, func
from sqlalchemy.orm import joinedload
from starlette.requests import Request

from server.conf import session, asyncSession
from server.const import bad_res, create_token, success_res, Const
from server.models import User, ProjData, DevUserData, UserDevUserMap, UserProjMap, DevUser, Role
from server.utils import make_pwd, check_pwd


class UserModel(BaseModel):
    username: constr(min_length=3, max_length=12, strip_whitespace=True) = ''
    password: constr(min_length=3, max_length=12, strip_whitespace=True) = ''
    password1: str = ''
    roleName: str = ''
    operateArr: List[str] = []
    pk: int = None


async def Login(userP: UserModel):
    async with asyncSession() as db:
        q = select(User).filter_by(username=userP.username,
                                   flag=True)
        result = await db.execute(q)
        user = result.scalar()
        if not user:
            return bad_res('用户名或密码错误')
        if not check_pwd(userP.password, user.password):
            return bad_res('用户名或密码错误')
    payload = {'userId': user.userId}
    token = create_token(payload)
    return success_res(data=token, msg='登陆成功')


async def SignUp(userP: UserModel):
    if userP.password != userP.password1:
        return bad_res('密码不一致')
    async with asyncSession() as db:
        q = select(User).filter_by(username=userP.username)
        result = await db.execute(q)
        user = result.scalar()
        if user:
            return bad_res('用户名已存在')
        user = User(username=userP.username,
                    password=make_pwd(userP.password), )
        db.add(user)
        await db.commit()
    payload = {'userId': user.userId}
    token = create_token(payload)
    return success_res(data=token)


def getOperateOps():
    return Role.operate


async def getUserInfo(request: Request):
    async with asyncSession() as db:
        role = (await db.execute(select(Role).filter_by(roleId=request.state.user.roleId))).scalar()
    if role and role.operateArr:
        operateArr = role.operateArr.split(',')
    else:
        operateArr = []
    data = {
        'username': request.state.user.username,
        'userId': request.state.user.userId,
        'avatar_url': request.state.user.avatar_url,
        'operateArr': operateArr
    }
    return success_res(data=data)


async def changePassword(password: str, request: Request):
    async with asyncSession() as db:
        q = select(User).filter_by(userId=request.state.user.userId)
        result = await db.execute(q)
        user = result.scalar()
        user.password = make_pwd(password)
        await db.commit()
    return success_res()


async def setAvatar(avatar: str, request: Request):
    async with asyncSession() as db:
        q = select(User).filter_by(userId=request.state.user.userId)
        result = await db.execute(q)
        user = result.scalar()
        user.avatar_url = avatar
        await db.commit()
    return success_res()


class OverviewModel(BaseModel):
    page: int = 1
    limit: int = 20
    order_by: str = 'openrank'
    item: int = 1
    tt: str = '202410'
    search: str | None = None


async def overview(mm: OverviewModel, request: Request):
    userId = request.state.user.userId
    limit = mm.limit
    offset = (mm.page - 1) * limit
    async with asyncSession() as db:
        if mm.item == 1:
            where = [
                ProjData.tt == mm.tt,
            ]
            if mm.search:
                where.append(ProjData.label.like(f'%{mm.search}%'))
            queryset = select(ProjData
                              ).filter(*where
                                       ).order_by(getattr(ProjData, mm.order_by).desc()
                                                  ).limit(limit).offset(offset)
            result = await db.execute(queryset)
            dataArr = result.scalars().all()

            q2 = select(UserProjMap.projectId).filter_by(userId=userId, flag=True)

            result = await db.execute(q2)
            focusArr = result.scalars().all()

            total_q = select(func.count()).select_from(ProjData).filter(*where)
            result = await db.execute(total_q)
            total = result.scalar()
            columns = [
                {'label': '名称', 'key': 'label'},
                {'label': 'DashBoard', 'key': 'dash'},
                {'label': 'OpenRank', 'key': 'openRank'},
                {'label': '活跃度', 'key': 'activity'},
                {'label': 'Stars', 'key': 'stars'},
                {'label': '关注度', 'key': 'attention'},
                {'label': 'Fork', 'key': 'technical_fork'}
            ]
        else:
            where = [
                DevUserData.tt == mm.tt,
            ]
            if mm.search:
                where.append(DevUserData.label.like(f'%{mm.search}%'))

            queryset = select(DevUserData
                              ).options(joinedload(DevUserData.dev_user)
                                        ).filter(*where
                                                 ).order_by(getattr(DevUserData, mm.order_by).desc()
                                                            ).limit(limit).offset(offset)
            result = await db.execute(queryset)
            dataArr = result.scalars().all()

            q2 = select(UserDevUserMap.devUserId).filter_by(userId=userId, flag=True)

            result = await db.execute(q2)
            focusArr = result.scalars().all()

            total_q = select(func.count()).select_from(DevUserData).filter(*where)
            result = await db.execute(total_q)
            total = result.scalar()

            columns = [
                {'label': '头像', 'key': 'avatar_url'},
                {'label': '名称', 'key': 'label'},
                {'label': 'DashBoard', 'key': 'dash'},
                {'label': 'OpenRank', 'key': 'openRank'},
                {'label': '活跃度', 'key': 'activity'},
            ]
        columns.append({'label': '操作', 'key': 'operate'})
        data = []
        for i in dataArr:
            tmp = await i.to_dict()
            tmp['focus'] = tmp['pk'] in focusArr
            data.append(tmp)
    res = {
        'data': data,
        'columns': columns,
        'total': total
    }
    return res


async def chartData(u_id: int, request: Request):
    res = {}
    attrArr = [
        'openRank',
        'activity',
        'stars',
        'attention',
        'technical_fork',
    ]
    series = []
    xAxisLen = 0
    final_xAxis = []
    async with asyncSession() as db:
        obj = (await db.execute(select(ProjData).filter_by(projectId=u_id))).scalar()
        where = [ProjData.tt > 202401, ProjData.ttType == 'm', ProjData.projectId == u_id]
        queryset = select(ProjData).filter(*where).order_by(ProjData.tt)
        dataArr = (await db.execute(queryset)).scalars().all()
        for attr in attrArr:
            data = []
            xAxis = []
            for i in dataArr:
                data.append(getattr(i, attr))
                xAxis.append(getattr(i, 'tt'))
            res.setdefault(attr, {})['data'] = data
            res.setdefault(attr, {})['xAxis'] = xAxis
            series.append(
                {
                    'name': attr,
                    'type': 'line',
                    'stack': 'Total',
                    'data': data
                },
            )
            if len(xAxis) > xAxisLen:
                xAxisLen = len(xAxis)
                final_xAxis = xAxis
    res['attention']['legend'] = attrArr
    res['attention']['series'] = series
    res['attention']['xAxis'] = final_xAxis

    res['indicator'] = [
        {'value': obj.openRank, 'label': 'OpenRank'},
        {'value': obj.activity, 'label': '活跃度'},
        {'value': obj.stars, 'label': 'Stars'},
        {'value': obj.attention, 'label': '关注度'},
        {'value': obj.technical_fork, 'label': '被Fork数'},
    ]
    res['title'] = obj.label + ' 洞察大屏'

    return res


async def chartData2(u_id: int, request: Request):
    kk = sys._getframe().f_code.co_name + str(u_id)
    res = Const.cache.get(kk)
    if not res:
        res = {}
        attrArr = [
            ('openRank', 'bar', 'OpenRank'),
            ('activity', 'line', '活跃度'),
        ]
        series = []
        yAxis = []
        xAxisLen = 0
        final_xAxis = []
        eventArr = []
        reposArr = []
        async with asyncSession() as db:
            devUser = (await db.execute(select(DevUser).filter_by(devUserId=u_id))).scalar()
            try:
                repo_url = f'https://api.github.com/users/{devUser.name}/repos?per_page=10&page=1'
                async with httpx.AsyncClient() as client:
                    repos = (await client.get(repo_url, timeout=5)).json()
                for repo in repos:
                    tmp = {
                        'full_name': repo.get('name'),
                        'html_url': repo.get('html_url'),
                        'private': not repo.get('private'),
                        'starts': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'watchers': repo.get('watchers_count', 0),
                        'created_at': repo.get('created_at').replace('T', '').replace('Z', ''),
                    }
                    reposArr.append(tmp)

                event_url = f'https://api.github.com/users/{devUser.name}/events?per_page=10&page=1'
                async with httpx.AsyncClient() as client:
                    events = (await client.get(event_url, timeout=5)).json()
                for event in events:
                    if isinstance(event, dict):
                        tmp = {
                            'type': event.get('type'),
                            'full_name': event.get('repo', {}).get('name'),
                            'ref': event.get('payload', {}).get('ref'),
                            'created_at': event.get('created_at', '').replace('T', ' ').replace('Z', ' '),
                        }
                        tmp['html_url'] = 'https://github.com/' + tmp['full_name']
                        eventArr.append(tmp)
            except:
                pass

            where = [DevUserData.tt > 202401, DevUserData.ttType == 'm', DevUserData.devUserId == u_id]
            queryset = select(DevUserData).filter(*where).order_by(DevUserData.tt)
            dataArr = (await db.execute(queryset)).scalars().all()
            for index, attrT in enumerate(attrArr):
                attr, charType, label = attrT
                data = []
                xAxis = []
                yAxis.append({
                    'type': 'value',
                    'name': label,
                })
                for i in dataArr:
                    data.append(getattr(i, attr))
                    xAxis.append(getattr(i, 'tt'))
                series.append(
                    {
                        'name': attr,
                        'type': charType,
                        'data': data,
                        'yAxisIndex': index,
                        'symbolSize': 8,
                    },
                )
                if len(xAxis) > xAxisLen:
                    xAxisLen = len(xAxis)
                    final_xAxis = xAxis

        res['legend'] = [i[0] for i in attrArr]
        res['series'] = series
        res['xAxis'] = final_xAxis
        res['yAxis'] = yAxis
        res['eventArr'] = eventArr

        res['eventColumns'] = [
            {'label': '仓库', 'key': 'full_name'},
            {'label': '分支', 'key': 'ref'},
            {'label': 'type', 'key': 'type'},
            {'label': '时间', 'key': 'created_at'},
        ]
        res['reposArr'] = reposArr
        res['reposColumns'] = [
            {'label': '仓库', 'key': 'full_name'},
            {'label': '是否公开', 'key': 'private'},
            {'label': 'Star数', 'key': 'starts'},
            {'label': 'Fork数', 'key': 'forks'},
            {'label': '关注人数', 'key': 'watchers'},
            {'label': '时间', 'key': 'created_at'},
        ]
        res['otherIndicator'] = [
            {'value': devUser.followers, 'label': '关注人数'},
            {'value': devUser.forks, 'label': 'Forks'},
            {'value': devUser.template_count, 'label': '模板总数'},
            {'value': devUser.issues_count, 'label': 'Issues总数'},

        ]

        res['indicator'] = [
            {'value': devUser.repos, 'label': '项目总数'},
            {'value': devUser.openRank, 'label': 'OpenRank'},
            {'value': devUser.activity, 'label': '活跃度'},
            {'value': devUser.stars, 'label': 'Stars总数'},
            {'value': devUser.technical_fork, 'label': '被Fork总数'},
        ]
        res['title'] = devUser.name + ' 开发者大屏'
        Const.cache[kk] = res

    return res


async def toFocusProj(u_id: int, operate: str, request: Request):
    flag = operate == 'add'
    userId = request.state.user.userId
    async with asyncSession() as db:
        obj = (await db.execute(select(UserProjMap).filter_by(userId=userId, projectId=u_id))).scalar()
        if not obj:
            obj = UserProjMap(userId=userId, projectId=u_id, flag=flag)
            db.add(obj)
        else:
            obj.flag = flag
        await db.commit()
    return success_res(msg='操作成功')


async def toFocusDevUser(u_id: int, operate: str, request: Request):
    flag = operate == 'add'
    userId = request.state.user.userId
    async with asyncSession() as db:
        obj = (await db.execute(select(UserDevUserMap).filter_by(userId=userId, devUserId=u_id))).scalar()
        if not obj:
            obj = UserDevUserMap(userId=userId, devUserId=u_id, flag=flag)
            db.add(obj)
        else:
            obj.flag = flag
        await db.commit()
    return success_res(msg='操作成功')


async def getFocusArr(item: int, request: Request):
    async with asyncSession() as db:
        if item == 1:
            where = {
                UserProjMap.userId == request.state.user.userId,
                UserProjMap.flag == True,
            }
            queryset = select(UserProjMap).options(joinedload(UserProjMap.project)
                                                   ).filter(*where)

            total_aql = select(func.count()).select_from(UserProjMap
                                                         ).filter(*where)
            columns = [
                {'label': '名称', 'key': 'label'},
                {'label': 'DashBoard', 'key': 'dash'},
                {'label': 'OpenRank', 'key': 'openRank'},
                {'label': '活跃度', 'key': 'activity'},
                {'label': 'Stars', 'key': 'stars'},
                {'label': '关注度', 'key': 'attention'},
                {'label': 'Fork', 'key': 'technical_fork'}
            ]
        else:
            where = {
                UserDevUserMap.userId == request.state.user.userId,
                UserDevUserMap.flag == True,
            }
            queryset = select(UserDevUserMap).options(joinedload(UserDevUserMap.dev_user)
                                                      ).filter(*where)

            total_aql = select(func.count()).select_from(UserDevUserMap
                                                         ).filter(*where)
            columns = [
                {'label': '头像', 'key': 'avatar_url'},
                {'label': '名称', 'key': 'label'},
                {'label': 'DashBoard', 'key': 'dash'},
                {'label': 'OpenRank', 'key': 'openRank'},
                {'label': '活跃度', 'key': 'activity'},
            ]
        total = (await db.execute(total_aql)).scalar()

        dataArr = (await db.execute(queryset)).scalars().all()

        data = []
        for i in dataArr:
            tmp = i.to_dict()
            tmp['focus'] = True
            data.append(tmp)
    columns.append({'label': '操作', 'key': 'operate'})
    res = {
        'data': data,
        'columns': columns,
        'total': total
    }
    return res


async def Soul():
    arr = [
        '真正的成功，不在于战胜多少人，而在于成为最好的自己',
        '春风又绿江南岸，明月何时照我还',
        '不要因为害怕失败而停止尝试，每一次尝试都是成功的积累',
        '人生若只如初见，何事秋风悲画扇',
        '梦想是指引前行的灯塔，即使路途遥远，也要勇敢地追逐',
        '山中一夜雨，树杪百重泉',
        '最困难的时候，往往离成功不远。坚持下去，奇迹就会发生',
        '落花人独立，微雨燕双飞',
        '相信自己，超越自我，每一次挑战都是成长的机会',
        '月落乌啼霜满天，江枫渔火对愁眠',
    ]
    return random.choice(arr)


async def Upload(file: UploadFile = File(...)):
    fileName = 'static/' + random_string.generate(max_length=8, min_length=8) + '.png'
    with open(fileName, 'wb') as f:
        f.write(await file.read())
    return f'http://127.0.0.1:7878/{fileName}'


async def getRoleList(request: Request):
    async with asyncSession() as db:
        queryset = select(Role).filter_by(flag=True)
        dataArr = (await db.execute(queryset)).scalars().all()
        total = (await db.execute(select(func.count()).select_from(Role).filter_by(flag=True))).scalar()
        data = [i.to_dict() for i in dataArr]
    columns = [
        {'label': '角色Id', 'key': 'pk'},
        {'label': '角色名', 'key': 'roleName'},
        {'label': '权限', 'key': 'auth'},
        {'label': '操作', 'key': 'operate'},
    ]
    res = {
        'data': data,
        'columns': columns,
        'total': total
    }
    return success_res(res)


async def addRole(userP: UserModel, request: Request):
    async with asyncSession() as db:
        role = (await db.execute(select(Role).filter_by(roleName=userP.roleName))).scalar()
        if role:
            return bad_res('角色名已存在')
        role = Role(roleName=userP.roleName, operateArr=','.join(userP.operateArr))
        db.add(role)
        await db.commit()
        await db.refresh(role)
    return success_res(msg='操作成功')


async def updateRole(userP: UserModel, request: Request):
    async with asyncSession() as db:
        role = (await db.execute(select(Role).filter(Role.roleName == userP.roleName,
                                                     Role.roleId != userP.pk))).scalar()
        if role:
            return bad_res('角色名已存在')
        role = (await db.execute(select(Role).filter(Role.roleId == userP.pk))).scalar()
        role.roleName = userP.roleName
        role.operateArr = ','.join(userP.operateArr)

        await db.commit()
    return success_res(msg='操作成功')


async def deleteRole(pk: int, request: Request):
    async with asyncSession() as db:
        obj = (await db.execute(select(Role).filter_by(roleId=pk))).scalar()
        obj.flag = False
        await db.commit()
    return success_res(msg='操作成功')


async def getUserList(request: Request):
    async with asyncSession() as db:
        queryset = select(User).options(joinedload(User.role)).filter_by(flag=True)
        dataArr = (await db.execute(queryset)).scalars().all()

        data = [i.to_dict() for i in dataArr]
        total = (await db.execute(select(func.count()).select_from(User).filter_by(flag=True))).scalar()
    columns = [
        {'label': '用户Id', 'key': 'pk'},
        {'label': '头像', 'key': 'avatar_url'},
        {'label': '用户名', 'key': 'username'},
        {'label': '角色', 'key': 'roleName'},
        {'label': '操作', 'key': 'operate'},
    ]
    res = {
        'data': data,
        'columns': columns,
        'total': total
    }
    return success_res(res)


async def addUser(userP: UserModel, request: Request):
    async with asyncSession() as db:
        user = (await db.execute(select(User).filter_by(username=userP.username))).scalar()
        if user:
            return bad_res('用户名已存在')
        user = User(username=userP.username,
                    password=make_pwd(userP.password), )
        db.add(user)
        await db.commit()
    return success_res(msg='操作成功')


async def updateUser(userP: UserModel, request: Request):
    async with asyncSession() as db:
        user = (
            await db.execute(select(User).filter(User.username == userP.User,
                                                 User.userId != userP.pk))).scalar()
        user = (await db.execute(select(User).filter(User.userId == userP.pk))).scalar()
        if user:
            return bad_res('用户名已存在')
        user.username = userP.roleName
        user.roleId = userP.roleId

        await db.commit()
    return success_res(msg='操作成功')


async def deleteUser(pk: int, request: Request):
    async with asyncSession() as db:
        obj = (await db.execute(select(User).filter_by(userId=pk))).scalar()
        obj.flag = False
        await db.commit()
    return success_res(msg='操作成功')
