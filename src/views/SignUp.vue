<script setup>
import {onMounted, reactive, ref} from "vue";
import {useRoute, useRouter} from "vue-router";

import {useStore} from "@/stores/app";
import {getUserInfo, SignUp} from "@/api/dash";
import {Lock, User} from "@element-plus/icons-vue";

const route = useRoute()
const router = useRouter()
const store = useStore()

const state = reactive({})
const form = ref({
  username: "",
  password: "",
  password1: "",
})
const formRef = ref()
const toSignUp = async () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      const res = await SignUp(form.value)
      if (res.data.code === 0) {
        await store.set_token(res.data.data)
        const user_res = await getUserInfo()
        store.set_userinfo(user_res.data.data)
        await router.push("/dashboard")
      }

    }
  })

}
const aa = ref(false)
onMounted(() => {
  aa.value = !aa.value
})
</script>

<template>
  <div style="position: fixed; top:100px; left: 20%;font-size: 1.5rem; font-weight: bold">DashBoard</div>
  <transition name="fade-up">
    <el-card v-if="aa"
             style="position: absolute;top:200px;left:0;right:0;margin: auto;display: flex;
     justify-content: center;align-items: center; width: 400px;height: 500px;">
      <div style="display: flex;flex-direction: column;justify-content:center;
    align-items: center;
    margin: 20px 0 30px; font-weight: bold;font-size: 1.5rem;color:#265f99">
        账号注册
        <div style="width: 24px;margin-top: 10px; height: 5px;border-radius: 5px;
      background-color: #265f99"></div>
      </div>
      <el-form
        ref="formRef"
        style="width: 300px"
        :model="form"
        label-width="auto"
        :rules="{
        username:[
          {required: true, min:3, max: 12, trigger: 'blur',message:'请输入用户名'}
        ],
        password:[
          {required: true, min:3, max: 12, trigger: 'blur',message:'请输入密码'}
        ],
        password1:[
          {required: true, min:3, max: 12, trigger: 'blur',message:'请确认密码'}
        ],
      }"
        class="demo-dynamic"
      >
        <el-form-item
          prop="username"
        >
          <el-input size="large" placeholder="用户名" v-model="form.username">
            <template #prefix>
              <el-icon>
                <User/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item
          prop="password"
        >
          <el-input size="large" clearable type="password" show-password
                    placeholder="密码" v-model="form.password">
            <template #prefix>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item
          prop="password1"
        >
          <el-input size="large" clearable type="password" show-password
                    placeholder="确认密码" v-model="form.password1">
            <template #prefix>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>


      </el-form>
      <el-row justify="space-between">
        <el-button type="text" size="small" @click="router.push('Login')">去登录</el-button>
      </el-row>

      <div style="margin-top: 20px">
        <el-button type="primary" style="width: 100%" @click="toSignUp">立即注册</el-button>
      </div>

    </el-card>
  </transition>

</template>

<style scoped lang="less">
/* 动画定义 */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all .3s linear; /* 动画持续时间 */
}

.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0; /* 初始状态为完全透明 */
  transform: translateY(20px); /* 初始状态向下偏移 20px */
}

.fade-up-enter-to,
.fade-up-leave-from {
  opacity: 1; /* 最终状态为完全不透明 */
  transform: translateY(0); /* 最终状态回到原位置 */
}
</style>
