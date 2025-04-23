<script setup>
import {useRoute, useRouter} from 'vue-router'
import {computed, onMounted, ref} from "vue";
import {useStore} from "@/stores/app";
import {ElMessageBox} from "element-plus";

const userInfo = computed(() => store.userInfo)


const router = useRouter()
const store = useStore()
const cardList = ref([])
const logout = () => {
  ElMessageBox.confirm('退出登录?', {
    closeOnClickModal: true,
    callback: (action) => {
      if (action === 'confirm') {
        store.set_userinfo({username: ''})
        store.set_token('')
        setTimeout(() => {
          router.push('/Login')
        }, 200)
      }
    },
  })

}

onMounted(async () => {

})


</script>

<template>
  <el-row justify="space-between" style="padding: 10px 10px 40px;width: 1200px;margin: auto;">
    <el-space alignment="center" @click="router.push('dashboard')" style="font-size: 20px;cursor: pointer">
      <img src="@/assets/img3.png" :width="60" alt="">
      <strong>DashBoard</strong>
    </el-space>

    <el-dropdown>
      <el-space style="cursor: pointer">
        <el-avatar :src="userInfo.avatar_url" :size="32"></el-avatar>
        <span>{{ userInfo.username }}</span>
      </el-space>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="router.push('usercenter')">个人中心</el-dropdown-item>
          <el-dropdown-item v-if="userInfo.operateArr.includes('admin')" @click="router.push('admin')">后台管理</el-dropdown-item>
          <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </el-row>
  <div
    style="box-shadow: 0 0 20px 0 white;width: 1200px;margin: auto;background: white; border-radius: 8px;padding: 20px">
    <router-view/>
  </div>
</template>

<style scoped>
</style>
