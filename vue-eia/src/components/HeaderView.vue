<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false" @select="handleSelect">
    <el-menu-item index="0">
      <img style="width: 180px; height: 60px" src="@/components/icons/logo.jpg" alt="logo" />
    </el-menu-item>
    <el-menu-item index="1">登录</el-menu-item>
    <el-menu-item index="2">注册</el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style>
