<template>
  <div class="main-container">
    <!-- Three.js Scene Container -->
    <div class="scene-container" ref="container"></div>

    <!-- 纯 CSS colorbar 容器 -->
    <div class="colorbar-container">
      <div class="cb-label min-label">0℃</div>
      <div class="cb-label max-label">1200℃</div>
    </div>

    <!-- 单独的 ECharts 图表容器 -->
    <div class="left-charts-wrapper">
      <div class="chart-container" ref="chart1"></div>
      <div class="chart-container" ref="chart2"></div>
    </div>
    <div class="right-charts-wrapper">
      <div class="chart-container" ref="chart3"></div>
      <div class="chart-container" ref="chart4"></div>
    </div>
    <!-- 开关按钮容器 -->
    <!--
    <div class="toggle-container">
      <label class="switch">
        <input type="checkbox" v-model="leftOvenChecked" @change="onLeftOvenChange" />
        <span class="slider"></span>
      </label>
      <span class="label-text">
        碳化室孪生体：{{ leftOvenChecked ? 'ON' : 'OFF' }}
      </span>
    </div>
    -->
  </div>
</template>

<script>
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import industryUrl from '../../assets/models/实验焦炉.glb' // 确保路径正确
import gridTextureUrl from '../../assets/textures/grid4.jpg' // 导入网格纹理
import * as echarts from 'echarts'

