<script setup>


import {ref} from "vue";

const props = defineProps({
  src: {},
  width: {default: '200px'},
  height: {default: '100px'},
  fit: {default: 'cover'}
})

const item = ref({
  src: props.src,
  show: false
})
</script>


<template>
  <div :style="{width: width,height: height,}"
       style="display: flex;
    justify-content: center;
    align-items: center;
           background: rgba(0,0,0,.8);">
    <transition name="fade">
      <van-image
        block
        v-show="item.show"
        :width="width"
        :height="height"
        :src="item.src"
        :fit="fit"
        alt="Your Image"
        @load="item.show=true"
      >
        <template #loading>
        </template>
      </van-image>
    </transition>
    <van-loading type="spinner" v-show="!item.show"
                 :size="30"></van-loading>
  </div>


</template>


<style>

</style>
