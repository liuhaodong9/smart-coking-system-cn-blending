<template>
  <div >
    <!-- 不同图表id名字需要取成不同的，否则只能显示一个图表-->
      <div class="echart" id="echart-pie_2" :style="{position:'absolute',left:'1%',top:'5%', width: '100%', height: '100%'}"></div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      pieData: [
        {
          name: '山西',
          value: 39.3
        },
        {
          name: '河北',
          value: 12.4
        },
        {
          name: '贵州',
          value: 8.1
        },
        {
          name: '河南',
          value: 4.2
        },
        {
          name: '黑龙江',
          value: 4.1
        },
        {
          name: '安徽',
          value: 3.8
        },
        {
          name: '陕西',
          value: 3.8
        },
        {
          name: '云南',
          value: 3.6
        },
        {
          name: '内蒙古',
          value: 2.6
        },
        {
          name: '青海',
          value: 2.6
        },
        {
          name: '其它省份',
          value: 15.5
        }
      ]
    }
  },
  mounted () {
    this.initChart()
  },
  methods: {
    initChart(Data) {
      const getchart = this.$echarts.init(document.getElementById('echart-pie_2'))
      var option = {
        title: { // 通用配置 1
          text: '中国炼焦煤资源分布情况',
          x: 'center', // 标题居中对齐
          textStyle: {
            color: 'white',
            fontSize: 15
          }
        },
        tooltip: { // 提示框组件
          trigger: 'item',
          formatter: '炼焦煤{b}分布占比：{c}%', // 对提示框的内容进行格式化
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
            label: {
              show: true,
              formatter: '{b}: {a|{c}%}', // {d}显示百分比。｛a|｝富文本样式标签。｛b｝数据
              rich: {
                a: {
                  color: '#4B7CF3' // 颜色
                }
              },
              textStyle: {
                fontSize: 11,
                color: 'white'
              }
            },
            radius: ['35%', '55%'] // 参考div的半径
          }

        ],
        color: ['#FF7070', '#CB7BF4', '#4B7CF3', '#F24354', '#32D5B9', '#F19E34', '#9565F4', '#0255FD', '#7ED3F4', '#002E5A', '#FFDC60']
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
