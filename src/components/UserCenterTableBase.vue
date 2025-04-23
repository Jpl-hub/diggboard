<script setup>
import {computed, onMounted, reactive, ref} from "vue"
import router from "@/router";
import {useRoute} from "vue-router"
import {getFocusArr, toFocusDevUser, toFocusProj} from "@/api/dash";

const route = useRoute()
const state = reactive({})
const props = defineProps([
  'item'
])
const payload = ref({
  search: '',
  item: props.item,
  tt: undefined,
  ttType: 'y',
  order_by: 'openRank',
  page: 1,
  limit: 20,
})
const get_data = async () => {
  state.loading = true
  const res = await getFocusArr(payload.value)
  state.data = res.data.data
  state.columns = res.data.columns
  state.total = res.data.total
  state.loading = false
}
const to_chart = (row) => {
  if (row.item === 1) {
    router.push({name: "dashchart", query: {pk: row.pk}})
  } else {
    router.push({name: "dashchart2", query: {pk: row.pk}})
  }

}

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
onMounted(() => {
  get_data()
})
</script>

<template>
  <el-table :data="state.data" v-loading="state.loading">
    <el-table-column v-for="cc in state.columns" :prop="cc.key" :label="cc.label" align="center">
      <template #default="scope">
        <div v-if="cc.key==='operate'">
          <el-button v-if="!scope.row.focus" type="text" size="small"
                     @click="to_focus(scope.row, 'add')">+关注
          </el-button>
          <el-button v-else type="info" text size="small"
                     @click="to_focus(scope.row, 'delete')">取消关注
          </el-button>
        </div>
        <el-avatar v-else-if="cc.key==='avatar_url'" :src="scope.row[cc.key]"></el-avatar>
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