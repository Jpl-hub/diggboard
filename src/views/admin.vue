<script setup>
import {computed, onMounted, reactive, ref} from "vue";
import {
  addRole,
  addUser,
  deleteRole,
  deleteUser,
  getRoleList,
  getUserList,
  getOperateOps, updateRole, updateUser, getUserInfo
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
const userRef = ref()
const roleRef = ref()

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


const state = reactive({
  active: '1',
  userData: [],
  userColumns: [],
  userTotal: 0,
  roleData: [],
  roleColumns: [],
  roleTotal: 0,
  operateOps: [],
  userDialogShow: false,
  roleDialogShow: false,
  type: ''
})
onMounted(() => {
  get_roleList()
  get_userList()
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
      </el-space>
      <el-table :data="state.userData">
        <el-table-column v-for="cc in state.userColumns" :label="cc.label">
          <template #default="scope">
            <el-avatar v-if="cc.key==='avatar_url'" :src="scope.row[cc.key]"></el-avatar>
            <el-space v-else-if="cc.key==='operate'">
              <el-button type="primary" v-if="userInfo.operateArr.includes('updateUser')"
                         @click="userForm = _.cloneDeep(scope.row);state.userDialogShow=true">编辑
              </el-button>
              <div v-if="userInfo.operateArr.includes('deleteUser')">
                <el-button type="danger" v-show="scope.row.pk!==userInfo.userId"
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
      </el-space>
      <el-table :data="state.roleData">
        <el-table-column v-for="cc in state.roleColumns" :label="cc.label">
          <template #default="scope">
            <el-avatar v-if="cc.key==='avatar_url'" :src="scope.row[cc.key]"></el-avatar>
            <el-space v-else-if="cc.key==='operate'">
              <el-button type="primary"
                         @click="roleForm = _.cloneDeep(scope.row);state.roleDialogShow=true;console.log(scope.row)">编辑
              </el-button>
              <el-button type="danger" @click="delete_role(scope.row)">删除</el-button>
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
</template>

<style scoped lang="less">

</style>