<template>
  <div>
    <div class='child-1'>
        <span class='intro'>软件功能模块</span>
        <div class='sub_1'>
        <div>
          <p class='sub_1_text'>模块1：配煤焦炭质量预测</p>
          <p class='sub_1_text_2'>AI算法焦炭质量预测</p>
          <p class='sub_1_text_2'>炼焦过程基础知识</p>
        </div>
        </div>
        <div class='sub_2'>
        <div>
          <p class='sub_1_text'>模块2：配煤方案辅助决策</p>
          <p class='sub_1_text_2'>AI算法最优配煤方案预测</p>
          <p class='sub_1_text_2'>配煤基本理论知识</p>
        </div>
        </div>
        <div class='sub_3'>
        <div>
          <p class='sub_1_text'> 模块3：煤数据处理</p>
          <p class='sub_1_text_2'>煤数据参数解读</p>
          <p class='sub_1_text_2'>煤数据展示及自动分类</p>
        </div>
        </div>
        <div class='sub_4'>
        <div>
          <p class='sub_1_text'>模块4：煤焦化国标</p>
          <p class='sub_1_text_2'>中国煤焦化国家标准</p>
          <p class='sub_1_text_2'>国际煤焦化标准</p>
        </div>
        </div>
        <div class='sub_5'>
        <div>
          <p class='sub_1_text'>模块5：煤床数字孪生模拟</p>
        </div>
        </div>
    </div>
    <div class='child-2'><OriginalCoalNumberBar></OriginalCoalNumberBar></div>
    <div class='child-3'><CoalTypePie></CoalTypePie></div>
    <div class='child-4'><CoalNumberPie></CoalNumberPie></div>
    <div class='child-5'><CokeNumberBar></CokeNumberBar></div>
    <span class='reference'>数据来源参考: https://www.chyxx.com/industry/1123298.html</span>
  </div>
</template>

<script>
import CoalTypePie from './CoalTypePie.vue'
import CoalNumberPie from './CoalNumberPie.vue'
import OriginalCoalNumberBar from './OriginalCoalNumberBar.vue'
import CokeNumberBar from './CokeNumberBar.vue'
export default {
  components: {
    CoalTypePie,
    CoalNumberPie,
    OriginalCoalNumberBar,
    CokeNumberBar
  },
  created() {
    this.$emit('changeActiveStep', 1)
  }
}
</script>

<style>
.child-1{
    position:absolute;
    height: 50%;
    width: 30%;
    background-color:rgba(0,0,0,0.3);
}
.intro{
  position: absolute;
  left: 50%;
  top: 4%;
  color:white;
  font-family: '微软雅黑';
  font-weight:bold;
  font-size: 90%;
  transform: translate(-50%,0%);
  cursor:default;
}
.child-2{
    left: 33%;
    position:absolute;
    height: 40%;
    width: 32%;
    background-color:rgba(0,0,0,0.3);
}
.child-3{
    left: 66.5%;
    position:absolute;
    height: 40%;
    width: 32%;
    background-color:rgba(0,0,0,0.3);
}
.child-4{
    top: 56%;
    position:absolute;
    height: 40%;
    width: 30%;
    background-color:rgba(0,0,0,0.3);
}
.child-5{
    left: 33%;
    top: 46.5%;
    position:absolute;
    height: 49.5%;
    width: 65.5%;
    background-color:rgba(0,0,0,0.3);
}
.sub_1{
  position: absolute;
  width: 43%;
  height: 30%;
  top: 20%;
  left: 4%;
  border: solid 1.5px;
  border-color: #09927b;
  background-color:rgba(32, 209, 167, 0.2);
  display:flex;
  justify-content:center;
  align-items:center;
}
.sub_2{
  position: absolute;
  width: 43%;
  height: 30%;
  top: 20%;
  left: 52%;
  border: solid 1.5px;
  border-color: #09927b;
  background-color:rgba(32, 209, 167, 0.2);
  display:flex;
  justify-content:center;
  align-items:center;
}
.sub_3{
  position: absolute;
  width: 43%;
  height: 30%;
  top: 60%;
  left: 4%;
  border: solid 1.5px;
  border-color: #09927b;
  background-color:rgba(32, 209, 167, 0.2);
  display:flex;
  justify-content:center;
  align-items:center;
}
.sub_4{
  position: absolute;
  width: 43%;
  height: 30%;
  top: 60%;
  left: 52%;
  border: solid 1.5px;
  border-color: #09927b;
  background-color:rgba(32, 209, 167, 0.2);
  display:flex;
  justify-content:center;
  align-items:center;
}
.sub_5{
  position: absolute;
  width: 43%;
  height: 30%;
  top: 60%;
  left: 52%;
  border: solid 1.5px;
  border-color: #09927b;
  background-color:rgba(32, 209, 167, 0.2);
  display:flex;
  justify-content:center;
  align-items:center;
}

.sub_1_text{
  color: #0df1cb;
  font-family: '微软雅黑';
  font-weight:bold;
  font-size: 70%;
  text-align: center;
  margin-top: 3%;
  cursor:default;
}
.sub_1_text_2{
  color: white;
  font-family: '微软雅黑';
  font-size: 65%;
  text-align: center;
  margin-top: -2%;
  cursor:default;
}
.reference{
  position: absolute;
  font-size: 20%;
  color: gray;
  bottom: 1%;
  right: 1.5%;
  cursor:default;
}
</style>
