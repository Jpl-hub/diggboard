import App from './App.vue'
import {createApp} from 'vue'
import router from './router'
import myPinia from "@/stores";

import './assets/main.css'
import './assets/iconfont/iconfont.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// main.js 文件
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/assets/element-dark.less'

import zhCn from 'element-plus/es/locale/lang/zh-cn';



const app = createApp(App)


app.use(myPinia)
app.use(router)
app.use(ElementPlus,{
    locale: zhCn,
})

app.mount('#app')