export default {
  name: 'CokeDigitalTwin',
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      clock: null,
      animationFrameId: null,

      ovenShaderMat: null,
      leftOvenGroup: null,
      rightOvenGroup: null,

      // ECharts 实例
      chart1: null,
      chart2: null,
      chart3: null,
      chart4: null,

      // 用于控制图表更新的时间间隔
      lastUpdateTime: 0, // 上一次更新的时间
      updateInterval: 5000, // 更新间隔，单位毫秒（例如：5000ms = 5秒）

      // 左炉是否透明，false=不透明(OFF)，true=透明(ON)
      leftOvenChecked: false,
      myTempData: [], // 温度曲线的数据
      myPressData50: [],
      myPressData100: [],
      myPressData150: [],
      myPressData200: [],
      myPressData250: [],
      myTimeData: [], // 时间曲线的数据
      myPlasticData: []
    }
  },
  mounted() {
    this.initScene()
    this.loadAndCloneModel()
    this.initCharts()
    this.animate()
    this.startSyncAnimation()
    window.addEventListener('resize', this.onWindowResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.onWindowResize)
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId)
    }
    if (this.renderer) {
      this.renderer.dispose()
    }

    // 销毁 ECharts 实例
    if (this.chart1) {
      this.chart1.dispose()
    }
    if (this.chart2) {
      this.chart2.dispose()
    }
    if (this.chart3) { // 新增
      this.chart3.dispose()
    }
  },
  methods: {
    /**
   * 生成带“延时上升”的数组
   * @param {number} totalPoints     - 总采样点数（与X轴刻度数量一致，比如 21 个点 0~20h）
   * @param {number} offsetHour      - 延迟上升的“开始小时”，如 3 表示从 3h 开始升
   * @param {number} startValue      - 升温的初始温度(如 30℃)
   * @param {number} endValue        - 升温的终点温度(如 1600℃)
   * @returns {Array<number>}        - 长度为 totalPoints 的数据数组
   */
    generateOffsetCurve(totalPoints, offsetHour, startValue, endValue) {
      const data = []
      // 这里假设 X 轴与“小时”一一对应：索引=0 => 0h, 索引=1 => 1h, … 索引=20 => 20h
      // 那么 offsetHour=3 就对应索引=3。
      const offsetIndex = offsetHour

      // （1）如果 offsetHour 已经大于等于 totalPoints，那就全程都是 0
      if (offsetIndex >= totalPoints) {
        for (let i = 0; i < totalPoints; i++) {
          data.push(0)
        }
        return data
      }

      // （2）先确定缓动区间长度
      const transitionLength = totalPoints - offsetIndex

      for (let i = 0; i < totalPoints; i++) {
        if (i < offsetIndex) {
          // offsetIndex 之前保持 0
          data.push(0)
        } else {
          // 从 offsetIndex ~ (totalPoints-1) 做缓动上升
          const r = (i - offsetIndex) / (transitionLength - 1) // 0~1
          // 这里用三次缓动（easeOutCubic）
          const eased = 1 - Math.pow(1 - r, 3)
          const val = startValue + (endValue - startValue) * eased
          data.push(val)
        }
      }
      return data
    },
    /**
     * 生成一组正态分布数据
     * @param {number} numPoints - 需要生成的点数
     * @param {number} mean - 正态分布的均值
     * @param {number} stdDev - 正态分布的标准差
     * @returns {Array<number>}
     */
    generateNormalDistData(numPoints, mean, stdDev) {
      const data = []
      // 这里将 x 取为 0,1,2,... numPoints-1
      // 如果你想让曲线在更大或更小范围上，可以自行调整
      for (let x = 0; x < numPoints; x++) {
        // 经典正态分布 PDF = 1/(σ·sqrt(2π)) * e^(-(x - μ)² / (2σ²))
        const exponent = -Math.pow(x - mean, 2) / (2 * stdDev * stdDev)
        const base = 1 / (stdDev * Math.sqrt(2 * Math.PI))
        const y = base * Math.exp(exponent)
        data.push(y)
      }
      return data
    },
    generateCustomCurve(totalPoints, startValue, endValue, speedFactor) {
      const data = []
      for (let i = 0; i < totalPoints; i++) {
        const t = i / (totalPoints - 1)
        const p = 1.0 - Math.pow(1 - t, speedFactor)
        const val = startValue + (endValue - startValue) * p
        data.push(val)
      }
      return data
    },
    /**
     * 生成一个在 [20, 25] 之间波动的折线数据
     * 这里示例采用正弦波，你也可改为随机数或随机游走
     * @param {number} numPoints - 数据点数
     * @returns {Array<number>}
     */
    generateTimeFluctuationData(numPoints = 21) {
      const data = []
      // 波动幅度：2.5 => 让它以 22.5 为中心，向上/下各浮动 2.5 => [20, 25]
      const amplitude = 2.5
      const center = 22.5

      // 这里设置一个频率或周期，你可以自定义
      // 让 x 从 0~(numPoints-1)，完成半个正弦周期(0~π)
      const freq = Math.PI / (numPoints - 1)

      for (let i = 0; i < numPoints; i++) {
        const val = center + amplitude * Math.sin(freq * i)
        data.push(Number(val.toFixed(2))) // 保留2位小数
      }
      return data
    },
    generateIncreasingStableData() {
      const data = []
      const totalPoints = 20
      const transitionPoint = 10 // 前 transitionPoint 个点做缓动上升
      const startValue = 30
      const endValue = 1600

      for (let i = 0; i < totalPoints; i++) {
        if (i < transitionPoint) {
          // r 在 0 ~ 1 之间
          const r = i / (transitionPoint - 1)

          // （1）如果想用二次缓动（easeOutQuad），可写：
          // const eased = 1 - (1 - r) * (1 - r)

          // （2）如果想用三次缓动（easeOutCubic），可写：
          const eased = 1 - Math.pow((1 - r), 3)

          // 将 eased 映射到 [startValue, endValue]
          const value = startValue + (endValue - startValue) * eased
          data.push(value)
        } else {
          // 超过 transitionPoint 的部分，直接保持在 endValue
          data.push(endValue)
        }
      }

      return data
    },
    onLeftOvenChange() {
      // 当开关状态变化时 (true/false), 我们执行逻辑
      if (this.leftOvenChecked) {
        // 左炉变透明
        this.makeLeftTransparent()
      } else {
        // 左炉恢复不透明
        this.makeLeftOpaque()
      }
    },
    makeLeftTransparent() {
      // 这里就是你之前的遍历、设置材质透明的逻辑
      // 比如：
      if (this.leftOvenGroup) {
        this.leftOvenGroup.traverse(child => {
          if (child.isMesh) {
            child.material.transparent = true
            child.material.opacity = 0.2
          }
        })
      }
    },
    makeLeftOpaque() {
      // 同理，恢复不透明
      if (this.leftOvenGroup) {
        this.leftOvenGroup.traverse(child => {
          if (child.isMesh) {
            child.material.transparent = false
            child.material.opacity = 1.0
          }
        })
      }
    },
    startSyncAnimation() {
      // 1) 先用你已有的函数生成四组带缓动的“目标数据”。
      //    这里举例都用 generateIncreasingStableData()，你也可以改成不同的函数/区间。
      const timeFluctArr = this.generateTimeFluctuationData(21)
      this.myTimeData = []
      const plasticCurve = this.generateIncreasingStableData() // 用于塑性

      // === 新增 chart1 的 5条线目标数据 ===
      const curve50 = this.generateOffsetCurve(21, 0, 30, 1600)
      const curve100 = this.generateOffsetCurve(21, 3, 30, 1600)
      const curve150 = this.generateOffsetCurve(21, 6, 30, 1600)
      const curve200 = this.generateOffsetCurve(21, 9, 30, 1600)
      const curve250 = this.generateOffsetCurve(21, 6, 30, 1600) // 与 150mm 相同

      // 先生成 5 条目标数据 (每条都有 21 个点, 仅示例)
      const normal50 = this.generateNormalDistData(21, 1, 5)
      const normal100 = this.generateNormalDistData(21, 3, 10)
      const normal150 = this.generateNormalDistData(21, 5, 15)
      const normal200 = this.generateNormalDistData(21, 7, 20)
      const normal250 = this.generateNormalDistData(21, 5, 15) // 与 150mm 相同

      // 先清空存放温度、压力数据的数组
      this.myData50 = []
      this.myData100 = []
      this.myData150 = []
      this.myData200 = []
      this.myData250 = []

      this.myPressData50 = []
      this.myPressData100 = []
      this.myPressData150 = []
      this.myPressData200 = []
      this.myPressData250 = []

      // 也清空时间、塑性曲线
      this.myTimeData = []
      this.myPlasticData = []

      // 2) 定义索引，分“温度索引”+“压力索引”
      let idxT50 = 0
      let idxT100 = 0
      let idxT150 = 0
      let idxT200 = 0
      let idxT250 = 0

      let idxP50 = 0
      let idxP100 = 0
      let idxP150 = 0
      let idxP200 = 0
      let idxP250 = 0

      let idxTime = 0
      let idxPlastic = 0

      // 4) 用 setInterval 每隔 500ms 推送一个点
      this.intervalId = setInterval(() => {
        // ---- 温度曲线: 5 条 ----
        if (idxT50 < curve50.length) {
          this.myData50.push(curve50[idxT50])
          idxT50++
        }
        if (idxT100 < curve100.length) {
          this.myData100.push(curve100[idxT100])
          idxT100++
        }
        if (idxT150 < curve150.length) {
          this.myData150.push(curve150[idxT150])
          idxT150++
        }
        if (idxT200 < curve200.length) {
          this.myData200.push(curve200[idxT200])
          idxT200++
        }
        if (idxT250 < curve250.length) {
          this.myData250.push(curve250[idxT250])
          idxT250++
        }

        // ---- 压力曲线: 5 条 ----
        if (idxP50 < normal50.length) {
          this.myPressData50.push(normal50[idxP50])
          idxP50++
        }
        if (idxP100 < normal100.length) {
          this.myPressData100.push(normal100[idxP100])
          idxP100++
        }
        if (idxP150 < normal150.length) {
          this.myPressData150.push(normal150[idxP150])
          idxP150++
        }
        if (idxP200 < normal200.length) {
          this.myPressData200.push(normal200[idxP200])
          idxP200++
        }
        if (idxP250 < normal250.length) {
          this.myPressData250.push(normal250[idxP250])
          idxP250++
        }

        // --- 时间曲线 ---
        if (idxTime < timeFluctArr.length) {
          this.myTimeData.push(timeFluctArr[idxTime])
          idxTime++
          this.chart3.setOption({
            series: [{ data: [...this.myTimeData] }]
          })
        }

        // --- 塑性曲线 ---
        if (idxPlastic < plasticCurve.length) {
          this.myPlasticData.push(plasticCurve[idxPlastic])
          idxPlastic++
          this.chart4.setOption({
            series: [{ data: [...this.myPlasticData] }]
          })
        }

        // 更新 chart1 (温度线)
        this.chart1.setOption({
          series: [
            { name: '50mm', data: [...this.myData50] },
            { name: '100mm', data: [...this.myData100] },
            { name: '150mm', data: [...this.myData150] },
            { name: '200mm', data: [...this.myData200] },
            { name: '250mm', data: [...this.myData250] }
          ]
        })

        // 更新 chart2 (压力线)
        this.chart2.setOption({
          series: [
            { name: '50mm', data: [...this.myPressData50] },
            { name: '100mm', data: [...this.myPressData100] },
            { name: '150mm', data: [...this.myPressData150] },
            { name: '200mm', data: [...this.myPressData200] },
            { name: '250mm', data: [...this.myPressData250] }
          ]
        })

        // 4) 如果都推送完，就停止定时器
        if (
          idxT50 >= curve50.length && idxT100 >= curve100.length &&
          idxT150 >= curve150.length && idxT200 >= curve200.length &&
          idxT250 >= curve250.length &&

          idxP50 >= normal50.length && idxP100 >= normal100.length &&
          idxP150 >= normal150.length && idxP200 >= normal200.length &&
          idxP250 >= normal250.length &&

          idxPlastic >= plasticCurve.length
        ) {
          clearInterval(this.intervalId)
        }
      }, 500)
    },
    initScene() {
      const container = this.$refs.container

      this.scene = new THREE.Scene()

      // 加载网格纹理作为背景
      const loader = new THREE.TextureLoader()
      loader.load(
        gridTextureUrl,
        (texture) => {
          texture.wrapS = THREE.RepeatWrapping
          texture.wrapT = THREE.RepeatWrapping
          texture.repeat.set(1, 1) // 根据需要调整重复次数
          this.scene.background = texture
        },
        undefined,
        (err) => {
          console.error('加载网格纹理时出错:', err)
          this.scene.background = new THREE.Color(0x888888) // 出错时设置一个默认背景色
        }
      )

      // 相机设置
      this.camera = new THREE.PerspectiveCamera(
        60,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
      )
      this.camera.position.set(-10, 8, 12)

      // 渲染器设置
      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }) // 启用 alpha 以支持透明
      this.renderer.setSize(container.clientWidth, container.clientHeight)
      container.appendChild(this.renderer.domElement)

      this.renderer.outputEncoding = THREE.sRGBEncoding
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping
      this.renderer.toneMappingExposure = 1.0

      // 灯光设置
      const ambientLight = new THREE.AmbientLight(0xffffff, 1.0)
      this.scene.add(ambientLight)
      const dirLight = new THREE.DirectionalLight(0xffffff, 1.2)
      dirLight.position.set(50, 100, 70)
      this.scene.add(dirLight)

      // 控制器设置
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enableDamping = true
      this.controls.dampingFactor = 0.1

      this.clock = new THREE.Clock()

      // 添加增强的网格辅助线
      const gridHelper = new THREE.GridHelper(100, 100, 0x00ff00, 0x00ff00)
      gridHelper.position.y = -0.1 // 将网格下移 3 个单位
      gridHelper.material.opacity = 0
      gridHelper.material.transparent = true
      this.scene.add(gridHelper)

      // 添加坐标轴辅助线
      // const axesHelper = new THREE.AxesHelper(10)
      // this.scene.add(axesHelper)
    },
    loadAndCloneModel() {
      const loader = new GLTFLoader()
      loader.load(
        industryUrl,
        (gltf) => {
          const ovenModel = gltf.scene

          // 1) 模型初步定位、旋转等操作
          let box = new THREE.Box3().setFromObject(ovenModel)
          const min = box.min
          ovenModel.position.x += 0.298 // 平移
          ovenModel.position.y -= min.y // 贴地
          ovenModel.rotation.y = -Math.PI / 2 // 旋转

          // 2) 刷新矩阵，确保模型的变换应用到世界坐标
          ovenModel.updateMatrixWorld(true)

          // 3) 重新计算包围盒（此时 box 才能正确反映最新位置）
          box = new THREE.Box3().setFromObject(ovenModel)

          // 4) 根据包围盒，获取中心和最大半径
          const newCenterVec = new THREE.Vector3()
          box.getCenter(newCenterVec)

          const leftDist = Math.abs(box.min.x - newCenterVec.x)
          const rightDist = Math.abs(box.max.x - newCenterVec.x)
          const maxX = Math.max(leftDist, rightDist)

          // 5) 使用该中心和范围，构建或更新 ShaderMaterial uniforms
          this.ovenShaderMat = new THREE.ShaderMaterial({
            vertexShader,
            fragmentShader,
            uniforms: {
              uTime: { value: 0 },
              uMaxX: { value: maxX },
              uCenterX: { value: newCenterVec.x }
            },
            transparent: true
          })

          // 右炉子（克隆 + 自定义材质）
          this.rightOvenGroup = new THREE.Group()
          const rightOvenClone = ovenModel.clone(true)
          rightOvenClone.traverse(child => {
            if (child.isMesh) {
              child.material = this.ovenShaderMat
            }
          })
          this.rightOvenGroup.add(rightOvenClone)
          this.rightOvenGroup.position.set(2.5, 0, 0) // 调整位置
          this.scene.add(this.rightOvenGroup)

          // 移动完再更新:
          const finalCenterX = newCenterVec.x + this.rightOvenGroup.position.x
          this.ovenShaderMat.uniforms.uCenterX.value = finalCenterX

          // 使相机集中于右炉子并增加缩放
          this.camera.lookAt(0, 0, 0)
          this.camera.position.set(0, 8, 15) // 放大模型
        },
        (xhr) => {
          console.log(`${(xhr.loaded / xhr.total) * 100}% loaded`)
        },
        (err) => {
          console.error('加载模型时出错:', err)
        }
      )
    },
    animate() {
      this.animationFrameId = requestAnimationFrame(this.animate)
      this.controls.update()
      const elapsed = this.clock.getElapsedTime()
      if (this.ovenShaderMat) {
        this.ovenShaderMat.uniforms.uTime.value = elapsed
      }
      this.renderer.render(this.scene, this.camera)

      // 获取当前时间的毫秒数
      const currentTime = Date.now()
      if (currentTime - this.lastUpdateTime >= this.updateInterval) {
        // this.updateChartsData()
        this.lastUpdateTime = currentTime
      }
    },
    onWindowResize() {
      const container = this.$refs.container
      if (!container) return
      this.camera.aspect = container.clientWidth / container.clientHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(container.clientWidth, container.clientHeight)

      // 调整 ECharts 大小
      if (this.chart1) this.chart1.resize()
      if (this.chart2) this.chart2.resize()
      if (this.chart3) this.chart3.resize()
      if (this.chart4) this.chart4.resize()
    },
    initCharts() {
      // 公用的 grid 设置，增加右边距以防止标签被遮挡
      const commonGrid = {
        top: '30%',
        left: '10%',
        right: '15%', // 增加右边距
        bottom: '10%', // 增加底部间距
        containLabel: true
      }

      // 图表 1：煤床温度检测
      this.chart1 = echarts.init(this.$refs.chart1)
      const option1 = {
        backgroundColor: 'transparent',
        title: {
          text: '煤床温度检测',
          textStyle: { color: '#ffffff' },
          left: 'center',
          top: 30
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          // 因为有多条线，最好把 legend 打开
          show: true,
          textStyle: { color: '#ffffff' },
          top: 0 // 视需求调整位置
        },
        grid: commonGrid,
        xAxis: {
          type: 'category',
          // 把 X 轴名称改得更明确
          name: '时间',
          // 使用我们新写的生成函数
          data: this.generateHourCategories(),
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: {
            color: '#ffffff',
            rotate: 45,
            // 如果要截断超长文本
            formatter(value) {
              return value.length > 5 ? value.slice(0, 5) + '...' : value
            }
          },
          splitLine: { show: false },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        yAxis: {
          type: 'value',
          name: '温度（℃）',
          min: 0,
          max: 1600, // 如果想让纵轴固定在0~1600，可以这样
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: { color: '#ffffff' },
          splitLine: { lineStyle: { color: '#444444' } },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        series: [
          {
            name: '50mm',
            type: 'line',
            data: this.generateOffsetCurve(21, 0, 30, 1600),
            lineStyle: { color: '#ff0000', width: 2 },
            itemStyle: { color: '#ff0000' },
            smooth: true
          },
          {
            name: '100mm',
            type: 'line',
            data: this.generateOffsetCurve(21, 3, 30, 1600),
            lineStyle: { color: '#00ff00', width: 2 },
            itemStyle: { color: '#00ff00' },
            smooth: true
          },
          {
            name: '150mm',
            type: 'line',
            data: this.generateOffsetCurve(21, 6, 30, 1600),
            lineStyle: { color: '#0000ff', width: 2 },
            itemStyle: { color: '#0000ff' },
            smooth: true
          },
          {
            name: '200mm',
            type: 'line',
            data: this.generateOffsetCurve(21, 9, 30, 1600),
            lineStyle: { color: '#ffff00', width: 2 },
            itemStyle: { color: '#ffff00' },
            smooth: true
          },
          {
            name: '250mm',
            type: 'line',
            data: this.generateOffsetCurve(21, 6, 30, 1600),
            lineStyle: { color: '#ff00ff', width: 2 },
            itemStyle: { color: '#ff00ff' },
            smooth: true
          }
        ]
      }
      this.chart1.setOption(option1)

      // 初始化图表 2：煤床压力检测
      this.chart2 = echarts.init(this.$refs.chart2)
      const numPoints = 20 // X 轴上我们准备 20 个点，对应 generateCategories() 的长度
      const option2 = {
        backgroundColor: 'transparent',
        title: {
          text: '煤床压力检测',
          textStyle: { color: '#ffffff' },
          left: 'center',
          top: 30
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: commonGrid,
        xAxis: {
          type: 'category',
          name: '时间',
          data: this.generateCategories(), // 原有函数: 生成 20 个时间刻度
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: {
            color: '#ffffff',
            rotate: 45,
            formatter: (value) =>
              value.length > 5 ? value.slice(0, 5) + '...' : value
          },
          splitLine: { show: false },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        yAxis: {
          type: 'value',
          name: '压力（Mpa）',
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: { color: '#ffffff' },
          splitLine: { lineStyle: { color: '#444444' } },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        legend: {
          show: true,
          textStyle: { color: '#ffffff' },
          top: 0 // 根据需要自行调整
        },
        series: [
          {
            name: '50mm',
            type: 'line',
            data: this.generateNormalDistData(numPoints, 1, 5),
            smooth: true
          },
          {
            name: '100mm',
            type: 'line',
            data: this.generateNormalDistData(numPoints, 3, 10),
            smooth: true
          },
          {
            name: '150mm',
            type: 'line',
            data: this.generateNormalDistData(numPoints, 5, 15),
            smooth: true
          },
          {
            name: '200mm',
            type: 'line',
            data: this.generateNormalDistData(numPoints, 7, 20),
            smooth: true
          },
          {
            name: '250mm',
            type: 'line',
            // 250mm 与 150mm 一样，因此直接复用 150mm 的数组
            data: this.generateNormalDistData(numPoints, 5, 15),
            smooth: true
          }
        ]
      }
      this.chart2.setOption(option2)
      // 初始化图表 3：焦化时间预测（只保留一条曲线）
      this.chart3 = echarts.init(this.$refs.chart3)
      const option3 = {
        backgroundColor: 'transparent',
        title: {
          text: '焦化时间预测',
          textStyle: { color: '#ffffff' },
          left: 'center',
          top: 30
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          show: false // 如果就一条线，可不显示图例
        },
        grid: commonGrid,
        xAxis: {
          type: 'category',
          name: '时间',
          data: this.generateCategories(), // 你已有的函数
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: {
            color: '#ffffff',
            rotate: 45,
            formatter: (value) => value.length > 5 ? value.slice(0, 5) + '...' : value
          },
          splitLine: { show: false },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        yAxis: {
          type: 'value',
          name: '焦化完成时间（h）',
          min: 20, // 让坐标从20开始
          max: 25, // 截止到25
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: { color: '#ffffff' },
          splitLine: { lineStyle: { color: '#444444' } },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        series: [{
          name: '完成焦化时间',
          type: 'line',
          // 先留空或给初始数据，后面要动态推送
          data: [],
          lineStyle: { color: '#0000ff', width: 2 },
          itemStyle: { color: '#0000ff' },
          areaStyle: {
            color: 'rgba(0, 0, 255, 0.3)'
          },
          smooth: true
        }]
      }
      this.chart3.setOption(option3)

      // === 新增 chart4: 胶质层取样器温度检测 ===
      this.chart4 = echarts.init(this.$refs.chart4)
      const option4 = {
        backgroundColor: 'transparent',
        title: {
          text: '胶质层取样器温度检测',
          textStyle: { color: '#ffffff' },
          left: 'center',
          top: 30
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: commonGrid,
        xAxis: {
          type: 'category',
          name: '时间',
          data: this.generateCategories(), // 与其他图表一样，可复用
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: {
            color: '#ffffff',
            rotate: 45,
            formatter: function(value) {
              return value.length > 5 ? value.slice(0, 5) + '...' : value
            }
          },
          splitLine: { show: false },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        yAxis: {
          type: 'value',
          name: '温度（℃）',
          min: 0,
          max: 1600,
          axisLine: { lineStyle: { color: '#ffffff' } },
          axisLabel: { color: '#ffffff' },
          splitLine: { lineStyle: { color: '#444444' } },
          nameTextStyle: { color: '#ffffff', fontSize: 14 }
        },
        series: [{
          name: '胶质层取样器温度',
          type: 'line',
          // 这里您可以用 generateData() 或自定义的 generateIncreasingStableData()
          // 看需求而定
          data: this.generateIncreasingStableData(),
          lineStyle: { color: '#ff6600', width: 2 },
          itemStyle: { color: '#ff6600' },
          areaStyle: {
            color: 'rgba(255, 102, 0, 0.3)'
          },
          smooth: true
        }]
      }
      this.chart4.setOption(option4)
    },
    generateHourCategories() {
      const categories = []
      for (let i = 0; i <= 20; i++) {
        categories.push(`${i}h`)
      }
      return categories
    },
    generateCategories() {
      // 生成 X 轴分类（例如时间或索引）
      const categories = []
      const currentTime = new Date()
      for (let i = 19; i >= 0; i--) {
        const time = new Date(currentTime.getTime() - i * 60000) // 每分钟一个点
        const formattedTime = `${time.getHours()}:${('0' + time.getMinutes()).slice(-2)}`
        categories.push(formattedTime)
      }
      return categories
    },
    generateData() {
      // 生成随机数据
      const data = []
      for (let i = 0; i < 20; i++) {
        data.push(Math.round(Math.random() * 100))
      }
      return data
    },
    updateChartsData() {
      const newCategories = this.generateCategories()
      const newData1 = this.generateIncreasingStableData()
      const newData2 = this.generateIncreasingStableData()
      const newCycleTime = this.generateIncreasingStableData()
      const newTotalCokeTime = this.generateIncreasingStableData()

      // 更新图表1
      if (this.chart1) {
        this.chart1.setOption({
          xAxis: {
            data: newCategories
          },
          series: [{
            data: newData1
          }]
        })
      }

      // 更新图表2
      if (this.chart2) {
        this.chart2.setOption({
          xAxis: {
            data: newCategories
          },
          series: [{
            data: newData2
          }]
        })
      }

      // 更新图表3
      if (this.chart3) {
        this.chart3.setOption({
          xAxis: {
            data: newCategories
          },
          series: [
            {
              name: '预计时间',
              data: newCycleTime
            },
            {
              name: '总焦化时间',
              data: newTotalCokeTime
            }
          ]
        })
      }
    }
  }
}

// 顶点着色器代码
const vertexShader = `
  varying vec3 vWorldPos;
  void main() {
  // 计算世界坐标
  vec4 worldPosition = modelMatrix * vec4(position, 1.0);
  vWorldPos = worldPosition.xyz;

  // 转到裁剪坐标
  gl_Position = projectionMatrix * viewMatrix * worldPosition;
}
`
// 片元着色器代码
const fragmentShader = `
  uniform float uTime;   // 从JS里传进来的动画时间(秒)
  uniform float uMaxX;   // 炉子在 X 方向的一半宽度
  uniform float uCenterX;
  varying vec3 vWorldPos;

  // ========== 辅助函数：HSL 转 RGB ==========
  vec3 hsl2rgb(float H, float S, float L) {
      float C = (1.0 - abs(2.0 * L - 1.0)) * S;
      float Hp = H / 60.0; 
      float X = C * (1.0 - abs(mod(Hp, 2.0) - 1.0));
      
      vec3 rgb;
      if (0.0 <= Hp && Hp < 1.0)      rgb = vec3(C, X, 0.0);
      else if (1.0 <= Hp && Hp < 2.0) rgb = vec3(X, C, 0.0);
      else if (2.0 <= Hp && Hp < 3.0) rgb = vec3(0.0, C, X);
      else if (3.0 <= Hp && Hp < 4.0) rgb = vec3(0.0, X, C);
      else if (4.0 <= Hp && Hp < 5.0) rgb = vec3(X, 0.0, C);
      else if (5.0 <= Hp && Hp < 6.0) rgb = vec3(C, 0.0, X);
      else                            rgb = vec3(0.0, 0.0, 0.0);
      
      float m = L - 0.5*C;
      return rgb + vec3(m);
  }

  void main() {
      // 当前像素与炉子中心线(x=0)的距离
      float dist = abs(vWorldPos.x - uCenterX);
      
      // 最外缘保持红色区域的边界(比如 0.9倍的uMaxX)
      float outerThreshold = 0.9 * uMaxX;

      // 定义动画时长/速度，让 shrinkBoundary 从 outerThreshold 渐变到 0
      float totalDuration = 10.0;   // 10秒内推进
      float p = clamp(uTime / totalDuration, 0.0, 1.0);
      float shrinkBoundary = mix(outerThreshold, 0.0, p);

      // ========== 逻辑判断 ==========

      // 1) dist >= outerThreshold => 最外边始终保持红色
      if (dist >= outerThreshold) {
          gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
          return;
      }

      // 2) 如果 dist 在 [shrinkBoundary, outerThreshold] => 渲染“彩虹渐变”
      if (dist >= shrinkBoundary) {
          float factor = (dist - shrinkBoundary) / (outerThreshold - shrinkBoundary);
          // Hue 从 240(蓝) -> 0(红)
          float hue = mix(240.0, 0.0, factor);
          float saturation = 1.0;
          float lightness = 0.5;
          vec3 rgb = hsl2rgb(hue, saturation, lightness);
          gl_FragColor = vec4(rgb, 1.0);
          return;
      }

      // 3) 如果 dist < shrinkBoundary => 代表尚未被彩虹区覆盖，先渲染成黑色(或其他颜色)
      gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
`
</script>

<style scoped>
.main-container {
  position: relative; /* 使子元素的绝对定位基于此容器 */
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.scene-container {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1; /* 确保 Three.js 场景在底层 */
}

.left-charts-wrapper {
  position: absolute;
  top: 20px;
  left: 20px; /* 这里关键是 left: 20px，放在左侧 */
  width: 400px;
  height: 90%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 10;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5),
              0 0 30px rgba(0, 255, 255, 0.3);
}

.right-charts-wrapper {
  position: absolute; /* 绝对定位，使其悬浮在场景上方 */
  top: 20px; /* 根据需要调整位置，增加顶部间距 */
  right: 20px; /* 将右侧间距设置为20px */
  width: 400px; /* 增加宽度以容纳更多的右边距 */
  height: 90%; /* 占据整个高度，留出顶部和底部间距 */
  display: flex;
  flex-direction: column; /* 垂直排列图表 */
  gap: 20px; /* 增加图表之间的间距 */
  z-index: 10; /* 确保图表在顶层 */
  overflow-y: auto; /* 如果图表高度超过容器，可以滚动 */
  background: rgba(0, 0, 0, 0.3); /* 添加半透明背景以增强科技感 */
  border-radius: 10px; /* 圆角效果 */
  padding: 10px; /* 内边距 */
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5), /* 青色发光 */
              0 0 30px rgba(0, 255, 255, 0.3); /* 更强的发光效果 */
}

.chart-container {
  width: 100%; /* 使每个图表占据容器的全部宽度 */
  height: 50%;
  background-color: transparent; /* 设置为透明 */
  /* 移除统一的边框和阴影 */
  border-radius: 8px; /* 圆角效果 */
  box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2), /* 内部发光 */
              0 0 10px rgba(0, 255, 255, 0.2); /* 外部发光 */
  box-sizing: border-box;
  padding-right: 20px; /* 增加右内边距，防止x轴标签被遮挡 */
}

/* 针对大屏幕进行调整 */
@media (min-width: 1200px) {
  .right-charts-wrapper {
    width: 500px; /* 增加宽度以容纳更宽的图表 */
    top: 60px; /* 根据需要调整位置 */
    right: 30px; /* 根据需要调整位置 */
    height: 85%; /* 根据需要调整高度 */
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.6),
                0 0 40px rgba(0, 255, 255, 0.4);
  }
  .chart-container {
    width: 100%;
    height: 50%; /* 每个图表占30%的高度 */
    box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.3),
                0 0 15px rgba(0, 255, 255, 0.3);
    padding-right: 30px; /* 增加右内边距，确保标签完全显示 */
  }
  .left-charts-wrapper {
    width: 500px;
    top: 60px;
    left: 30px;
    height: 85%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.6),
                0 0 40px rgba(0, 255, 255, 0.4);
  }
}

/* 可选：调整图表内的字体大小 */
.chart-container .echarts-for-react {
  font-size: 14px; /* 增加字体大小 */
}

/* 容器大致定位，可根据你页面需求来摆放 */
.toggle-container {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 999;
  display: flex;
  align-items: center;
}

/* 如果你想在它旁边加文字，就可以加一个 .label-text 的 margin */
.toggle-container .label-text {
  margin-left: 8px;
  color: #fff; /* 文本颜色 (取决于背景) */
}

/* 开关主体 */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;   /* 控制开关整体宽度 */
  height: 28px;  /* 控制开关整体高度 */
  margin-right: 8px;
}

/* 隐藏掉 input[type=checkbox] 原本的显示 */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* 滑块轨道 */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;   /* 关状态的背景 */
  border-radius: 34px;
  transition: .4s;
}

