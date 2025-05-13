<template>
  <el-row class="tac">
    <el-col :span="3">
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item index="1">
          <template #title>
            <el-icon><icon-menu /></el-icon>
            <span>空气质量数据</span>
          </template>
        </el-menu-item>
        <el-menu-item index="2">
          <template #title>
            <el-icon><icon-menu /></el-icon>
            <span>空气质量数据校验</span>
          </template>
        </el-menu-item>
        <el-menu-item index="3">
          <template #title>
            <el-icon><icon-menu /></el-icon>
            <span>地理数据网站</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="20">
      <el-form :inline="true" :model="form" class="demo-form-inline">
        <el-form-item label="数据类型">
          <el-select v-model="dataTypeOptions" placeholder="请选择数据类型">
            <el-option
              v-for="item in form.dataTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              :disabled="item.disabled"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="城市及站点">
          <el-cascader
            v-model="cityAndStationOptions"
            :options="form.cityAndStationOptions"
            :props="props"
            @change="handleChange"
            placeholder="请选择城市及站点"
          />
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="selectedDate"
            type="datetimerange"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD HH"
            date-format="YYYY/MM/DD"
            time-format="A hh:mm:ss"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
      <!-- <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="positionName" label="站点" width="180" />
        <el-table-column prop="pm10" label="PM10" width="180" />
        <el-table-column prop="pm25" label="PM2.5" />
      </el-table> -->
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { Menu as IconMenu, Location } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
import { utils, writeFile } from 'xlsx'

const dataTypeOptions = ref()
const cityAndStationOptions = ref([])
const selectedDate = ref()
const tableData = ref([])

const form = reactive({
  dataTypeOptions: [
    {
      value: 'airQuality',
      label: '城市空气质量实时数据',
    },
    {
      value: 'airQualityDailyNum',
      label: '城市空气质量日数据',
    },
    {
      value: 'nationMonitorDailyData',
      label: '国控站点空气质量日数据',
    },
    {
      value: 'nationMonitorLiveData',
      label: '国控站点空气质量实时数据',
    },
    {
      value: 'provinceMonitorDailyData',
      label: '省控站点空气质量日数据',
      disabled: true,
    },
    {
      value: 'provinceMonitorLiveData',
      label: '省控站点空气质量实时数据',
    },
  ],
  cityAndStationOptions: [
    {
      value: '341500',
      label: '六安',
      children: [
        {
          value: '',
          label: '六安站',
        },
        {
          value: '1057A',
          label: '监测大楼',
        },
        {
          value: '1058A',
          label: '皖西学院',
        },
        {
          value: '1059A',
          label: '朝阳厂',
        },
        {
          value: '1060A',
          label: '开发区',
        },
        {
          value: '813',
          label: '叶集区环保局',
        },
        {
          value: '610',
          label: '霍邱县环保局大楼',
        },
        {
          value: '604',
          label: '霍山县环保局',
        },
        {
          value: '601',
          label: '金寨县老干部活动中心',
        },
        {
          value: '607',
          label: '舒城县政府',
        },
      ],
    },
  ],
})

const onSubmit = () => {
  const params = {
    dataType: dataTypeOptions.value,
    cityAndStation: cityAndStationOptions.value,
    dateRange: selectedDate.value,
  }

  fetch(`http://127.0.0.1:5000/prepareData`, {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  }).then((response) => {
    console.log('Response:', response)
    if (response.ok) {
      response.json().then((data) => {
        tableData.value = data.data
        const wooksheet = utils.json_to_sheet(data.data)
        const book = utils.book_new()
        utils.book_append_sheet(book, wooksheet, 'Sheet1')
        writeFile(book, '数据.xlsx')
      })
    } else {
      console.error('Error fetching data:', response.statusText)
    }
  })
}
const props = {
  expandTrigger: 'hover' as const,
}

const handleChange = () => {
  console.log()
}

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}

.demo-form-inline {
  text-align: center; /* 让内容居中 */
}
</style>
