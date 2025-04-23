import {maxImgSize} from "@/api/base";
import {useStore} from "@/stores/app";


export const get_openId_code = (ascope) => {
    const store = useStore()
    if (ascope === 'snsapi_base' && store.get_token()) return
    const userAgent = navigator.userAgent.toLowerCase()
    // && !import.meta.env.DEV
    if (userAgent.includes('micromessenger')) {
        const redirect_uri = encodeURIComponent(window.location.href)
        window.location.href = `https://jjj.hubeixiyao.cn?redirect_uri=${redirect_uri}&appId=${store.appId}&ascope=${ascope}`
        return false
    }
}

export const countDownTime = (time, type) => {
    var nowtime = new Date(), //获取当前时间
        endtime = new Date(time).getTime(); //定义结束时间
    let timestamp = endtime - nowtime.getTime(); //距离结束时间的毫秒数
    if (timestamp < 0) {
        return "截止了"
    }
    let D = Math.floor(timestamp / (1000 * 60 * 60 * 24)); //计算天数
    let H = Math.floor(timestamp / (1000 * 60 * 60) % 24); //计算小时数
    let m = Math.floor(timestamp / (1000 * 60) % 60); //计算分钟数
    let s = Math.floor(timestamp / 1000 % 60); //计算秒数
    if (H < 10) {
        H = '0' + H
    }
    if (m < 10) {
        m = '0' + m
    }
    if (s < 10) {
        s = '0' + s
    }
    if (type === 1) {
        return `${D}天${H}时${m}分${s}秒`
    } else {
        return `${H}时${m}分${s}秒`
    }
}

export const formatterDate = (date, type) => {
    const time = date ? new Date(date) : new Date();
    const year = time.getFullYear() // 获取年
    const month = time.getMonth() + 1 < 10 ? '0' + (time.getMonth() + 1) : time.getMonth() + 1 // 获取月
    const day = time.getDate() < 10 ? '0' + time.getDate() : time.getDate() // 获取日
    const hour = time.getHours() < 10 ? '0' + time.getHours() : time.getHours() // 获取小时
    const minute = time.getMinutes() < 10 ? '0' + time.getMinutes() : time.getMinutes() // 获取分钟
    const second = time.getSeconds() < 10 ? '0' + time.getSeconds() : time.getSeconds() // 获取秒
    if (type === 'y') {
        return year + ''
    } else if (type === 'm') {
        return year + month + ''
    } else {
        return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
    }
}

export const onOversize = (file) => {
    const size = (file.file.size / 1024 / 1024).toFixed(1)
}