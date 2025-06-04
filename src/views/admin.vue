<script setup>
import {computed, onMounted, reactive, ref} from "vue";
import {
  addRole,
  addUser,
  deleteRole,
  deleteUser,
  getRoleList,
  getUserList,
  getOperateOps, updateRole, updateUser, getUserInfo,
  // 项目管理
  getProjectList,
  addProject,
  updateProject,
  deleteProject,
  // 开发者管理
  getDevUserList,
  addDevUser,
  updateDevUser,
  deleteDevUser
} from "@/api/dash";
import {useStore} from "@/stores/app";
import _ from "lodash"
import {ElMessageBox} from "element-plus";


const store = useStore()
const userInfo = computed(() => store.userInfo)
const userForm = ref({
  username: '',
  password: '',
  roleId: '',
})

const roleForm = ref({
  roleName: '',
  operateArr: [],
})

const projectForm = ref({
  name: '',
  platform: '',
  openRank: 0,
  activity: 0,
  stars: 0,
  attention: 0,
  technical_fork: 0,
})

const devUserForm = ref({
  name: '',
  platform: '',
  openRank: 0,
  activity: 0,
  repos: 0,
  stars: 0,
  technical_fork: 0,
})

const userRef = ref()
const roleRef = ref()
const projectRef = ref()
const devUserRef = ref()

const get_userList = async () => {
  const res = await getUserList()
  state.userData = res.data.data.data
  state.userColumns = res.data.data.columns
  state.userTotal = res.data.data.total
}
const add_user = async () => {
  userRef.value.validate(async (v) => {
    if (v) {
      // 确保 roleId 是数字类型或 null
      if (userForm.value.roleId === '' || userForm.value.roleId === undefined) {
        userForm.value.roleId = null;
      } else {
        userForm.value.roleId = Number(userForm.value.roleId);
      }
      
      console.log('添加用户数据:', userForm.value); // 调试信息
      
      const res = await addUser(userForm.value)
      if (res.data.code === 0) {
        await get_userList()
        state.userDialogShow = false
      }
    }
  })
}
const edit_user = async () => {
  userRef.value.validate(async (v) => {
    if (v) {
      // 确保 roleId 是数字类型或 null
      if (userForm.value.roleId === '' || userForm.value.roleId === undefined) {
        userForm.value.roleId = null;
      } else {
        userForm.value.roleId = Number(userForm.value.roleId);
      }
      
      console.log('发送的用户数据:', userForm.value); // 调试信息
      
      const res = await updateUser(userForm.value)
      if (res.data.code === 0) {
        await get_userList()
        state.userDialogShow = false
      }
    }
  })
}
const delete_user = (row) => {
  ElMessageBox.confirm('确认删除?', {
    closeOnClickModal: true,
    callback: async (action) => {
      if (action === 'confirm') {
        const res = await deleteUser({pk: row.pk})
        if (res.data.code === 0) {
          await get_userList()
        }
      }
    },
  })

}
const get_roleList = async () => {
  const res = await getRoleList()
  state.roleData = res.data.data.data
  state.roleColumns = res.data.data.columns
  state.roleTotal = res.data.data.total
}
const add_role = async () => {
  roleRef.value.validate(async (v) => {
    if (v) {
      const res = await addRole(roleForm.value)
      if (res.data.code === 0) {
        await get_roleList()
        state.roleDialogShow = false
      }
    }
  })

}
const delete_role = (row) => {
  ElMessageBox.confirm('确认删除?', {
    closeOnClickModal: true,
    callback: async (action) => {
      if (action === 'confirm') {
        const res = await deleteRole({pk: row.pk})
        if (res.data.code === 0) {
          await get_roleList()
        }
      }
    },
  })

}

const edit_role = async () => {
  roleRef.value.validate(async (v) => {
    if (v) {
      const res = await updateRole(roleForm.value)
      if (res.data.code === 0) {
        await get_roleList()
        const user_res = await getUserInfo()
        store.set_userinfo(user_res.data.data)
        state.roleDialogShow = false
      }
    }
  })
}

const openRole = () => {
  state.roleDialogShow = true
  roleForm.value = {
    roleName: '',
    operateArr: [],
  }
}

const openUser = () => {
  state.userDialogShow = true
  userForm.value = {
    username: '',
    password: '',
    roleId: '',
  }
}

const get_operate_ops = async () => {
  const res = await getOperateOps()
  state.operateOps = res.data
}

// 项目管理函数
const get_projectList = async () => {
  const res = await getProjectList()
  state.projectData = res.data.data.data
  state.projectColumns = res.data.data.columns
  state.projectTotal = res.data.data.total
}