/* 滑块本体 (小圆) */
.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  background-color: #fff; /* 小圆的颜色 */
  transition: .4s;
  border-radius: 50%;
}

/* 选中(ON)时，轨道颜色 & 小圆位置 */
.switch input:checked + .slider {
  background-color: #66bb6a; /* 打开时轨道的颜色, 这里是绿色 */
}
.switch input:checked + .slider:before {
  transform: translateX(22px); /* 小圆往右移动 */
}

.colorbar-container {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  width: 300px;
  height: 20px;
  border: 1px solid #fff;
  border-radius: 4px;
  /* 这里先定义主色带 */
  background:
    linear-gradient(to right,
      #0000ff 0%,
      #00ff00 50%,
      #ff0000 100%
    ),
    /* 然后在上面叠加一层重复的线性渐变竖线(透明+白), 以模拟刻度 */
    repeating-linear-gradient(to right,
      transparent 0,
      transparent 9%,
      rgba(255,255,255,0.8) 9.5%,
      transparent 10%
    );
  background-size: 100% 100%;
  background-blend-mode: overlay;
  /* 下面调节文字位置 */
  .cb-label {
    position: absolute;
    color: #fff;
    top: 30px !important; /* 让文字在渐变条上方一点 */
    font-size: 14px;
  }

  /* 左端的文字 */
  .min-label {
    left: 0;
    transform: translateX(0);
  }

  /* 右端的文字 */
  .max-label {
    right: 0;
    transform: translateX(0);
  }
}
</style>
