#!/usr/bin/env python
"""
测试用户角色赋予功能
"""
import asyncio
from server.conf import asyncSession
from server.models import User, Role
from sqlalchemy import select
from sqlalchemy.orm import joinedload

async def test_user_role():
    """测试用户角色功能"""
    async with asyncSession() as db:
        # 查询所有用户和其角色
        print("=== 当前用户列表 ===")
        users = await db.execute(
            select(User).options(joinedload(User.role)).filter_by(flag=True)
        )
        for user in users.scalars().all():
            print(f"用户ID: {user.userId}, 用户名: {user.username}, 角色ID: {user.roleId}, 角色名: {user.role.roleName if user.role else '无角色'}")
        
        print("\n=== 当前角色列表 ===")
        roles = await db.execute(select(Role).filter_by(flag=True))
        for role in roles.scalars().all():
            print(f"角色ID: {role.roleId}, 角色名: {role.roleName}")

if __name__ == "__main__":
    asyncio.run(test_user_role())