const add_project = async () => {
  projectRef.value.validate(async (v) => {
    if (v) {
      const res = await addProject(projectForm.value)
      if (res.data.code === 0) {
        await get_projectList()
        state.projectDialogShow = false
      }
    }
  })
}

const edit_project = async () => {
  projectRef.value.validate(async (v) => {
    if (v) {
      const res = await updateProject(projectForm.value)
      if (res.data.code === 0) {
        await get_projectList()
        state.projectDialogShow = false
      }
    }
  })
}

const delete_project = (row) => {
  ElMessageBox.confirm('确认删除?', {
    closeOnClickModal: true,
    callback: async (action) => {
      if (action === 'confirm') {
        const res = await deleteProject({pk: row.pk})
        if (res.data.code === 0) {
          await get_projectList()
        }
      }
    },
  })
}

const openProject = () => {
  state.projectDialogShow = true
  projectForm.value = {
    name: '',
    platform: 'github',
    openRank: 0,
    activity: 0,
    stars: 0,
    attention: 0,
    technical_fork: 0,
  }
}

// 开发者管理函数
const get_devUserList = async () => {
  const res = await getDevUserList()
  state.devUserData = res.data.data.data
  state.devUserColumns = res.data.data.columns
  state.devUserTotal = res.data.data.total
}

const add_devUser = async () => {
  devUserRef.value.validate(async (v) => {
    if (v) {
      const res = await addDevUser(devUserForm.value)
      if (res.data.code === 0) {
        await get_devUserList()
        state.devUserDialogShow = false
      }
    }
  })
}

const edit_devUser = async () => {
  devUserRef.value.validate(async (v) => {
    if (v) {
      const res = await updateDevUser(devUserForm.value)
      if (res.data.code === 0) {
        await get_devUserList()
        state.devUserDialogShow = false
      }
    }
  })
}

const delete_devUser = (row) => {
  ElMessageBox.confirm('确认删除?', {
    closeOnClickModal: true,
    callback: async (action) => {
      if (action === 'confirm') {
        const res = await deleteDevUser({pk: row.pk})
        if (res.data.code === 0) {
          await get_devUserList()
        }
      }
    },
  })
}

const openDevUser = () => {
  state.devUserDialogShow = true
  devUserForm.value = {
    name: '',
    platform: 'github',
    openRank: 0,
    activity: 0,
    repos: 0,
    stars: 0,
    technical_fork: 0,
  }
}

const state = reactive({
  active: '1',
  userData: [],
  userColumns: [],
  userTotal: 0,
  roleData: [],
  roleColumns: [],
  roleTotal: 0,
  projectData: [],
  projectColumns: [],
  projectTotal: 0,
  devUserData: [],
  devUserColumns: [],
  devUserTotal: 0,
  operateOps: [],
  userDialogShow: false,
  roleDialogShow: false,
  projectDialogShow: false,
  devUserDialogShow: false,
  type: ''
})
onMounted(() => {
  get_roleList()
  get_userList()
  get_projectList()
  get_devUserList()
  get_operate_ops()
})
</script>

