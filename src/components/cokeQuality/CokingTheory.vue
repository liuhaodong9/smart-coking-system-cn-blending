<template>
  <div>
    <div class="CoalData">
      <div class='selectbutton'>
      <p></p>
      <span class='subtitle_3'>焦炭质量预测</span>
      <el-button id='b11' class='button_2' size="mini" @click='switchAIpredict'>AI算法焦炭质量预测</el-button>
      <el-button id='b10' class='button_2' size="mini" >炼焦过程基础知识</el-button>
      <!-- <el-button id='b12' class='button_2' size="mini" @click='switchAIComparison'>预测性能对比</el-button> -->
      </div>
    <el-card class="box-card_2">
      <p class='description_2'>现代焦炭生产过程分为洗煤、配煤、炼焦和产品处理等工序。</p>
      <p class='contenttitle_2'>洗煤</p>
      <p class='description_2'>原煤在炼焦之前，先进行洗选，其目的是降低煤中所含的灰分和去除其它杂质。</p>
      <p class='contenttitle_2'>配煤</p>
      <p class='description_2'>将各种结焦性能不同的煤按一定比例配合炼焦，其目的是在保证焦炭质量的前提下，扩大炼焦用煤的使用范围，合理地利用国家资源，并尽可能地多得到一些化工产品。</p>
      <p class='contenttitle_2'>炼焦</p>
      <p class='description_2'>将配合好的煤装入炼焦炉的炭化室，在隔绝空气的条件下通过两侧燃烧室加热干馏，经过一定时间，最终形成焦炭。</p>
      <p class='contenttitle_2'>炼焦产品处理</p>
      <p class='description_2'>将炉内推出的红热焦炭送去熄焦塔熄火，然后进行破碎、筛分、分级、获得不同粒度的焦炭产品。其中熄焦有干法和湿法两种，湿法熄焦是用高压水喷淋60-90秒，而干法熄焦则是用惰性气体回收焦炭的物理热，时间为2-4小时。</p>
      <p class='description_2'>除焦炭之外，在炼焦过程中还会产生炼焦煤气及多种化学产品，焦炉煤气是烧结、炼焦、炼铁和炼钢生产的主要燃料。</p>
      <p class='contenttitle_2'>焦炭质量评价</p>
      <p class='description_2'>焦炭在使用过程中会与氧气、二氧化碳或水蒸气之间发生化学反应，焦炭在与这些气体之间的反应过程中所表现出的反应性能的高低，对不同的生产过程有不同的影响。对于冶金焦来说，要求反应性要低，若焦炭的反应性高，则在炉内快速消耗，很快降低焦炭的强度，使冶金过程趋于恶化；若焦炭的反应性低，则在炉内消耗慢，焦炭的强度保持得就好，就有利于冶金过程的稳定进行。</p>
      <p class='description_2'>焦炭反应性指数CRI和反应后强度CSR是反应焦炭在高炉中粒度稳定性的两个重要质量参考指标，前者以损失的焦炭质量占反应前焦样总质量的百分数表示，后者以转鼓后大于10mm粒级焦炭占反应后残余焦炭的质量分数表示。</p>
    </el-card>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    switchAIpredict() {
      this.$router.push('/CokeQualitySelection') // 点击首页按钮切换到coalDataPresent页面
    },
    switchAIComparison() {
    }
  }
}
</script>

<style>
.CoalData{
  position: absolute;
  height: 96%;
  width: 95%;
}
.box-card_2{
  width: 100% !important;
  height: 120%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
}
.button_2{
  /* background:linear-gradient(to top right,#19968e,#27524f,#011629,#011629) !important; */
  /* border: #22b39a !important;; */
  background-color: rgba(0,0,0,0.3) !important;
  border-radius: 0 !important;
  border: none !important;
  font-family: '微软雅黑';
  font-weight:500 !important;
  color: rgb(255, 255, 255) !important;
}
#b10{
  color: rgb(0, 148, 247) !important;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b11{
  right: 12.5%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b12{
  right: 0%;
  top: -2%;
  border: 1px solid #09927b !important;
}
.button_2:hover{
  color: rgb(3, 205, 205) !important;
}
.contenttitle_2{
  color: rgb(0, 148, 247);
  font-family: '微软雅黑';
  font-weight:bold;
  font-size: 80%;
  text-align: left;
  margin-top: 0%;
  cursor:default;
}
.description_2{
  color: white;
  font-size: 80%;
}
.subtitle_3{
  position: absolute;
  color: rgb(12, 158, 255);
  left: 0%;
  font-size: 90%;
}
</style>
