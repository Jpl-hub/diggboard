import axios from "axios"
import {useStore} from "@/stores/app"
import {ElMessage} from "element-plus";
import router from "@/router";

export const upLoadUrl = import.meta.env.DEV 
  ? import.meta.env.VITE_UPLOAD_URL_DEV || 'http://127.0.0.1:7777/api/Upload' 
  : import.meta.env.VITE_UPLOAD_URL_PROD || 'https://hubeixiyao.cn/vote/user/UploadToOss'

export const maxImgSize = {text: '5M', size: 1024 * 1024 * 5}
const instance = axios.create({
  baseURL: '/api',
})

instance.interceptors.request.use(
  config => {
    const store = useStore()
    const token = store.get_token()
    if (token) {
      config.headers.token = 'Bearer ' + token
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)
instance.interceptors.response.use(
  response => {
    if (response.data.code === 400) {
      return ElMessage.error(response.data.message)
    }
    if (response.data.code === 401) {
      ElMessage.error(response.data.message)
      return router.push('/Login')

    }
    if (response.data.message) {
      ElMessage.success(response.data.message)
    }

    return response
  },
  error => {
    if (error.status === 422) {
      return ElMessage.error('参数错误')
    }
    ElMessage.error('服务器错误')

  }
)
export {
  instance,
}