<template>
  <el-tabs v-model="state.active">
    <el-tab-pane v-if="userInfo.operateArr.includes('userManager')" name="1" label="用户管理">
      <el-space>
        <el-button v-if="userInfo.operateArr.includes('addUser')"
                   @click="openUser"
                   type="primary">添加用户
        </el-button>
      </el-space>      <el-table :data="state.userData">
        <el-table-column v-for="cc in state.userColumns" :label="cc.label" :width="cc.key === 'operate' ? 200 : undefined">
          <template #default="scope">
            <el-avatar v-if="cc.key==='avatar_url'" :src="scope.row[cc.key]"></el-avatar>
            <el-space v-else-if="cc.key==='operate'" :size="8">
              <el-button type="primary" size="small" v-if="userInfo.operateArr.includes('updateUser')"
                         @click="userForm = _.cloneDeep(scope.row);state.userDialogShow=true">编辑
              </el-button>
              <div v-if="userInfo.operateArr.includes('deleteUser')">
                <el-button type="danger" size="small" v-show="scope.row.pk!==userInfo.userId"
                           @click="delete_user(scope.row)">删除
                </el-button>
              </div>
            </el-space>
            <div v-else>{{ scope.row[cc.key] }}</div>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane v-if="userInfo.operateArr.includes('roleManager')" name="2" label="角色管理">
      <el-space>
        <el-button v-if="userInfo.operateArr.includes('addRole')"
                   @click="openRole"
                   type="primary">添加角色
        </el-button>
      </el-space>      <el-table :data="state.roleData">
        <el-table-column v-for="cc in state.roleColumns" :label="cc.label" :width="cc.key === 'operate' ? 200 : undefined">
          <template #default="scope">
            <el-avatar v-if="cc.key==='avatar_url'" :src="scope.row[cc.key]"></el-avatar>
            <el-space v-else-if="cc.key==='operate'" :size="8">
              <el-button type="primary" size="small"
                         @click="roleForm = _.cloneDeep(scope.row);state.roleDialogShow=true;console.log(scope.row)">编辑
              </el-button>
              <el-button type="danger" size="small" @click="delete_role(scope.row)">删除</el-button>
            </el-space>
            <div v-else>{{ scope.row[cc.key] }}</div>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    
    <!-- 项目管理 -->
    <el-tab-pane v-if="userInfo.operateArr.includes('admin')" name="3" label="项目管理">
      <el-space>
        <el-button @click="openProject" type="primary">添加项目</el-button>
      </el-space>      <el-table :data="state.projectData">
        <el-table-column v-for="cc in state.projectColumns" :label="cc.label" :width="cc.key === 'operate' ? 200 : undefined">
          <template #default="scope">
            <el-space v-if="cc.key==='operate'" :size="8">
              <el-button type="primary" size="small" @click="projectForm = _.cloneDeep(scope.row);state.projectDialogShow=true">编辑</el-button>
              <el-button type="danger" size="small" @click="delete_project(scope.row)">删除</el-button>
            </el-space>
            <div v-else>{{ scope.row[cc.key] }}</div>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    
    <!-- 开发者管理 -->
    <el-tab-pane v-if="userInfo.operateArr.includes('admin')" name="4" label="开发者管理">
      <el-space>
        <el-button @click="openDevUser" type="primary">添加开发者</el-button>
      </el-space>      <el-table :data="state.devUserData">
        <el-table-column v-for="cc in state.devUserColumns" :label="cc.label" :width="cc.key === 'operate' ? 200 : undefined">
          <template #default="scope">
            <el-avatar v-if="cc.key==='avatar_url'" :src="scope.row[cc.key]"></el-avatar>
            <el-space v-else-if="cc.key==='operate'" :size="8">
              <el-button type="primary" size="small" @click="devUserForm = _.cloneDeep(scope.row);state.devUserDialogShow=true">编辑</el-button>
              <el-button type="danger" size="small" @click="delete_devUser(scope.row)">删除</el-button>
            </el-space>
            <div v-else>{{ scope.row[cc.key] }}</div>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
  </el-tabs>

  <el-dialog v-model="state.userDialogShow"
             width="600"
             style=""
  >
    <div style="display: flex; flex-direction: column; justify-content: space-between;min-height: 400px;">
      <el-form :model="userForm"
               label-width="80px"
               style="margin: 20px"
               ref="userRef"
               :rules="{
                    username:[{required:true, trigger: 'blur', message:'输入用户名'}],
                    password:[{required:!userForm.pk, trigger: 'blur', message:'输入密码'}],
             }"
      >
        <el-form-item label="用户名" prop="username">
          <el-input clearable v-model="userForm.username"></el-input>
        </el-form-item>
        <el-form-item v-if="!userForm.pk" label="密码" prop="password">
          <el-input clearable type="password" show-password v-model="userForm.password"></el-input>
        </el-form-item>        <el-form-item label="选择角色">
          <el-select v-model="userForm.roleId" clearable placeholder="请选择角色">
            <el-option v-for="rr in state.roleData"
                       :label="rr.roleName"
                       :value="rr.pk"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-row justify="center" style="margin-top: 50px">
        <el-button type="primary" @click="userForm.pk ?edit_user():add_user()">保存</el-button>
      </el-row>
    </div>

  </el-dialog>
  <el-dialog v-model="state.roleDialogShow"
             width="600"
             style=""
  >
    <div style="display: flex; flex-direction: column; justify-content: space-between;min-height: 400px;">
      <el-form :model="roleForm"
               label-width="80px"
               style="margin: 20px"
               ref="roleRef"
               :rules="{
             roleName:[{required:true, trigger: 'blur', message:'输入角色名'}]
             }"
      >
        <el-form-item label="角色名" prop="roleName">
          <el-input clearable v-model="roleForm.roleName"></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-select v-model="roleForm.operateArr" multiple>
            <el-option v-for="oo in state.operateOps" :label="oo.label" :value="oo.value"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-row justify="center" style="">
        <el-button type="primary" @click="roleForm.pk? edit_role():add_role()">保存</el-button>
      </el-row>
    </div>

  </el-dialog>
  
  <!-- 项目管理对话框 -->
  <el-dialog v-model="state.projectDialogShow" width="600">
    <div style="display: flex; flex-direction: column; justify-content: space-between;min-height: 400px;">
      <el-form :model="projectForm"
               label-width="100px"
               style="margin: 20px"
               ref="projectRef"
               :rules="{
                 name:[{required:true, trigger: 'blur', message:'输入项目名称'}],
                 platform:[{required:true, trigger: 'blur', message:'选择平台'}]
               }"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input clearable v-model="projectForm.name"></el-input>
        </el-form-item>
        <el-form-item label="平台" prop="platform">
          <el-select v-model="projectForm.platform">
            <el-option label="GitHub" value="github"></el-option>
            <el-option label="Gitee" value="gitee"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="OpenRank">
          <el-input-number v-model="projectForm.openRank" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="活跃度">
          <el-input-number v-model="projectForm.activity" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="Stars">
          <el-input-number v-model="projectForm.stars" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="关注度">
          <el-input-number v-model="projectForm.attention" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="Fork数">
          <el-input-number v-model="projectForm.technical_fork" :min="0"></el-input-number>
        </el-form-item>
      </el-form>
      <el-row justify="center" style="margin-top: 50px">
        <el-button type="primary" @click="projectForm.pk ? edit_project() : add_project()">保存</el-button>
      </el-row>
    </div>
  </el-dialog>
  
  <!-- 开发者管理对话框 -->
  <el-dialog v-model="state.devUserDialogShow" width="600">
    <div style="display: flex; flex-direction: column; justify-content: space-between;min-height: 400px;">
      <el-form :model="devUserForm"
               label-width="100px"
               style="margin: 20px"
               ref="devUserRef"
               :rules="{
                 name:[{required:true, trigger: 'blur', message:'输入开发者名称'}],
                 platform:[{required:true, trigger: 'blur', message:'选择平台'}]
               }"
      >
        <el-form-item label="开发者名称" prop="name">
          <el-input clearable v-model="devUserForm.name"></el-input>
        </el-form-item>
        <el-form-item label="平台" prop="platform">
          <el-select v-model="devUserForm.platform">
            <el-option label="GitHub" value="github"></el-option>
            <el-option label="Gitee" value="gitee"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="OpenRank">
          <el-input-number v-model="devUserForm.openRank" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="活跃度">
          <el-input-number v-model="devUserForm.activity" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="仓库数">
          <el-input-number v-model="devUserForm.repos" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="Stars总数">
          <el-input-number v-model="devUserForm.stars" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="被Fork数">
          <el-input-number v-model="devUserForm.technical_fork" :min="0"></el-input-number>
        </el-form-item>
      </el-form>
      <el-row justify="center" style="margin-top: 50px">
        <el-button type="primary" @click="devUserForm.pk ? edit_devUser() : add_devUser()">保存</el-button>
      </el-row>
    </div>
  </el-dialog>
