<template>
  <div>
    <div class="CoalData_2">
    <div class='selectbutton'>
      <p></p>
      <span class='subtitle_2'>焦炭质量预测</span>
      <el-button id='b14' class='button_2' size="mini" >AI算法焦炭质量预测</el-button>
      <el-button id='b13' class='button_2' size="mini" @click='switchCoalTheory'>炼焦过程基础知识</el-button>
      <!-- <el-button id='b15' class='button_2' size="mini">预测性能对比</el-button> -->
    </div>
    <el-card class="box-card_4">
      <!--辽宁科技大学先进煤焦化技术省重点实验室-原煤数据库-->
      <span class='datasbase_title'>原煤数据库</span>
        <pl-table @selection-change="handleSelectionChange" :row-style="tableRowClassName" id='CoalTable_3' :data='coalList' big-data-checkbox highlight-current-row :row-height="40" use-virtual border :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" :height="height" :key='Math.random()' :default-sort="{prop: 'id', order: 'ascending'}" size='mini' :cell-style="{padding:'0px',fontSize: '14px'}" fixedColumnsRoll>
            <pl-table-column type="selection" width="55" align="center"></pl-table-column>
            <pl-table-column align="center" label='序号' width="80px" prop='id' key="1" fixed ></pl-table-column>
            <pl-table-column align="center" label='煤样名称' width="140px" prop='coal_name' key="2" fixed></pl-table-column>
            <pl-table-column align="center" label='煤种' prop='coal_type' key="3" fixed></pl-table-column> <!-- 加prop可以直接渲染值 -->
            <pl-table-column align="center" label='水分(Mad)' width="90px" prop='coal_mad' key="33"></pl-table-column>
            <pl-table-column align="center" label='灰分(Ad)' width="90px" prop='coal_ad' key="34"></pl-table-column>
            <pl-table-column align="center" label='挥发分(Vdaf)' width="90px" prop='coal_vdaf' key="35"></pl-table-column>
            <pl-table-column align="center" label='全硫(St,d)' width="90px" prop='coal_std' key="41"></pl-table-column>
            <pl-table-column align="center" label='粘结指数(G)' width="90px" v-if='show_5' prop='G' key="57"></pl-table-column>
            <pl-table-column align="center" label='X' width="90px" prop='X' key="59"></pl-table-column>
            <pl-table-column align="center" label='Y' width="90px" prop='Y' key="60"></pl-table-column>
            <pl-table-column align="center" label='焦炭质量真实值' prop='predicted_type' key="Math.random()" >
                <pl-table-column align="center" label='CRI' prop='coke_CRI' width="105px"></pl-table-column>
                <pl-table-column align="center" label='CSR' prop='coke_CSR' width="105px"></pl-table-column>
            </pl-table-column>
            <pl-table-column align="center" label='焦炭质量预测值(人工智能算法)' prop='predicted_type' key="Math.random()">
                <pl-table-column align="center" label='CRI' prop='predicted_CRI'  width="105px"></pl-table-column>
                <pl-table-column align="center" label='CSR' prop='predicted_CSR'  width="105px"></pl-table-column>
            </pl-table-column>
        </pl-table>
        <div class='Classifybutton_div'>
          <el-button class='Classifybutton_2' type="primary" @click="sendPredictedData">开始预测</el-button>
        </div>
        <!-- 展示煤分类结果的对话框 -->
    </el-card>
    <el-dialog :lock-scroll='true' class='abow_dialog' top='7vh' title="焦炭质量预测结果(人工智能算法)" custom-class="userDig" center :show-close='true' :closeOnPressEscape='true' :close-on-click-modal="true" :visible.sync="editCoalDetailVisible" :append-to-body="true" width="75%" height='40%'>
        <pl-table ref='CoalTable' :data='coalQualityList' big-data-checkbox highlight-current-row :row-height="36"  border :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" :height="height" :key='Math.random()' :default-sort="{prop: 'id', order: 'ascending'}" size='mini' :cell-style="{padding:'0px',fontSize: '14px'}" fixedColumnsRoll>
            <pl-table-column align="center" label='序号' prop='id'></pl-table-column>
            <pl-table-column align="center" label='煤样名称' prop='coal_name'></pl-table-column>
            <pl-table-column align="center" label='焦炭质量预测值' prop='predicted_type'>
                <pl-table-column align="center" label='CRI' prop='CRI' ></pl-table-column>
                <pl-table-column align="center" label='CSR' prop='CSR' ></pl-table-column>
                <!-- <pl-table-column align="center" label='M10' prop='M10' ></pl-table-column>
                <pl-table-column align="center" label='M25' prop='M25'></pl-table-column> -->
            </pl-table-column>
            <pl-table-column align="center" label='焦炭质量真实值' prop='predicted_type'>
                <pl-table-column align="center" label='CRI' prop='real_CRI' ></pl-table-column>
                <pl-table-column align="center" label='CSR' prop='real_CSR' ></pl-table-column>
                <!-- <pl-table-column align="center" label='M10' prop='real_M10' ></pl-table-column>
                <pl-table-column align="center" label='M25' prop='real_M25'></pl-table-column> -->
            </pl-table-column>
            <pl-table-column align="center" label='预测误差百分比' prop='predicted_type'>
                <pl-table-column align="center" label='CRI' prop='error_CRI' ></pl-table-column>
                <pl-table-column align="center" label='CSR' prop='error_CSR' ></pl-table-column>
                <!-- <pl-table-column align="center" label='M10' prop='real_M10' ></pl-table-column>
                <pl-table-column align="center" label='M25' prop='real_M25'></pl-table-column> -->
            </pl-table-column>
        </pl-table>
        <span slot="footer" class='dialog-footer'>
            <el-button type="primary" @click="uploadQualityData"> 上传预测结果 </el-button>
            <el-button @click="editCoalDetailVisible = false"> 取消 </el-button>
        </span>
        <p></p>
        <el-row>
          <span style="font-weight:normal">本数据采用支持向量机算法进行预测，总平均预测误差百分比  ——ㅤCRI: {{AverageCRIError}}%， CSR: {{AverageCSRError}}%</span>
        </el-row>
    </el-dialog>
    </div>
        <div> <!--切换按钮-->
          <el-button class='last_button' size="mini" type="primary" icon="el-icon-caret-left" @click="returnSelection"></el-button>
        <!-- <p class='switch_2'>返回</p> -->
        </div>
  </div>
