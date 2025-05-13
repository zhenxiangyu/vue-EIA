<template>
  <div class="dashboard">
    <div class="hero">
      <h1>环境预测智能分析系统</h1>
      <p>集成多维度环境预测模型，支持噪声、地下水、风险评估等专业分析</p>
    </div>

    <div class="grid">
      <a href="/groundWater" class="card">
        <i class="fas fa-water card-icon"></i>
        <h3 class="card-title">地下水污染预测</h3>
        <p class="card-desc">一维水动力弥散模型分析，支持多参数输入和可视化结果输出</p>
      </a>

      <a href="/noise" class="card">
        <i class="fas fa-volume-up card-icon"></i>
        <h3 class="card-title">噪声扩散预测</h3>
        <p class="card-desc">工业噪声传播模型，支持三维空间分析和等值线可视化</p>
      </a>

      <a href="/risk" class="card">
        <i class="fas fa-exclamation-triangle card-icon"></i>
        <h3 class="card-title">环境风险评估</h3>
        <p class="card-desc">多因子风险评估模型，支持概率分析和风险等级划分</p>
      </a>
      <a href="/getdata" class="card">
        <i class="fas fa-exclamation-triangle card-icon"></i>
        <h3 class="card-title">环境质量数据</h3>
        <p class="card-desc">通过爬虫技术从网上获取相关环境数据</p>
      </a>
    </div>
  </div>
</template>
<style scoped>
/* body {
  font-family: 'Segoe UI', system-ui;
  background: var(--background-color);
  margin: 0;
  min-height: 100vh;
} */

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.nav {
  background: var(--card-background);
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.card {
  background: var(--card-background);
  border-radius: 12px;
  padding: 2rem;
  transition: transform 0.3s ease;
  cursor: pointer;
  text-align: center;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.card-icon {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}
a {
  text-decoration: none;
}
.card-title {
  color: #000000;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.card-desc {
  color: #000000;
  line-height: 1.6;
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: var(--gradient);
  color: rgb(0, 0, 0);
  border-radius: 12px;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
</style>

<script setup lang="ts">
// const predict = (type: string) => console.log(`Predicting for ${type}`)

// const getData = (type: string) => {
//   console.log(`Getting data for ${type}`)
//   window.open('https://www.aqistudy.cn/historydata/', '_blank')
// }
</script>
