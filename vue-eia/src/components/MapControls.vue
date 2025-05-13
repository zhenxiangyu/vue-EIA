<template>
  <div class="map-controls">
    <button @click="startDrawing('Point')">点</button>
    <button @click="startDrawing('LineString')">线</button>
    <button @click="startDrawing('Polygon')">面</button>
    <button @click="clearAll">清除</button>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue'
import { Draw } from 'ol/interaction'
import type { Map } from 'ol'

const props = defineProps({
  vectorLayer: {
    type: Object,
    required: true
  }
})

const map = inject<Map>('map')
let drawInteraction: Draw | null = null

const startDrawing = (type: 'Point' | 'LineString' | 'Polygon') => {
  if (drawInteraction) {
    map?.removeInteraction(drawInteraction)
  }

  drawInteraction = new Draw({
    source: props.vectorLayer.getSource(),
    type: type
  })

  drawInteraction.on('drawend', () => {
    map?.removeInteraction(drawInteraction!)
    drawInteraction = null
  })

  map?.addInteraction(drawInteraction)
}

const clearAll = () => {
  props.vectorLayer.getSource().clear()
}
</script>

<style scoped>
.map-controls {
  position: absolute;
  top: 1em;
  right: 1em;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 4px;
}

button {
  margin: 0 5px;
  padding: 5px 10px;
}
</style>