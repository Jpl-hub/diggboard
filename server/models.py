import json

from sqlalchemy import Column, String, Integer, BOOLEAN, Float, ForeignKey, select
from sqlalchemy.orm import relationship
from server.conf import Base, engine

url_prefix = f'http://127.0.0.1:7878/'


class Role(Base):
    """角色表"""
    __tablename__ = 'role'
    roleId = Column(Integer, primary_key=True)
    roleName = Column(String(200), nullable=True)
    flag = Column(BOOLEAN, default=True, nullable=True)
    operateArr = Column(String(500), nullable=True)
    user = relationship("User", back_populates="role")
    operate = [
        {'label': '后台管理', 'value': 'admin'},

        {'label': '用户管理', 'value': 'userManager'},
        {'label': '添加用户', 'value': 'addUser'},
        {'label': '修改用户', 'value': 'updateUser'},
        {'label': '删除用户', 'value': 'deleteUser'},

        {'label': '角色管理', 'value': 'roleManager'},
        {'label': '添加角色', 'value': 'addRole'},
        {'label': '删除角色', 'value': 'deleteRole'},
        {'label': '修改角色', 'value': 'updateRole'},
    ]

    def to_dict(self):
        tmp = []
        if self.operateArr:
            for i in self.operateArr.split(','):
                for jj in self.operate:
                    if jj['value'] == i:
                        tmp.append(jj['label'])
                        break
            ops = ', '.join(tmp)
        else:
            ops = ''
        return {
            'pk': self.roleId,
            'roleName': self.roleName,
            'operateArr': self.operateArr.split(',') if self.operateArr else [],
            'auth': ops,
        }


class User(Base):
    """用户表"""
    __tablename__ = 'user'
    userId = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False)
    avatar_url = Column(String(200), nullable=True)
    password = Column(String(200), nullable=True)
    roleId = Column(Integer, ForeignKey('role.roleId', ondelete='SET NULL'), nullable=True)
    role = relationship("Role", back_populates="user")
    flag = Column(BOOLEAN, nullable=True, default=True)

    def to_dict(self):
        return {
            'pk': self.userId,
            'username': self.username,
            'avatar_url': self.avatar_url,
            'roleId': self.roleId,
            'roleName': self.role.roleName if self.role else '',
        }


class Project(Base):
    """项目表"""
    __tablename__ = 'project'
    projectId = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    platform = Column(String(200), nullable=True)
    openRank = Column(Float, nullable=True)
    activity = Column(Float, nullable=True)
    stars = Column(Integer, nullable=True)
    attention = Column(Integer, nullable=True)
    technical_fork = Column(Integer, nullable=True)
    proj_data = relationship("ProjData", back_populates="project")
    user_proj_map = relationship("UserProjMap", back_populates="project")


class ProjData(Base):
    """项目数据表"""
    __tablename__ = 'proj_data'
    index = Column(Integer, primary_key=True)
    projectId = Column(Integer, ForeignKey('project.projectId', ondelete='SET NULL'), nullable=False)
    project = relationship("Project", back_populates="proj_data")
    label = Column(String(200), nullable=True)
    tt = Column(Integer, nullable=True)
    ttType = Column(String(200), nullable=True, comment='时间类型，y年，m月')
    openRank = Column(Float, nullable=True)
    activity = Column(Float, nullable=True)
    stars = Column(Integer, nullable=True)
    attention = Column(Integer, nullable=True)
    technical_fork = Column(Integer, nullable=True)

    async def to_dict(self):
        return {
            'pk': self.projectId,
            'label': self.label,
            'item': 1,
            'tt': self.tt,
            'openRank': self.openRank,
            'activity': self.activity,
            'stars': self.stars,
            'attention': self.attention,
            'technical_fork': self.technical_fork,
        }


class DevUser(Base):
    """开发者表"""
    __tablename__ = 'devuser'
    devUserId = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True, comment='fork数')
    platform = Column(String(200), nullable=True)
    openRank = Column(Float, nullable=True)
    activity = Column(Float, nullable=True)
    repos = Column(Integer, nullable=True, comment='仓库总数')
    stars = Column(Integer, nullable=True, comment='星标数')
    technical_fork = Column(Integer, nullable=True, comment='被fork数')
    forks = Column(Integer, nullable=True, comment='fork总数')
    followers = Column(Integer, nullable=True, comment='关注人数')
    following = Column(Integer, nullable=True, comment='粉丝人数')
    template_count = Column(Integer, nullable=True, comment='模板数')
    issues_count = Column(Integer, nullable=True, comment='模板数')
    dev_user_data = relationship("DevUserData", back_populates="dev_user")
    user_devuser_map = relationship("UserDevUserMap", back_populates="dev_user")


class DevUserData(Base):
    """开发者数据表"""
    __tablename__ = 'devuser_data'
    index = Column(Integer, primary_key=True)
    devUserId = Column(Integer, ForeignKey('devuser.devUserId', ondelete='SET NULL'), nullable=False)
    dev_user = relationship("DevUser", back_populates="dev_user_data")
    label = Column(String(200), nullable=True)
    tt = Column(Integer, nullable=True)
    ttType = Column(String(200), nullable=True, comment='时间类型，y年，m月')
    openRank = Column(Float, nullable=True)
    activity = Column(Float, nullable=True)

    async def to_dict(self):
        return {
            'index': self.index,
            'pk': self.devUserId,
            'avatar_url': url_prefix + (self.dev_user.avatar_url or ''),
            'home': 'https://github.com/' + self.dev_user.name,
            'item': 2,
            'label': self.label,
            'tt': self.tt,
            'openRank': self.openRank,
            'activity': self.activity,
        }


class UserProjMap(Base):
    """用户项目映射"""
    __tablename__ = 'user_proj_map'
    userId = Column(Integer, ForeignKey('user.userId', ondelete='SET NULL'), primary_key=True,nullable=False)
    projectId = Column(Integer, ForeignKey('project.projectId', ondelete='SET NULL'), primary_key=True,nullable=False)
    project = relationship("Project", back_populates="user_proj_map")
    flag = Column(BOOLEAN, nullable=True, default=True)

    def to_dict(self):
        return {
            'pk': self.projectId,
            'label': self.project.name,
            'item': 1,
            'openRank': self.project.openRank,
            'activity': self.project.activity,
            'stars': self.project.stars,
            'attention': self.project.attention,
            'technical_fork': self.project.technical_fork,
        }


class UserDevUserMap(Base):
    """用户开发者映射"""
    __tablename__ = 'user_devuser_map'
    userId = Column(Integer, ForeignKey('user.userId', ondelete='SET NULL'), primary_key=True,nullable=False)
    devUserId = Column(Integer, ForeignKey('devuser.devUserId',ondelete='SET NULL'), primary_key=True,nullable=False)
    dev_user = relationship("DevUser", back_populates="user_devuser_map")
    flag = Column(BOOLEAN, nullable=True, default=True)

    def to_dict(self):
        return {
            'pk': self.devUserId,
            'avatar_url': url_prefix + (self.dev_user.avatar_url or ''),
            'item': 2,
            'label': self.dev_user.name,
            'openRank': self.dev_user.openRank,
            'activity': self.dev_user.activity,
        }


Base.metadata.create_all(engine)
