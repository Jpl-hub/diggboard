import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const useStore = defineStore('app', () => {
  const loading = ref(true)
  const userInfo = ref({
    username: '',
    avatar_url:'',
    operateArr:[]
  })

  const sToken = ref()

  const get_token = () => {
    return sToken.value
  }
  const set_token = (token) => {
    sToken.value = token
  }
  const set_userinfo = (userinfo) => {
    userInfo.value = userinfo
  }


  return {
    loading,
    userInfo,
    sToken,
    get_token,
    set_token,
    set_userinfo,

  }
}, {
  persist: true,
})


export const useStoreWithOut = defineStore('appWithOut', () => {
  const imgPreviewOpen = ref(false)
  const initIndex = ref(0)
  const imgArr = ref([])


  const set_imgArr = (arr, index = 0) => {
    imgArr.value = arr
    initIndex.value = index
    imgPreviewOpen.value = true
  }

  return {
    imgPreviewOpen,
    initIndex,
    imgArr,
    set_imgArr,

  }
})
