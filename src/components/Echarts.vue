<script setup>
import {computed, onMounted, reactive, ref, onUpdated, shallowRef} from "vue"
import {useRoute} from "vue-router"
import * as echarts from 'echarts';

const route = useRoute()
const state = reactive({})
const chart = shallowRef()
const chartRef = ref()

const props = defineProps({
    options: {
      type: Object,
      required: true
    },
    width: {
      type: String,
      default: '800px'
    },
    height: {
      type: String,
      default: '500px'
    }
  }
)


onMounted(() => {
  chart.value = echarts.init(chartRef.value, 'dark')
  props.options.backgroundColor = 'rgba(0,0,0,0)'
  chart.value.setOption(props.options)
  window.addEventListener('resize', () => {
    chart.value.resize()
  })

})

onUpdated(() => {
  if (chart.value) {
    chart.value.clear()
    chart.value.setOption(props.options)
  }

})
</script>

<template>
  <div ref="chartRef" style="width: 100%; height: 100%"></div>
</template>

<style scoped lang="less">

</style>