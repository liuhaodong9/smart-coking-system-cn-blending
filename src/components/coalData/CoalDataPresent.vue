<template>
  <div>
    <div class="CoalData_2">
      <div class='selectbutton'>
        <p></p>
        <span class='subtitle'>煤数据处理</span>
        <el-button id='b5' class='button_2' size="mini">文本煤数据展示</el-button>
        <el-button id='b6' class='button_2' size="mini" @click='switchCoalDataClassify'>煤数据自动分类</el-button>
        <el-button id='b4' class='button_2' size="mini" @click='switchCoalData'>煤数据参数解读</el-button>
    </div>
    <el-card class="box-card_3">
        <el-row><!--分栏-->
            <el-col :span="5">
                <div>
                    <input class='input_query' placeholder=" 请输入查找的煤种" v-model.lazy="queryInfo.query"> <!-- 用原始input+lazy属性不会造成卡顿 -->
                </div>
            </el-col>
            <el-col :span="4">
              <div>
                <el-button class='query_button' slot="append" icon="el-icon-search" @click="getCoalList"></el-button>
              </div>
            </el-col>
            <el-col :span="4">
              <div>
                <el-button size="small" type="primary" class='dataupload_2' @click="editRatioCoalVisible_2 = true">原煤数据导入</el-button>
                <!-- <el-upload class="upload-demo" :action="UploadUrl()" multiple :limit="1" :show-file-list='false' accept=".xlsx" :auto-upload='true' :file-list='fileList' :on-success="RemoveFiles"> 记得先导入模块 -->
                  <!-- <el-button size="small" type="primary" class='dataupload'>原煤数据导入</el-button> -->
                  <!-- <div slot="tip" class="el-upload__tip">&nbsp;&nbsp;&nbsp;只接收.xlsx文件</div>
                </el-upload> -->
              </div>
            </el-col>
            <el-col :span="6">
                <a href='http://1.116.164.66:5000/templatedownload' class='datatemplate'>数据导入模板下载</a>
            </el-col>
            <!-- 添加煤数据按钮 -->
            <el-col :span="10" class='selectShow'> <!-- 记得注册组件 -->
                <el-select class='select_show' collapse-tags v-model="chooseData" multiple placeholder="请选择" @change='selectAll'>
                    <el-option
                    v-for="item in selectOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span="5" class='showName'><p class='showPra'>选择显示的参数:</p></el-col>
        </el-row>
        <!--辽宁科技大学先进煤焦化技术省重点实验室-原煤数据库-->
        <el-row gutter="22"><span class='datasbase_title'>原煤数据库</span></el-row>
        <CoalDataTable ref='child1' :editCoalDetailVisible='editCoalDetailVisible' :show_1='show_1' :show_2='show_2' :show_3='show_3' :show_4='show_4' :show_5='show_5' :show_6='show_6' :show_7='show_7' :show_8='show_8' :show_9='show_9' :show_10='show_10' :show_11='show_11' :show_12='show_12' :show_13='show_13' :show_14='show_14' :show_15='show_15' :show_16='show_16' :show_17='show_17' :show_18='show_18' :queryInfo_get='queryInfo'></CoalDataTable>
        <el-dialog :lock-scroll='true' class='abow_dialog' top='7vh' title="原煤数据导入流程" custom-class="userDig" center :show-close='true' :closeOnPressEscape='true' :close-on-click-modal="true" :visible.sync="editRatioCoalVisible_2" :append-to-body="true" width="75%" height='40%'>
        <p>1. 点击“煤数据处理页面”中“文本煤数据展示”模块的“数据导入模板下载”，系统会自动将以后缀名为.xlsx格式的数据导入模板文件加载到用户本地</p>
        <p>ㅤ</p>
        <p>2. 打开.xlsx文件，根据每列参数名，输入相对应的煤参数信息，对于未填入的数据,系统会自动识别为空值存储.</p>
        <p>ㅤ</p>
        <p>3. 点击本页面下方的“数据上传”按钮,选择已填好的后缀名为.xlsx格式的文件,并将其进行上传.上传成功后,页面会自动刷新并提示"数据上传成功！"</p>
        <p>ㅤ</p>
        <p>(上传时,勿随意修改模板,目前系统暂不接受用户自定义列参数名，如有特定需求，请联系系统相关技术维护人员)</p>
        <p>ㅤ</p>
        <div>
        <el-upload class="upload-demo" :action="UploadUrl()" multiple :limit="1" :show-file-list='false' accept=".xlsx" :auto-upload='true' :file-list='fileList' :on-success="RemoveFiles"> <!-- 记得先导入模块 -->
          <el-button type="primary" class='dataupload'>数据上传</el-button>
          <!-- <div slot="tip" class="el-upload__tip">&nbsp;&nbsp;&nbsp;只接收.xlsx文件</div> -->
        </el-upload>
        </div>
        </el-dialog>
    </el-card>
    </div>
  </div>
