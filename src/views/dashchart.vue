<script setup>
import {onMounted, reactive, ref} from "vue";
import {useStore} from "@/stores/app";
import {useRoute} from "vue-router";
import {chartData} from "@/api/dash";
import Echarts from "@/components/Echarts.vue";
import VanillaTilt from 'vanilla-tilt'
import * as echarts from 'echarts';
import {openRankBase} from "@/libs/openRank";
import {technical_forkBase} from "@/libs/technical_fork";
import {starsBase} from "@/libs/stars";
import {activityBase} from "@/libs/activity";
import {attentionBase} from "@/libs/attention";
import _ from 'lodash'

const route = useRoute()
const store = useStore()

const state = reactive({
  indicator: [],
  openRank: {},
  technical_fork: {},
  stars: {},
  activity: {},
  attention: {},
  show: false
})
const get_data = async () => {
  const openRank = _.cloneDeep(openRankBase)
  const technical_fork = _.cloneDeep(technical_forkBase)
  const stars = _.cloneDeep(starsBase)
  const activity = _.cloneDeep(activityBase)
  const attention = _.cloneDeep(attentionBase)
  const res = await chartData({u_id: route.query.pk})
  activity.series[0].data = res.data.activity.data
  activity.xAxis[0].data = res.data.activity.xAxis

  openRank.series[0].data = res.data.openRank.data
  openRank.xAxis[0].data = res.data.openRank.xAxis

  stars.series[0].data = res.data.stars.data
  stars.xAxis[0].data = res.data.stars.xAxis

  technical_fork.series[0].data = res.data.technical_fork.data
  technical_fork.yAxis[0].data = res.data.technical_fork.xAxis

  console.log(res.data.attention);
  attention.series = res.data.attention.series
  attention.legend.data = res.data.attention.legend
  attention.xAxis.data = res.data.attention.xAxis


  state.indicator = res.data.indicator
  state.title = res.data.title
  state.openRank = openRank
  state.technical_fork = technical_fork
  state.stars = stars
  state.activity = activity
  state.attention = attention
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
})
</script>

<template>
  <div class="aa" style="">
    <div style="padding: 20px 0;display: flex; justify-content: center;
    align-items: center;color: #ffffff; font-size: 2rem;font-weight: bold">
      {{state.title}}
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
      <div style="flex: 2;margin: 20px;display: flex;">
        <div class="chart-item" style="flex: 1;">
          <Echarts style="flex: 1" width="100%" :options="state.openRank"></Echarts>
        </div>
        <div class="chart-item" style="flex: 1;margin: 0 20px">
          <Echarts style="flex: 1" width="100%" :options="state.activity"></Echarts>
        </div>
        <div class="chart-item" style="flex: 1;">
          <Echarts style="flex: 1" width="100%" :options="state.stars"></Echarts>
        </div>
      </div>
      <div style="flex: 2;display: flex;margin: 0 20px;">
        <div class="chart-item" style="flex: 1;margin-right: 10px">
          <Echarts style="flex: 1" width="100%" :options="state.technical_fork"></Echarts>
        </div>
        <div class="chart-item" style="flex: 1;margin-left: 10px">
          <Echarts style="flex: 1" width="100%" :options="state.attention"></Echarts>
        </div>
      </div>
    </div>
    <img v-else src="@/assets/loading.svg" style="width: 100px;position: fixed;inset: 0;margin: auto" alt="">

    <!--        <Echarts style="flex: 1" width="100%" :options="state.options"></Echarts>-->
    <!--        <Echarts style="flex: 1" width="100%" :options="state.options"></Echarts>-->
    <!--        <Echarts style="flex: 1" width="100%" :options="state.options"></Echarts>-->
  </div>


</template>

<style scoped lang="less">
.indicator-item {
  padding: 10px;
  position: relative;
}

.chart-item {
  padding: 10px;

  background-color: rgba(0, 0, 0, .5);
}

.aa {
  position: fixed;
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