</template>

<script>
export default {
  created() {
    this.getCoalList()
    this.height = window.screen.height > 850 ? window.screen.height * 0.62 : window.screen.height * 0.481 // 需要设置，控制表格高度
  },
  data() {
    return {
      coalList: [],
      coalQualityList: [], // 存储煤质量预测结果
      multipleSelectionData: [],
      editCoalDetailVisible: false,
      AverageCRIError: '',
      AverageCSRError: ''
    }
  },
  methods: {
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex % 2 === 0) {
        return 'background-color:rgba(0, 21, 40, 1) !important;'
      }
      if (rowIndex % 2 === 1) {
        return 'background-color:rgba(0, 21, 40, 0.7) !important;'
      }
    },
    async getCoalList() { // 不能和煤数据上传与查看共用一个接口
      await this.$http.get('getClassifyeData').then(ret => {
        this.coalList = ret.data.msg // 取具体的数值
        this.coalList.reverse()
      }
      )
    },
    handleSelectionChange(val) {
      this.multipleSelectionData = val
    },
    sendPredictedData() { // 发送待预测的数据
      const result = this.$http.post('getCokeQualityfyeResultAISVR', this.multipleSelectionData)
      result.then(res => {
        if (res.data[0] === 'Error') {
          this.$confirm('所选待预测的煤种中有缺少水分、灰分、挥发分、硫分、粘结指数G，X和Y等参数', '提示', {
            confirmButtonText: '确定',
            type: 'warning',
            showCancelButton: false
          })
        } else {
          this.editCoalDetailVisible = true // 展示煤分类结果的对话框
          this.coalQualityList = res.data
          this.AverageCRIError = this.coalQualityList[this.coalQualityList.length - 2]
          this.AverageCSRError = this.coalQualityList[this.coalQualityList.length - 1]
        }
      }
      )
    },
    uploadQualityData() {
      this.editCoalDetailVisible = false
      const result = this.$http.post('uploadQualityResult')
      result.then(res => {
        if (result) {
          this.getCoalList()
        }
      }
      )
    },
    switchCoalTheory() {
      this.$router.push('/CokingTheory')
    },
    returnSelection() {
      this.$router.push('/CokeQualitySelection')
    }
  }
}
</script>

<style>

.button_2{
  /* background:linear-gradient(to top right,#19968e,#27524f,#011629,#011629) !important; */
  /* border: #22b39a !important;; */
  background-color: rgba(0,0,0,0.3) !important;
  border-radius: 0 !important;
  font-family: '微软雅黑';
  font-weight:500 !important;
  color: rgb(255, 255, 255) !important;
}
.box-card_4{
  width: 100% !important;
  height: 95%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
}
.button_2:hover{
  color: rgb(3, 205, 205) !important;
}

.footnote{
    float: left;
    color: white;
}

#CoalTable_3 th{ /*标题栏背景颜色*/
  background-color: rgb(23, 42, 59)  !important;
  color: white !important;
  font-weight: 500;
}
#CoalTable_3 td{
  background-color: rgba(1, 22, 40,0) !important; /*必须要加透明，与方法里的tableRowClassName搭配使用，呈现的是tableRowClassName里的颜色*/
  color: white !important;
}
.Classifybutton_div{
  margin-top: 2%;
  text-align: right !important;
}
.Classifybutton_2{
  background-color: rgb(0, 148, 247)  !important;
  border-color: rgb(0, 148, 247) !important;
}
#CoalTable_3 .el-checkbox__input.is-checked .el-checkbox__inner{
  background-color: rgb(0, 148, 247)  !important;
  border-color: rgb(0, 148, 247)  !important;
}
#CoalTable_3 .el-checkbox__input.is-indeterminate .el-checkbox__inner{
  background-color: rgb(91, 138, 255) !important;
  border-color: rgb(91, 138, 255) !important;
}
.uploadclass{
  background-color: rgb(0, 148, 247)  !important;
  border-color: rgb(0, 148, 247)  !important;
}
.cancel{
  color: rgb(0, 148, 247)  !important;
}
.cancel:hover{
  color: rgb(0, 148, 247)  !important;
}
#b13{
  right: 25%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b14{
  right: 12.5%;
  top: -2%;
  color: rgb(0, 148, 247) !important;
  border: 1px solid #09927b !important;
}
#b15{
  right: 0%;
  top: -2%;
  border: 1px solid #09927b !important;
}
.subtitle_2{
  position: absolute;
  color: rgb(0, 148, 247);
  left: 0%;
  font-size: 90%;
}
</style>
