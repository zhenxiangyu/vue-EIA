<script setup lang="ts">
import { RouterView } from 'vue-router'
// import { ref } from 'vue'
// import HomeView from './views/HomeView.vue'
import FootView from './components/FootView.vue'
import HeaderView from './components/HeaderView.vue'
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <HeaderView />
      </el-header>
      <el-main style="height: 800px">
        <RouterView />
      </el-main>
      <el-footer>
        <FootView />
      </el-footer>
    </el-container>
  </div>
</template>

<style scoped></style>
