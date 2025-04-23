<script setup>
import {computed, onMounted, reactive, ref} from "vue"
import router from "@/router";
import {useRoute} from "vue-router"
import {useStore} from "@/stores/app";
import {UploadFilled} from "@element-plus/icons-vue";
import {changePassword, setAvatar, Soul} from "@/api/dash";
import {upLoadUrl} from "@/api/base";
import UserCenterTableBase from "@/components/UserCenterTableBase.vue";

const route = useRoute()
const state = reactive({
  active: '1',
  password: '',
  soul: '',
  avatar: '',
})
const store = useStore()
const userinfo = computed(()=>store.userInfo)

const change_password = async () => {
  const res = await changePassword({password: state.password})
  if (res.data.code === 0) {
    await router.replace('Login')
  }
}
const set_avatar = async () => {
  const res = await setAvatar({avatar: state.avatar})
  if (res.data.code === 0) {
    store.userInfo.avatar_url = state.avatar
    state.avatar = ''
  }
}

const get_soul = async () => {
  const res = await Soul()
  state.soul = res.data
}

import {useDark, useToggle} from "@vueuse/core";

const isDark = useDark()
const toggleDark = useToggle(isDark)

onMounted(() => {
  get_soul()
  if (isDark.value) {
    toggleDark()
  }
})
</script>

<template>
  <div style="position: relative;display: flex;justify-content: space-between; align-items: center">
    <div class="gradient-text" style="margin: 0 50px;
                                              font-weight: bold;
                                              font-size: 2rem;
                                              flex: 1;
                                              text-align: center;

                                            "
    >{{ state.soul }}
    </div>
    <el-space>
    <div style="text-align: end;width: 300px;margin-right: 20px">
      <div class="text-18px  " style="color: purple">
        早安，{{ userinfo.username }}，开心每一天
      </div>
      <div class="mt-10px text-14px " style="color: purple">
        今天，18℃ - 24℃！
      </div>
      <el-space style="width: 100%; margin-top: 20px">
        <el-input v-model="state.password"></el-input>
        <el-button type="primary"
                   @click="change_password"
                   :disabled="state.password.trim()===''">修改密码
        </el-button>
      </el-space>


    </div>
    <el-space direction="vertical">
      <div class="ml-20px avatar-box" style="position: relative">
        <el-space class="avatar-mask" alignment="center" style="flex: 1;position: absolute; justify-content: center;
                width: 100%; height: 100%;border-radius: 50%; background: rgba(0,0,0,0.5)">
          <el-icon :size="60" style="color: #cdcdcd">
            <UploadFilled/>
          </el-icon>
        </el-space>
        <el-upload
          ref="giftUploadRef"
          :action="upLoadUrl"
          accept=".png, .jpg, .jpeg, .svg"
          :show-file-list="false"
          :on-success="(res)=>{state.avatar=res}"
        >
          <el-avatar
            v-if="state.avatar"
            :src="state.avatar"
            :size="160"
          >
          </el-avatar>
          <el-avatar
            v-else
            :src="userinfo.avatar_url"
            :size="160"
          />
        </el-upload>
      </div>
      <el-row justify="center">
        <el-space>
          <el-button type="primary" v-show="state.avatar" @click="set_avatar">保存</el-button>
        </el-space>
      </el-row>
    </el-space>
      </el-space>
  </div>

  <el-tabs v-model="state.active">
    <el-tab-pane  label="我关注的开发者" name="1">
      <UserCenterTableBase :item="2"></UserCenterTableBase>
    </el-tab-pane>
    <el-tab-pane  label="我关注的项目" name="2">
      <UserCenterTableBase :item="1"></UserCenterTableBase>
    </el-tab-pane>

  </el-tabs>
</template>

<style scoped lang="less">
.avatar-mask {
  opacity: 0;
  pointer-events: none;
  transition-duration: .3s;
}

.avatar-box:hover .avatar-mask {
  opacity: 1;

}

.gradient-text {
  font-family: system-ui;
  background-image: linear-gradient(to right, #d800af, #f19245);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>