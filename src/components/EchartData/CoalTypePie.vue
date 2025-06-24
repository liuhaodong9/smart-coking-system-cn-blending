<template>
  <div >
    <!-- 不同图表id名字需要取成不同的，否则只能显示一个图表-->
      <div class="echart" id="echart-pie_" :style="{position:'absolute',left:'1%',top:'5%', width: '100%', height: '110%'}"></div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      pieData: [
        {
          name: '焦煤',
          value: 34.2
        },
        {
          name: '瘦煤',
          value: 23.2
        },
        {
          name: '肥煤',
          value: 15.8
        },
        {
          name: '气肥煤',
          value: 7.6
        },
        {
          name: '1/3焦煤',
          value: 7.2
        },
        {
          name: '其它煤种',
          value: 12
        }
      ]
    }
  },
  mounted () {
    this.initChart()
  },
  methods: {
    initChart(Data) {
      const getchart = this.$echarts.init(document.getElementById('echart-pie_'))
      var option = {
        title: { // 通用配置 1
          text: '中国炼焦煤煤种占比情况',
          x: 'center', // 标题居中对齐
          textStyle: {
            color: 'white',
            fontSize: 15
          }
        },
        tooltip: { // 提示框组件
          trigger: 'item',
          formatter: '{b}占比：{c}%', // 对提示框的内容进行格式化
          confine: true // 限制tootip在容器内
        },
        toolbox: { // 内置的工具栏
          feature: {
            saveAsImage: {}, // 导出图片
            dataView: {} // 数据视图
          },
          right: '4%' // 距离右边多远
        },
        series: [
          {
            type: 'pie',
            data: this.pieData,
            roseType: 'angle',
            label: {
              show: true,
              formatter: '{b}: {a|{c}%}', // {d}显示百分比。｛a|｝富文本样式标签。｛b｝数据
              rich: {
                a: {
                  color: '#1ac1b9' // 颜色
                }
              },
              textStyle: {
                fontSize: 11,
                color: 'white'
              }
            },
            radius: '50%' // 参考div的半径
          }

        ]
      }
      getchart.setOption(option)
      window.addEventListener('resize', () => {
        getchart.resize()
      })
    }
  }
}
</script>

<style lang="less" scoped>
</style>