</template>

<script>
import CoalDataTable from './CoalDataTable' // 引入组件
export default {
  components: {
    CoalDataTable
  },
  data() {
    return {
      // 获取煤数据参数对象
      queryInfo: {
        query: ''
      },
      editRatioCoalVisible_2: false,
      height: 250,
      selectOptions: [{
        value: 'ALL_SELECT',
        label: '选中所有'
      }, {
        value: '选项1',
        label: '原始试验煤样筛分组成'
      }, {
        value: '选项2',
        label: '粉碎后筛分组成'
      }, {
        value: '选项3',
        label: '煤样工业分析'
      }, {
        value: '选项4',
        label: '煤样元素分析'
      }, {
        value: '选项5',
        label: '粘结指数与胶质层指数'
      }, {
        value: '选项6',
        label: '奥亚膨胀度'
      }, {
        value: '选项7',
        label: '基氏流动度'
      }, {
        value: '选项8',
        label: '煤灰熔点/℃'
      }, {
        value: '选项9',
        label: '灰成分'
      }, {
        value: '选项10',
        label: '煤样显微组分分析'
      }, {
        value: '选项11',
        label: '炼焦过程参数'
      }, {
        value: '选项12',
        label: '炼焦温度参数'
      }, {
        value: '选项13',
        label: '焦炭工业分析'
      }, {
        value: '选项14',
        label: '焦炭筛分组成'
      }, {
        value: '选项15',
        label: '焦炭机械强度与热性质'
      }, {
        value: '选项16',
        label: '焦炭灰熔点'
      }, {
        value: '选项17',
        label: '粉焦反应性'
      }, {
        value: '选项18',
        label: '气孔率'
      }],
      oldChooseData: [],
      chooseData: [],

      // 变量判断显示的列
      show_1: false,
      show_2: false,
      show_3: true,
      show_4: true,
      show_5: true,
      show_6: false,
      show_7: false,
      show_8: false,
      show_9: false,
      show_10: true, // 显微组分分析
      show_11: false,
      show_12: false,
      show_13: false,
      show_14: false,
      show_15: false,
      show_16: false,
      show_17: false,
      show_18: false,
      // 显示添加煤数据的对话框
      adddialogVisible: false,
      // 显示对话框展示的元素
      showCoalInformation: false,
      showOriginalCoalScreen: false,
      showCrushCoalScreen: false,
      showIndustrialCoal: false,
      showElementCoal: false,
      showGXYCoal: false,
      showInflationCoal: false,
      showFluidCoal: false,
      showMeltCoal: false,
      showAshCoal: false,
      showMicroCoal: false,
      showProcessCoal: false,
      showTempCoal: false,
      showIndustrialCoke: false,
      showCokeScreen: false,
      showStrengthHot: false,
      showMeltCoke: false,
      showReactCoke: false,
      showPoreCoke: false,
      editCoalDetailVisible: false,

      fileList: [] // 上传文件的列表
    }
  },
  created() {
    const allValues = this.selectOptions.map(item => {
      return item.value
    })
    var showDataFirst = []// 刚登陆进行默认展示的数据选项
    showDataFirst.push(allValues[3])
    showDataFirst.push(allValues[4])
    showDataFirst.push(allValues[5])
    showDataFirst.push(allValues[10])
    this.chooseData = showDataFirst // 记住2个都要赋值，才可以默认选中取消，否则需要点击2次
    this.oldChooseData = showDataFirst
    this.$emit('changeActiveStep', 2)
  },
  methods: {
    switchCoalData() { // 煤参数数据解读跳转按钮
      this.$router.push('/CoalDataProcessing') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCoalDataClassify() { // 煤参数分类跳转按钮
      this.$router.push('/CoalDataClassifySelection')
    },
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex % 2 === 0) {
        return 'background-color:#E8E8E8;'
      }
    },
    getCoalList() {
      this.$refs.child1.getCoalList() // 调用子组件方法，按键索引指定数据
    },
    RemoveFiles() {
      this.fileList = [] // 当文件上传成功后，删除文件列表，以防止上传完一次后无法上传
      this.$message.success('数据上传成功！')
      location.reload()
    },
    selectAll (val) {
      this.editCoalDetailVisible = false
      // 根据点击的值改变显示的列
      const allValues = this.selectOptions.map(item => {
        return item.value
      })

      // 用来储存上一次选择的值，可进行对比
      const oldVal = this.oldChooseData.length > 0 ? this.oldChooseData : []

      // 若选择全部
      if (val.includes('ALL_SELECT')) {
        this.chooseData = allValues
      }
      // 取消全部选中， 上次有， 当前没有， 表示取消全选
      if (oldVal.includes('ALL_SELECT') && !val.includes('ALL_SELECT')) {
        this.chooseData = []
      }
      // 点击非全部选中，需要排除全部选中 以及 当前点击的选项
      // 新老数据都有全部选中
      if (oldVal.includes('ALL_SELECT') && val.includes('ALL_SELECT')) {
        const index = val.indexOf('ALL_SELECT')
        val.splice(index, 1) // 排除全选选项
        this.chooseData = val
      }
      // 全选未选，但是其他选项都全部选上了，则全选选上
      if (!oldVal.includes('ALL_SELECT') && !val.includes('ALL_SELECT')) {
        if (val.length === allValues.length - 1) {
          this.chooseData = ['ALL_SELECT'].concat(val)
        }
      }
      // 储存当前选择的最后结果 作为下次的老数据
      this.oldChooseData = this.chooseData

      var result0 = val.includes('ALL_SELECT') // 记得是索引val 不是 chooseData

      var result1 = val.includes('选项1') // 记得是索引val 不是 chooseData
      if (result1) {
        this.show_1 = true
      } else {
        this.show_1 = false
      }

      var result2 = val.includes('选项2')
      if (result2 || result0) {
        this.show_2 = true
      } else {
        this.show_2 = false
      }

      var result3 = val.includes('选项3')
      if (result3 || result0) {
        this.show_3 = true
      } else {
        this.show_3 = false
      }

      var result4 = val.includes('选项4')
      if (result4 || result0) {
        this.show_4 = true
      } else {
        this.show_4 = false
      }

      var result5 = val.includes('选项5')
      if (result5 || result0) {
        this.show_5 = true
      } else {
        this.show_5 = false
      }

      var result6 = val.includes('选项6')
      if (result6 || result0) {
        this.show_6 = true
      } else {
        this.show_6 = false
      }

      var result7 = val.includes('选项7')
      if (result7 || result0) {
        this.show_7 = true
      } else {
        this.show_7 = false
      }

      var result8 = val.includes('选项8')
      if (result8 || result0) {
        this.show_8 = true
      } else {
        this.show_8 = false
      }

      var result9 = val.includes('选项9')
      if (result9 || result0) {
        this.show_9 = true
      } else {
        this.show_9 = false
      }

      var result10 = val.includes('选项10')
      if (result10 || result0) {
        this.show_10 = true
      } else {
        this.show_10 = false
      }

      var result11 = val.includes('选项11')
      if (result11 || result0) {
        this.show_11 = true
      } else {
        this.show_11 = false
      }

      var result12 = val.includes('选项12')
      if (result12 || result0) {
        this.show_12 = true
      } else {
        this.show_12 = false
      }

      var result13 = val.includes('选项13')
      if (result13 || result0) {
        this.show_13 = true
      } else {
        this.show_13 = false
      }

      var result14 = val.includes('选项14')
      if (result14 || result0) {
        this.show_14 = true
      } else {
        this.show_14 = false
      }

      var result15 = val.includes('选项15')
      if (result15 || result0) {
        this.show_15 = true
      } else {
        this.show_15 = false
      }

      var result16 = val.includes('选项16')
      if (result16 || result0) {
        this.show_16 = true
      } else {
        this.show_16 = false
      }

      var result17 = val.includes('选项17')
      if (result17 || result0) {
        this.show_17 = true
      } else {
        this.show_17 = false
      }

      var result18 = val.includes('选项18')
      if (result18 || result0) {
        this.show_18 = true
      } else {
        this.show_18 = false
      }
      if (this.chooseData.length === 0) { // 注意是chooseData而不是val输入值
        this.editCoalDetailVisible = false
        this.show_1 = false
        this.show_2 = false
        this.show_3 = false
        this.show_4 = false
        this.show_5 = false
        this.show_6 = false
        this.show_7 = false
        this.show_8 = false
        this.show_9 = false
        this.show_10 = false
        this.show_11 = false
        this.show_12 = false
        this.show_13 = false
        this.show_14 = false
        this.show_15 = false
        this.show_16 = false
        this.show_17 = false
        this.show_18 = false
      }
      if (this.chooseData.length === 19 && this.chooseData.includes('ALL_SELECT')) {
        this.editCoalDetailVisible = false
        this.show_1 = true
        this.show_2 = true
        this.show_3 = true
        this.show_4 = true
        this.show_5 = true
        this.show_6 = true
        this.show_7 = true
        this.show_8 = true
        this.show_9 = true
        this.show_10 = true
        this.show_11 = true
        this.show_12 = true
        this.show_13 = true
        this.show_14 = true
        this.show_15 = true
        this.show_16 = true
        this.show_17 = true
        this.show_18 = true
      }
    },
    reload() {
      this.$forceUpdate()
    },
    // 根据ID删除对应的用户信息
    removeCoalById(id) {
      this.$confirm('此操作将永久删除该条数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 显示对话框展示的元素
    click_showCoalInformation() {
      this.showCoalInformation = true
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showOriginalCoalScreen() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = true
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showCrushCoalScreen() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = true
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showIndustrialCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = true
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showElementCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = true
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showGXYCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = true
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showInflationCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = true
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showFluidCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = true
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showMeltCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = true
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showAshCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = true
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showMicroCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = true
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showProcessCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = true
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showTempCoal() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = true
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showIndustrialCoke() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = true
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showCokeScreen() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = true
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showStrengthHot() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = true
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showMeltCoke() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = true
      this.showReactCoke = false
      this.showPoreCoke = false
    },
    click_showReactCoke() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = true
      this.showPoreCoke = false
    },
    click_showPoreCoke() {
      this.showCoalInformation = false
      this.showOriginalCoalScreen = false
      this.showCrushCoalScreen = false
      this.showIndustrialCoal = false
      this.showElementCoal = false
      this.showGXYCoal = false
      this.showInflationCoal = false
      this.showFluidCoal = false
      this.showMeltCoal = false
      this.showAshCoal = false
      this.showMicroCoal = false
      this.showProcessCoal = false
      this.showTempCoal = false
      this.showIndustrialCoke = false
      this.showCokeScreen = false
      this.showStrengthHot = false
      this.showMeltCoke = false
      this.showReactCoke = false
      this.showPoreCoke = true
    },
    UploadUrl() { // 用来返回煤数据导入的url
      return 'http://1.116.164.66:5000//UploadCoalData'
    }
  }

}
</script>

