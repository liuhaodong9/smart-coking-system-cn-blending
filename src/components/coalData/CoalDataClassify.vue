<template>
<div>
    <div class="CoalData_2">
      <div class='selectbutton'>
        <p></p>
        <span class='subtitle'>煤数据处理</span>
        <el-button id='b8' class='button_2' size="mini" @click='switchCoalDataPresent'>文本煤数据展示</el-button>
        <el-button id='b9' class='button_2' size="mini" @click='switchCoalDataClassify'>煤数据自动分类</el-button>
        <el-button id='b7' class='button_2' size="mini" @click='switchCoalData'>煤数据参数解读</el-button>
      </div>
        <el-card class="box-card_3">
          <!--辽宁科技大学先进煤焦化技术省重点实验室-原煤数据库-->
            <span class='datasbase_title'>原煤数据库</span>
            <pl-table @selection-change="handleSelectionChange" :row-style="tableRowClassName" ref='CoalTable' id='CoalTable_2' :data='coalList' big-data-checkbox highlight-current-row :row-height="40" use-virtual border :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" :height="height" :key='Math.random()' :default-sort="{prop: 'id', order: 'ascending'}" size='mini' :cell-style="{padding:'0px',fontSize: '14px'}" fixedColumnsRoll>
               <pl-table-column type="selection" width="55" align="center"></pl-table-column>
               <pl-table-column align="center" label='序号' width="80px" prop='id' key="1" ></pl-table-column>
                <pl-table-column align="center" label='煤样名称' prop='coal_name' key="2"></pl-table-column>
                <pl-table-column align="center" label='煤种' prop='coal_type' :key="Math.random()" ></pl-table-column> <!-- 加prop可以直接渲染值 -->
                <pl-table-column align="center" label='价格(吨)' key="5" prop='coal_price'></pl-table-column>
                <pl-table-column align="center" label='挥发分(Vdaf)' width="110px" prop='coal_vdaf' key="35"></pl-table-column>
                <pl-table-column align="center" label='氢(Hdaf)' width="110px" prop='coal_drynoash_hdaf' key="43"></pl-table-column>
                <pl-table-column align="center" label='粘结指数(G)' width="110px" prop='G' key="57"></pl-table-column>
                <pl-table-column align="center" label='Y' width="120px" prop='Y' key="60"></pl-table-column>
                <pl-table-column align="center" label='b/%' width="120px" prop='b'></pl-table-column>
            </pl-table>
            <p class='footnote'>*基于中国煤分类标准</p>
            <div class='Classifybutton_div'>
              <el-button class='Classifybutton' type="primary" @click="sendClassifyData">开始分类</el-button>
            </div>
            <!-- 展示煤分类结果的对话框 -->
        </el-card>
        <el-dialog :lock-scroll='true' class='abow_dialog' top='7vh' title="煤分类结果" custom-class="userDig" center :show-close='true' :closeOnPressEscape='true' :close-on-click-modal="true" :visible.sync="editCoalDetailVisible" :append-to-body="true" width="75%" height='40%'>
            <pl-table :data='coalTypeList' big-data-checkbox highlight-current-row :row-height="33" use-virtual border :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" :height="height" :key='Math.random()' :default-sort="{prop: 'id', order: 'ascending'}" size='mini' :cell-style="{padding:'0px',fontSize: '14px'}" fixedColumnsRoll>
                <pl-table-column align="center" label='序号' prop='id' key="Math.random()" ></pl-table-column>
                <pl-table-column align="center" label='煤样名称' prop='name' key="Math.random()" ></pl-table-column>
                <pl-table-column align="center" label='预测煤类别' prop='predicted_type' key="Math.random()" ></pl-table-column>
            </pl-table>
            <span slot="footer" class='dialog-footer'>
                <el-button class='uploadclass_2' type="primary" @click="uoloadClassifyData"> 上传煤分类结果 </el-button>
                <el-button class='cancel_2' @click="editCoalDetailVisible = false"> 取消 </el-button>
            </span>
        </el-dialog>
    </div>
    <div> <!--切换按钮-->
      <el-button class='last_button' size="mini" type="primary" icon="el-icon-caret-left" @click="returnClassifySelection"></el-button>
      <!-- <p class='switch_2'>返回</p> -->
    </div>
</div>
</template>

<script>
export default {
  created() {
    this.getCoalList()
    this.height = window.screen.height > 850 ? window.screen.height * 0.62 : window.screen.height * 0.481 // 设置表格在不同分辨率电脑的展示大小
  },
  data() {
    return {
      coalList: [],
      coalTypeList: [], // 存储煤分类结果
      multipleSelectionData: [],
      editCoalDetailVisible: false
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
    handleSelectionChange(val) { // 选择多个项
      this.multipleSelectionData = val
    },
    sendClassifyData() {
      const result = this.$http.post('getClassifyeResult', this.multipleSelectionData)
      result.then(res => {
        this.editCoalDetailVisible = true // 展示煤分类结果的对话框
        this.coalTypeList = res.data
      }
      )
    },
    uoloadClassifyData() {
      this.editCoalDetailVisible = false
      const result = this.$http.post('uploadClassifyeResult')
      result.then(res => {
        if (result) {
          this.getCoalList()
        }
      }
      )
    },
    switchCoalData() {
      this.$router.push('/CoalDataProcessing') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCoalDataPresent() {
      this.$router.push('/CoalDataPresent')
    },
    switchCoalDataClassify() { // 煤参数分类跳转按钮
      this.$router.push('/CoalDataClassifySelection')
    },
    returnClassifySelection() {
      this.$router.push('/CoalDataClassifySelection')
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
.box-card_3{
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

#CoalTable_2 th{ /*标题栏背景颜色*/
  background-color: rgb(23, 42, 59)  !important;
  color: white !important;
  font-weight: 500;
}
#CoalTable_2 td{
  background-color: rgba(1, 22, 40,0) !important; /*必须要加透明，与方法里的tableRowClassName搭配使用，呈现的是tableRowClassName里的颜色*/
  color: white !important;
}
.Classifybutton_div{
  margin-top: 2%;
  text-align: right !important;
}
.Classifybutton{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;
}
#CoalTable_2 .el-checkbox__input.is-checked .el-checkbox__inner{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;
}
#CoalTable_2 .el-checkbox__input.is-indeterminate .el-checkbox__inner{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;
}
.uploadclass_2{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;
}
.cancel_2{
  color: rgb(248, 182, 0) !important;
}
.cancel_2:hover{
  color: rgb(248, 182, 0) !important;
}
#b7{
  right: 25%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b8{
  right: 12.5%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b9{
  right: 0%;
  color: rgb(248, 182, 0) !important;
  top: -2%;
  border: 1px solid #09927b !important;
}
.last_button{
  position: fixed;
  width: 1%;
  height: 10%;
  left: 12.5%;
  top: 48%;
  font-size:40px !important;
  background-color: transparent !important;
  border: 0px !important;
  /* background-color: #23978f !important;
  border: 0px !important; */
}
/* .switch_2{
  position: fixed;
  color: white;
  font-size: 12px;
  left: 15%;
  top: 49.5%;
} */
</style>
