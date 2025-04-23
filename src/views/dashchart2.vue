<script setup>
import {onMounted, onUnmounted, reactive, ref} from "vue";
import {useStore} from "@/stores/app";
import {useRoute} from "vue-router";
import {chartData2} from "@/api/dash";
import Echarts from "@/components/Echarts.vue";
import VanillaTilt from 'vanilla-tilt'
import * as echarts from 'echarts';
import {combineBase} from "@/libs/combine";
import _ from 'lodash'

import {useDark, useToggle} from "@vueuse/core";

const isDark = useDark()
const toggleDark = useToggle(isDark)


const route = useRoute()
const store = useStore()

const state = reactive({
  indicator: [],
  otherIndicator: [],
  combine: {},
  eventArr: [],
  eventColumns: [],
  reposArr: [],
  reposColumns: [],
  show: false
})
const get_data = async () => {
  const combine = _.cloneDeep(combineBase)
  const res = await chartData2({u_id: route.query.pk})
  state.eventArr = res.data.eventArr
  state.eventColumns = res.data.eventColumns
  state.reposArr = res.data.reposArr
  state.reposColumns = res.data.reposColumns

  combine.series = res.data.series
  combine.xAxis[0].data = res.data.xAxis
  combine.yAxis = res.data.yAxis
  combine.legend.data = res.data.legend
  state.combine = combine

  state.indicator = res.data.indicator
  state.otherIndicator = res.data.otherIndicator
  state.title = res.data.title
  state.show = true
}
onMounted(() => {
  get_data()
  VanillaTilt.init(document.querySelectorAll('.ccard'), {
    max: 15, // 最大倾斜角度
    speed: 800, // 倾斜速度
    glare: true, // 是否启用反光效果
    "max-glare": 0.3 // 最大反光程度
  })

  if (!isDark.value) {
    toggleDark();
  }


})
onUnmounted(() => {


})
</script>

<template>
  <div class="aa" style="">
    <div style="padding: 20px 0;display: flex; justify-content: center;
    align-items: center;color: #ffffff; font-size: 2rem;font-weight: bold">
      {{ state.title }}
    </div>
    <div v-if="state.show" style="display: flex;height: calc(100% - 90px); flex-direction: column;width: 100%;
  justify-content: space-around;">
      <div style="flex: 1;display: flex; justify-content: center">
        <div style="width: 80%;height: 100%;display: flex;justify-content:space-around;align-items: center;">
          <div v-for="item in state.indicator" class="indicator-item" style="color:white;width: 280px">
            <img src="@/assets/4.png" alt="" style="width:100%;">
            <div style="position: absolute;width: 100%; height: 100%;left:0;top:0;display: flex;flex-direction: column;
            justify-content: center;align-items: center;">
              <div style="font-size: 1.5rem">{{ item.label }}</div>
              <span style="font-size: 3rem;color:#ffd900;font-weight: bold">{{ item.value }}</span>
            </div>
          </div>
        </div>
      </div>
      <div style="height: 500px;display: flex;margin: 20px 0">
        <div class="chart-item" style="flex: 1;margin:0 10px;">
          <Echarts style="flex: 1" width="100%" :options="state.combine"></Echarts>
        </div>
        <div style="flex: 1;margin: 0 20px;display: grid; grid-template-columns: repeat(3,1fr);grid-gap:20px;">
          <div v-for="item in state.otherIndicator" class="indicator-item" style="color:white;">
            <img src="@/assets/6.png" alt="" style="width:100%;">
            <div style="position: absolute;width: 100%; height: 100%;left:0;top:0;display: flex;flex-direction: column;
            justify-content: center;align-items: center;">
              <div style="font-size: 1.5rem;margin-bottom: 20px;color:#0be700">{{ item.label }}</div>
              <span style="font-size:3rem;color:#ffffff;font-weight: bold">{{ item.value }}</span>
            </div>
          </div>

        </div>


      </div>
      <div style="height: 500px;display: flex;">
        <div style="flex: 1;margin:0 10px;">
          <div style="color: #fff;text-align: center;font-weight: bold;
          padding: 10px 0;background: #063954">近期活跃事件
          </div>
          <div class="chart-item" style="overflow-y: scroll;">

            <el-table :data="state.eventArr" class="dark-table" style="">
              <el-table-column v-for="cc in state.eventColumns" :label="cc.label" :prop="cc.key">
                <template #default="scope">
                  <a v-if="cc.key==='full_name'" :href="scope.row.html_url"
                     target="_blank">{{ scope.row.full_name }}</a>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
        <div style="flex: 1;margin: 0 10px;">
          <div style="color: #fff;text-align: center;font-weight: bold;
          padding: 10px 0;background: #063954">仓库列表
          </div>
          <div class="chart-item" style="overflow-y: scroll;">
            <el-table :data="state.reposArr" class="dark-table" style="">
              <el-table-column v-for="cc in state.reposColumns" :label="cc.label" :prop="cc.key">
                <template #default="scope">
                  <a v-if="cc.key==='full_name'" :href="scope.row.html_url"
                     target="_blank">{{ scope.row.full_name }}</a>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

      </div>
    </div>

    <img v-else src="@/assets/loading.svg" style="width: 100px;position: fixed;inset: 0;margin: auto" alt="">
  </div>


</template>

<style  lang="less">


.indicator-item {
  padding: 10px;
  position: relative;
}

.chart-item {
  padding: 10px;
  border-radius: 10px;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
}

.aa {
  position: fixed;
  overflow-y: scroll;
  inset: 0;
  background: url('@/assets/img_1.png') no-repeat center/cover fixed
}

.ccard {
  min-width: 200px;
  padding: 20px;
  flex: 1;
  border-radius: 10px;
  color: #f1f1f1;
  font-weight: 700;
  transition-duration: .3s;
}

.card-title {
  font-size: 1.2rem;
}

.total-title {
  font-size: 1rem;
  font-weight: bold;
}

.total-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.amount {
  //background: linear-gradient(to bottom, #f90048, #ee4d7c)
  background: linear-gradient(to bottom, rgba(5, 120, 222, 0.59), rgba(7, 168, 217, 0.69))
}

.ticket {
  background: linear-gradient(to bottom, #f05b04, #ea8307)
}

.off {
  background: linear-gradient(to bottom, #0578de, #07a8d9)
}
</style>