<style>
.CoalData_2{
  position: absolute;
  height: 96%;
  width: 95%;
}
.box-card_3{
  width: 100% !important;
  height: 95% !important;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
}
.showPra{
  position: absolute;
  margin-top:10px;
  color:rgb(231, 231, 231);
  font-weight: bold;
  left: 62%;
}
.selectShow{
    position: absolute;
    left: 75%;
}
.input_query{
  outline-style: none;
  border: 1.4px solid #4DA4FF;
  border-radius: 3px;
  padding: 11px 0px;
  width: 80%
}
/* .input_query{
  background-color: #0c4275;
} */

.query_button{
  margin-left: -15% !important;
  color: rgb(248, 182, 0) !important;
}

.el-option{
  color: #4DA4FF !important;
}

.el-select-dropdown__item.selected{
  color: rgb(248, 182, 0) !important;
}

#b4{
  border: 1px solid #09927b !important;
}
#b5{
  color: rgb(248, 182, 0) !important;
  border: 1px solid #09927b !important;
}
#b6{
  border: 1px solid #09927b !important;
}
.datasbase_title{
  display: block;
  color: white;
  font-size: 80%;
  text-align: center !important;
  margin-bottom: 1%;
}
.el-upload__tip{
  color: white !important;
  font-size: 60% !important;
}
.upload-demo{
  margin-left: 46% !important;
}
.datatemplate{
  font-size: 80%;
  margin-left: -65%;
  color: yellow;
}
.dataupload{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;;
}
.dataupload_2{
  background-color: rgb(248, 182, 0) !important;
  border-color: rgb(248, 182, 0) !important;;
  margin-left: -70% !important;
}
</style>
