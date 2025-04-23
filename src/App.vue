<script setup>
import {useRoute, useRouter} from 'vue-router'
import {useStore, useStoreWithOut} from "@/stores/app";
import {computed, h, onMounted, reactive, ref, render} from "vue";

const store = useStore()
const storeWithOut = useStoreWithOut()
const router = useRouter()
const route = useRoute()
const userInfo = computed(() => store.userInfo)

const html = document.documentElement;

// 封装一个函数
function fontS() {
  // 获取 html 的宽
  let hW = html.offsetWidth;
  /* 计算字体大小（一般UI设计图是根据iPhone6的屏幕宽度设计的，即 宽为 750px）
  当 html 宽度大于 750px 时，html 的 font-size 为 100px;
  当 html 宽度小于 750px 时，html 的 font-size 为 html 宽度除以 7.5 (方便计算); 可以按自己的习惯设置 */
  let hS;
  if (hW > 1200) {
    hS = 14;
  } else {
    hS = hW / 100;
  }
  // 给的 html 设置字体大小
  html.style.fontSize = hS + "px";
}


onMounted(() => {
  window.addEventListener('resize', function () {
    fontS()
  })
})


</script>
<template>

  <router-view/>

</template>


<style>

</style>
