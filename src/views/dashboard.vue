<script setup>
import {onMounted, reactive, ref} from "vue";
import {useRoute} from "vue-router";
import {useStore} from "@/stores/app";
import {Search} from "@element-plus/icons-vue"
import {overview, toFocusDevUser, toFocusProj} from "@/api/dash";
import router from "@/router";
import {formatterDate} from "@/libs/utils";

const route = useRoute()
const store = useStore()

const state = reactive({
  data: [],
  columns: [],
  total: 0,
  loading: false,
})

const to_focus = async (row, operate) => {
  let res
  if (payload.value.item === 1) {
    res = await toFocusProj({
      u_id: row.pk,
      operate: operate,
    })
  } else {
    res = await toFocusDevUser({
      u_id: row.pk,
      operate: operate,
    })

  }

  if (res.data.code === 0) {
    await get_data()
  }
}
const to_chart = (row) => {
  if (row.item === 1) {
    router.push({name: "dashchart", query: {pk: row.pk}})
  } else {
    router.push({name: "dashchart2", query: {pk: row.pk}})
  }

}

const payload = ref({
  search: '',
  item: 1,
  tt: undefined,
  ttType: 'y',
  order_by: 'openRank',
  page: 1,
  limit: 15,
})
const value1 = ref(new Date(2024, 0, 1))
const get_data = async () => {
  if (['attention', 'stars', 'technical_fork'].includes(payload.value.order_by) && payload.value.item === 2) {
    payload.value.order_by = 'openRank'
  }

  payload.value.tt = formatterDate(value1.value, payload.value.ttType)

  state.loading = true
  const res = await overview(payload.value)
  state.data = res.data.data
  state.columns = res.data.columns
  state.total = res.data.total
  state.loading = false
}
import {useDark, useToggle} from "@vueuse/core";

const isDark = useDark()
const toggleDark = useToggle(isDark)
onMounted(() => {
  get_data()
  if (isDark.value) {
    toggleDark()
  }


})
</script>

<template>
  <div style="margin-bottom: 20px">
    <el-space>
      <div style="width: 60px">Item</div>
      <el-radio-group v-model="payload.item" @change="get_data">
        <el-radio :value="1">项目</el-radio>
        <el-radio :value="2">开发者</el-radio>
      </el-radio-group>
    </el-space>
  </div>
  <div style="margin-bottom: 20px">
    <el-space>
      <div style="width: 60px">排序</div>
      <el-radio-group v-model="payload.order_by" @change="get_data">
        <el-radio value="openRank">排名</el-radio>
        <el-radio value="activity">活跃度</el-radio>
        <div v-show="payload.item===1">
          <el-radio value="attention">关注度</el-radio>
          <el-radio value="stars">Stars</el-radio>
          <el-radio value="technical_fork">Fork</el-radio>
        </div>

      </el-radio-group>
    </el-space>
  </div>
  <div style="margin-bottom: 20px;">
    <el-row justify="space-between">
      <el-space>
        <div style="width: 60px">时间</div>
        <el-select v-model="payload.ttType" style="width: 100px" @change="get_data">
          <el-option value="y" label="年度"></el-option>
          <el-option value="m" label="月度"></el-option>
        </el-select>
        <el-date-picker
          v-if="payload.ttType==='y'"
          v-model="value1"
          type="year"
          @change="get_data"
        />
        <el-date-picker
          v-else
          v-model="value1"
          type="month"
          @change="get_data"
        />


      </el-space>
      <el-input placeholder="搜索" v-model="payload.search" clearable @clear="get_data" style="width: 240px;">
        <template #append>
          <el-button :icon="Search" @click="get_data"/>

        </template>
      </el-input>
    </el-row>
  </div>

  <el-table :data="state.data" v-loading="state.loading">
    <el-table-column v-for="cc in state.columns" :prop="cc.key" :label="cc.label" align="center">
      <template #default="scope">
        <div v-if="cc.key==='operate'">
          <el-button v-if="!scope.row.focus" type="text" size="small"
                     @click="to_focus(scope.row, 'add')">+关注
          </el-button>
          <el-button v-else type="info" text size="small"
                     @click="to_focus(scope.row, 'delete')">-取消关注
          </el-button>
        </div>
        <a :href="scope.row.home" v-else-if="cc.key==='avatar_url'" target="_blank">
        <el-avatar :src="scope.row[cc.key]"></el-avatar>
          </a>
        <div v-else-if="cc.key==='dash'" style="display: flex; justify-content: center;">
          <img style="cursor: pointer"
               @click="to_chart(scope.row)"
               src="https://open-leaderboard.x-lab.info/pics/dashboard.png" alt="" width="24">
        </div>

      </template>
    </el-table-column>
  </el-table>

  <el-pagination v-model:current-page="payload.page"
                 v-model:page-size="payload.limit"
                 background
                 :total="state.total"
                 @current-change="get_data"
                 style="margin-top: 10px"
  >

  </el-pagination>
</template>

<style scoped lang="less">

</style>
