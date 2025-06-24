<template>
  <div>
    <div class="CoalData_2">
      <div class='selectbutton'>
        <p></p>
        <span class='subtitle'>煤数据处理</span>
        <el-button id='b8' class='button_2' size="mini" @click='switchCoalDataPresent'>文本煤数据展示</el-button>
        <el-button id='b9' class='button_2' size="mini">煤数据自动分类</el-button>
        <el-button id='b7' class='button_2' size="mini" @click='switchCoalData'>煤数据参数解读</el-button>
      </div>
      <el-card class="box-card_3">
      <el-card class="box-card_7">
        <div class='source_div'>
        <span class='source'>数据源选择:</span>
        </div>
        <el-upload class='classify_el_upload'>
          <el-button class='button_classify_1' type="primary" @click='switchCoalDataClassifyData'>系统煤数据库</el-button>
        </el-upload>
      </el-card>
      <p></p>
      <el-card class="box-card_8">
        <span class='source'>数据源选择:</span>
        <el-upload class='classify_el_upload' :action="UploadUrl()" multiple :limit="1" :show-file-list='false' accept=".xlsx" :auto-upload='true' :file-list='fileList' :on-success="ClassifyFiles"> <!--记得先导入模块-->
          <el-button class='button_classify_2' type="primary">用户自选数据</el-button>
        </el-upload>
      </el-card>
      <p> ㅤ</p>
      <p class='note_classify'>*煤数据自动分类使用注意事项</p>
      <p> ㅤ</p>
      <p class='note_classify'>1. 运行煤数据自动分类算法时，有两个数据来源可供选择：系统煤数据库和用户自选数据。</p>
      <p> ㅤ</p>
      <p class='note_classify'>2. 点击系统煤数据库时，界面将跳转至系统煤数据库数据选择界面，点击用户自选数据时，要求用户上传带有待分类的煤数据.xlsx文件（数据导入模板可见下方下载）。</p>
      <p> ㅤ</p>
      <p class='note_classify'>3. 用户上传自选数据时，建议提供“煤样挥发分(Vdaf)”，“氢(Hdaf)”，“粘结指数(G)”，“Y”和“b/%”等参数信息来辅助系统进行煤类型的精确分类。在缺失相关参数的情况下，可能会导致算法判据不足，无法提供结果。</p>
      <p> ㅤ</p>
      <p><a href='http://1.116.164.66:5000/templatedownload' class='datatemplate_2'>数据导入模板下载</a></p>
      </el-card>
      <el-dialog :lock-scroll='true' class='abow_dialog' top='7vh' title="煤分类结果" custom-class="userDig" center :show-close='true' :closeOnPressEscape='true' :close-on-click-modal="true" :visible.sync="editCoalVisible" :append-to-body="true" width="75%" height='40%'>
          <pl-table :data='coalTypeList' big-data-checkbox highlight-current-row :row-height="33" use-virtual border :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" :height="height" :key='Math.random()' :default-sort="{prop: 'id', order: 'ascending'}" size='mini' :cell-style="{padding:'0px',fontSize: '14px'}" fixedColumnsRoll>
              <pl-table-column align="center" label='序号' prop='id' key="Math.random()" ></pl-table-column>
              <pl-table-column align="center" label='煤样名称' prop='name' key="Math.random()" ></pl-table-column>
              <pl-table-column align="center" label='预测煤类别' prop='predicted_type' key="Math.random()" ></pl-table-column>
          </pl-table>
          <span slot="footer" class='dialog-footer'>
              <el-button class='uploadclass_1' type="primary" @click="uoloadUserClassifyData"> 上传煤分类结果 </el-button>
              <el-button class='cancel_1' @click="editCoalVisible = false"> 取消 </el-button>
          </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      coalTypeList: [], // 存储煤分类结果
      fileList: [], // 上传文件的列表
      editCoalVisible: false
    }
  },
  methods: {
    switchCoalData() { // 煤参数数据解读跳转按钮
      this.$router.push('/CoalDataProcessing') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCoalDataPresent() {
      this.$router.push('/CoalDataPresent')
    },
    switchCoalDataClassifyData() {
      this.$router.push('/CoalDataClassify')
    },
    UploadUrl() { // 用来返回煤数据导入的url
      return 'http://1.116.164.66:5000//UploadUserCoalData'
    },
    ClassifyFiles() {
      this.fileList = [] // 当文件上传成功后，删除文件列表，以防止上传完一次后无法上传
      this.$message.success('数据上传成功！')
      const result = this.$http.post('ClassifydUserCoalData')
      result.then(res => {
        this.editCoalVisible = true // 展示煤分类结果的对话框
        this.coalTypeList = res.data
      }
      )
    },
    uoloadUserClassifyData() {
      this.editCoalVisible = false
      const result = this.$http.post('uploadUserClassifyeResult')
      result.then(res => {
        if (result) {
          this.$message.success('数据上传成功！')
        }
      }
      )
    }
  }
}
</script>

<style>
.source{
  position: absolute;
  color: white;
  font-size: 120% !important;
  left: 10%;
  padding-top: 2%;
}
.box-card_7{
  width: 100% !important;
  height: 30%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
  margin-top: 2% !important;
  display:flex;
  justify-content:center;
  align-items:center;
}
.box-card_8{
  width: 100% !important;
  height: 30%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
  display:flex;
  justify-content:center;
  align-items:center;
}
.button_classify_1{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;
  width: 270%;
  font-size: 140% !important;
  line-height: 200% !important; /*控制按钮的高度*/
  margin-top: -10% !important;
  margin-left: -30% !important;
}
.button_classify_2 {
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0)!important;
  width: 270% !important;
  font-size: 140% !important;
  line-height: 200% !important; /*控制按钮的高度*/
  margin-top: -10% !important;
  margin-left: -30% !important;
}
.note_classify{
  margin-top: 1%;
  color: white;
  font-size: 80%;
}
.datatemplate_2{
  color: yellow;
  font-size: 80%;
}
.classify_el_upload{
  width: 100% !important;
  margin-left: 39.5% !important;
  margin-top: 10% !important;
}
.uploadclass_1{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;;
}
.cancel_1{
  border-color: rgb(248, 182, 0) !important;;
}
</style>
