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
  <el-row justify="space-between" style="padding: 10px 10px 40px;width: 1200px;margin: auto;">    <el-space alignment="center" @click="router.push('dashboard')" style="font-size: 20px;cursor: pointer" class="logo-section">
      <img src="@/assets/dashboard-icon.svg" :width="60" alt="Dashboard Icon">
      <strong class="logo-text">开源生态数据分析可视化平台</strong>
    </el-space><el-dropdown>
      <el-space style="cursor: pointer" class="user-dropdown">
        <el-avatar :src="userInfo.avatar_url" :size="32"></el-avatar>
        <span class="username-text">{{ userInfo.username }}</span>
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
.logo-section {
  transition: all 0.3s ease;
}

.logo-section:hover {
  transform: translateY(-2px);
}

.logo-text {
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  font-size: 20px;
  font-weight: 700;
}

.user-dropdown {
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
  transition: all 0.3s ease;
}

.user-dropdown:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.3);
}

.username-text {
  color: white;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  font-size: 16px;
}
</style>
