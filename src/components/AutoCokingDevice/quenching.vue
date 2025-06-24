<template>
  <div class="main-container">
    <!-- Three.js 场景 -->
    <div class="scene-container" ref="container"></div>

    <!-- 左侧容器：显示加载中的提示 -->
    <div class="charts-wrapper-left">
      <div class="loading-message">
        <p>网络相机画面正在加载中，请等待</p>
      </div>
    </div>

    <!-- 右侧的三个板块（从上到下） -->
    <div class="charts-wrapper">
      <!-- 板块1：胶质层取样器状态 -->
      <div class="chart-container">
        <div class="info-block">
          <p class="section-title">胶质层取样器状态</p>
          <div class="text-content">
            <p>状态：<span class="value-glow">{{ glycerinStatus.status }}</span></p>
            <p>
              胶质层取样器样品管温度：
              <span class="value-glow">{{ glycerinStatus.temp }}</span>
            </p>
          </div>
        </div>
      </div>

      <!-- 板块2：焦炉状态 -->
      <div class="chart-container">
        <div class="info-block">
          <p class="section-title">焦炉状态</p>
          <div class="text-content">
            <!-- 通过 v-for 循环渲染不同位置的温度 -->
            <p v-for="(temp, depth) in furnaceStatus" :key="depth">
              {{ depth }}：
              <span class="value-glow">{{ temp }}</span>
            </p>
          </div>
        </div>
      </div>

      <!-- 板块3：氮气冷却系统状态 -->
      <div class="chart-container">
        <div class="info-block">
          <p class="section-title">氮气冷却系统状态</p>
          <div class="text-content">
            <p>
              氮气压力：
              <span class="value-glow">{{ nitrogenStatus.pressure }}</span>
            </p>
            <p>
              氮气流量：
              <span class="value-glow">{{ nitrogenStatus.flow }}</span>
            </p>
            <p>
              冷却室温度：
              <span class="value-glow">{{ nitrogenStatus.temp }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Quenching',
  data() {
    return {
      // 只是示例，可根据业务需求自行修改或加载接口数据
      modifyParametersForm: { params: [] },
      modifyParametersForm_2: { params: [] },

      // 每个状态通过响应式数据进行管理
      glycerinStatus: {
        status: '冷却',
        temp: '550 ℃'
      },
      furnaceStatus: {
        '50mm': '980 ℃',
        '100mm': '960 ℃',
        '150mm': '940 ℃',
        '200mm': '920 ℃',
        '250mm': '900 ℃'
      },
      nitrogenStatus: {
        pressure: '0.1 Mpa',
        flow: '20 L/min',
        temp: '60 ℃'
      }
    }
  },
  mounted() {
    // 如果需要在加载后动态更新，可在这里执行
    this.updateStatus()
  },
  methods: {
    updateStatus() {
      // 这里只是演示。比如可以根据接口返回数据来更新：
      // this.glycerinStatus.status = '加热中'
      // this.furnaceStatus['50mm'] = '985 ℃'
      // this.nitrogenStatus.temp = '70 ℃'
    }
  }
}
</script>

<style scoped>
.main-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.scene-container {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}

.charts-wrapper-left {
  position: absolute;
  top: 2%;
  left: 20px;
  width: 45%;
  height: 95%;
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent !important;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5),
    0 0 30px rgba(0, 255, 255, 0.3);
  overflow: hidden;
}

.loading-message p {
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  font-family: 'Arial', sans-serif;
}

.charts-wrapper {
  position: absolute;
  top: 2%;
  right: 20px;
  width: 50%;
  height: 95%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 10;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5),
    0 0 30px rgba(0, 255, 255, 0.3);
}

.chart-container {
  background-color: transparent;
  border-radius: 8px;
  box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2),
    0 0 10px rgba(0, 255, 255, 0.2);
  box-sizing: border-box;
}

.info-block {
  height: 90%;
  padding: 20px;
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(0, 204, 255, 0.3));
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.2);
}

/* 这里标题仅有轻微发光或保持原状 */
.section-title {
  color: #00f7ff;
  font-family: 'Arial', sans-serif;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin: 15px 0;
}

/* 普通文字不发光，仅保持基础样式 */
.text-content {
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  text-align: center;
  font-family: 'Arial', sans-serif;
}

/* 冒号后面的值文字，带发光效果 */
.value-glow {
  text-shadow:
    0 0 3px #fff,
    0 0 6px #0ff,
    0 0 9px #0ff,
    0 0 12px #0ff;
  color: #fff;
}
</style>
