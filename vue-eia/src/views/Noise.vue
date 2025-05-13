<template>
  <div class="container_zdy">
    <div id="mapDiv" style="position: absolute"></div>
    <div style="position: absolute; left: 100px; top: 20px; z-index: 1000">
      <el-button type="primary" plain @Click="openMarkerTool()">点源</el-button>
      <el-button type="primary" plain @Click="openRectangleTool()">矩形工具</el-button>
      <el-button type="primary" plain @Click="openPolygonTool()">多边形工具</el-button>
      <el-button type="primary" plain @Click="openPolylineTool()">线工具</el-button>
      <el-button type="primary" plain @Click="openRectangleTool()">矩形工具</el-button>
      <el-button type="primary" plain @Click="openCircleTool()">画圆工具</el-button>
      <el-button type="primary" plain @Click="map.clearOverLays()">清除所有</el-button>
      <el-button type="primary" plain @Click="getOverlays()">计算</el-button>
      <el-button plain @click="openMarkerZeroTool()"> 设置坐标原点 </el-button>
    </div>
    <el-dialog v-model="dialogFormVisible" title="坐标原点参数设置" width="400px">
      <el-form :model="zeroPoint">
        <el-form-item label="经度" :label-width="formLabelWidth">
          <el-input v-model="zeroPoint.x" autocomplete="off" />
        </el-form-item>
        <el-form-item label="纬度" :label-width="formLabelWidth">
          <el-input v-model="zeroPoint.y" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="dialogFormVisible = false"> Confirm </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { ZeroPoint, NoisePoint, NoisePointGroup } from '@/assets/noise.ts'
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const zeroPoint = reactive({
  x: '',
  y: '',
})

let ZeroPointObj = reactive(new T.Marker(new T.LngLat(0, 0)))
let map
const zoom = 12
let lay
let onlyMapLay
let handler
let infoWin

const markConfig = {
  showLabel: false,
  color: 'blue',
  weight: 3,
  opacity: 0.5,
  fillColor: '#FFFFFF',
  fillOpacity: 0.5,
}

onMounted(() => {
  // const imageURL =
  //   'http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles' +
  //   '&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=ca5674438dbf7215aceefabb2e5c3fd0'
  // const ciaURL =
  //   'http://t0.tianditu.gov.cn/cia_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles' +
  //   '&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=ca5674438dbf7215aceefabb2e5c3fd0'
  //创建自定义图层对象
  // const imageLay = new T.TileLayer(imageURL, { minZoom: 1, maxZoom: 18 })
  // const ciaLay = new T.TileLayer(ciaURL, { minZoom: 1, maxZoom: 18 })
  const mapConfig = { datasourcesControl: true }
  //初始化地图对象
  map = new T.Map('mapDiv', mapConfig)
  //设置显示地图的中心点和级别
  map.centerAndZoom(new T.LngLat(116.51138, 31.73518), zoom)
  //允许鼠标滚轮缩放地图
  map.enableScrollWheelZoom()

  //创建对象
  const ctrl = new T.Control.MapType()
  //添加控件
  map.addControl(ctrl)
})

function openPolygonTool() {
  if (handler) handler.close()
  handler = new T.PolygonTool(map, markConfig)

  handler.open()
}

function openPolylineTool() {
  if (handler) handler.close()
  handler = new T.PolylineTool(map, markConfig)
  handler.addEventListener('draw', function (e) {
    const polyline = e.allPolylines

    console.log(polyline[0].getLngLats())
  })
  handler.open()
}

function openMarkerTool() {
  if (handler) handler.close()
  handler = new T.MarkTool(map, { follow: false })
  handler.addEventListener('mouseup', function (e) {
    const point = e.currentLnglat
    console.log(point)
    // console.log(handler.getMarkers())
  })

  handler.open()
}
function openMarkerZeroTool() {
  if (handler) handler.close()
  map.removeOverLay(ZeroPointObj)
  handler = new T.MarkTool(map, { follow: false })
  handler.addEventListener('mouseup', function (e) {
    const point = e.currentLnglat
    ZeroPointObj = e.currentMarker
    zeroPoint.x = point.lng
    zeroPoint.y = point.lat
    dialogFormVisible.value = true
    // console.log(handler.getMarkers())
  })

  handler.open()
}

function openRectangleTool() {
  if (handler) handler.close()
  handler = new T.RectangleTool(map, { follow: true })
  handler.addEventListener('draw', function (e) {
    const rect = e.currentBounds
    console.log(rect.Lq)
    console.log(rect.kq)
  })
  handler.open()
}
function openCircleTool() {
  if (handler) handler.close()
  handler = new T.CircleTool(map, { follow: true })
  handler.open()
}

function setZeroPoint() {
  if (handler) handler.close()
  handler = new T.MarkTool(map, { follow: true })
  handler.addEventListener('mouseup', function (e) {
    zeroPoint = e.currentLnglat
    console.log(zeroPoint)
  })
  handler.open()
}

function getOverlays() {
  const array = map.getOverlays()
  array.forEach((element) => {
    if (element instanceof T.Polygon) {
      console.log('多边形')
      console.log(element.getLngLats())
    } else if (element instanceof T.Polyline) {
      console.log('线')
      console.log(element.getLngLats())
    } else if (element instanceof T.Marker) {
      console.log('点')
      console.log(element.getLngLat())
    } else if (element instanceof T.Rectangle) {
      console.log('矩形')
      console.log(element.getBounds())
    } else if (element instanceof T.Circle) {
      console.log('圆')
      console.log(element.getCenter())
    }
  })
}
</script>

<style scoped>
#mapDiv {
  width: 100%;
  height: 100%;
}
.container_zdy {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