</template>

<style scoped lang="less">
/* 管理页面整体样式 */
.el-tabs {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 20px;
  margin: 20px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

/* 标签页头部样式 */
:deep(.el-tabs__header) {
  margin-bottom: 20px;
}

:deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
  padding: 0 30px;
}

:deep(.el-tabs__item.is-active) {
  color: #3b82f6;
  font-weight: 600;
}

:deep(.el-tabs__active-bar) {
  background-color: #3b82f6;
  height: 3px;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  margin-top: 16px;
}

:deep(.el-table__header-wrapper) {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}

:deep(.el-table th) {
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
  color: #475569;
}

:deep(.el-table td) {
  border-bottom: 1px solid #f1f5f9;
}

:deep(.el-table__row):hover {
  background-color: rgba(59, 130, 246, 0.05);
}

/* 操作按钮优化 */
.el-button {
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.el-button--primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border: none;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.el-button--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.el-button--danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: none;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.el-button--danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

/* 对话框样式 */
:deep(.el-dialog) {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 80px rgba(0, 0, 0, 0.2);
}

:deep(.el-dialog__header) {
  padding: 24px 24px 12px;
  border-bottom: 1px solid #f1f5f9;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

/* 表单样式 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.2);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 头像样式 */
:deep(.el-avatar) {
  border: 2px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 选择器样式 */
:deep(.el-select .el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-select-dropdown) {
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

/* 标签样式 */
:deep(.el-tag) {
  border-radius: 6px;
  font-weight: 500;
}

/* 空间间距 */
.el-space {
  margin-bottom: 16px;
}
</style>