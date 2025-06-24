<template>
  <div class="main-container">
    <!-- Three.js 场景 -->
    <div class="scene-container" ref="container"></div>

    <!-- 左上方容器：显示【第二段代码】中的面板内容 -->
    <div class="charts-wrapper-upleft">
      <div class="CoalData">
        <!-- 直接使用第二段代码中 .CoalData 的表单面板 -->
        <div class='selectbutton'>
          <p></p>
          <!-- <el-button id='b12' class='button_2' size="mini" @click='switchAIComparison'>预测性能对比</el-button> -->
        </div>

        <el-card  class="box-card_6"  shadow="never"  :body-style="{ backgroundColor: 'transparent', border: 'none' }">
          <el-form>
            <el-row>
              ㅤ<h3 class="ai-algorithm-title">AI配煤算法</h3>
            </el-row>
            <el-row>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_1"
                  type="primary"
                  @click="selectQicoal"
                >气煤选择</el-button>
              </el-col>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_1"
                  type="primary"
                  @click="deleteQicoal"
                >清空选择</el-button>
              </el-col>
              <el-col :span="1">ㅤ</el-col>
              <el-col :span="15">
                <el-form-item
                  style="font-weight:bold"
                  class="type_label_1"
                  :model="modifyParametersForm"
                >
                  选择的气煤煤样：
                  <span
                    style="font-weight:bold"
                    v-for="(item) in modifyParametersForm.params"
                    :key="item.key"
                    class="selectedCoal"
                  >
                    ㅤ{{ item.paramName }}
                  </span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_2"
                  type="primary"
                  @click="selectFeicoal"
                >肥煤选择</el-button>
              </el-col>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_2"
                  type="primary"
                  @click="deleteFeicoal"
                >清空选择</el-button>
              </el-col>
              <el-col :span="1">ㅤ</el-col>
              <el-col :span="15">
                <el-form-item
                  style="font-weight:bold"
                  class="type_label_1"
                  :model="modifyParametersForm_2"
                >
                  选择的肥煤煤样：
                  <span
                    style="font-weight:bold"
                    v-for="(item) in modifyParametersForm_2.params"
                    :key="item.key"
                    class="selectedCoal_2"
                  >
                    ㅤ{{ item.paramName }}
                  </span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_3"
                  type="primary"
                  @click="selectQiFeicoal"
                >气肥煤选择</el-button>
              </el-col>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_3"
                  type="primary"
                  @click="deleteQiFeicoal"
                >清空选择</el-button>
              </el-col>
              <el-col :span="1">ㅤ</el-col>
              <el-col :span="15">
                <el-form-item
                  style="font-weight:bold"
                  class="type_label_1"
                  :model="modifyParametersForm_3"
                >
                  选择的气肥煤煤样:
                  <span
                    style="font-weight:bold"
                    v-for="(item) in modifyParametersForm_3.params"
                    :key="item.key"
                    class="selectedCoal_3"
                  >
                    ㅤ{{ item.paramName }}
                  </span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_4"
                  type="primary"
                  @click="select13jiaocoal"
                >1/3焦煤选择</el-button>
              </el-col>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_4"
                  type="primary"
                  @click="delete13jiaocoal"
                >清空选择</el-button>
              </el-col>
              <el-col :span="1">ㅤ</el-col>
              <el-col :span="15">
                <el-form-item
                  style="font-weight:bold"
                  class="type_label_1"
                  :model="modifyParametersForm_4"
                >
                  选择的1/3焦煤煤样:
                  <span
                    style="font-weight:bold"
                    v-for="(item) in modifyParametersForm_4.params"
                    :key="item.key"
                    class="selectedCoal_4"
                  >
                    ㅤ{{ item.paramName }}
                  </span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_5"
                  type="primary"
                  @click="selectjiaocoal"
                >焦煤选择</el-button>
              </el-col>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_5"
                  type="primary"
                  @click="deletetjiaocoal"
                >清空选择</el-button>
              </el-col>
              <el-col :span="1">ㅤ</el-col>
              <el-col :span="15">
                <el-form-item
                  style="font-weight:bold"
                  class="type_label_1"
                  :model="modifyParametersForm_5"
                >
                  选择的焦煤煤样:
                  <span
                    style="font-weight:bold"
                    v-for="(item) in modifyParametersForm_5.params"
                    :key="item.key"
                    class="selectedCoal_5"
                  >
                    ㅤ{{ item.paramName }}
                  </span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_6"
                  type="primary"
                  @click="selectshoucoal"
                >瘦煤选择</el-button>
              </el-col>
              <el-col :span="3">
                <el-button
                  class="BlendingTypebutton_6"
                  type="primary"
                  @click="deletetshoucoal"
                >清空选择</el-button>
              </el-col>
              <el-col :span="1">ㅤ</el-col>
              <el-col :span="15">
                <el-form-item
                  style="font-weight:bold"
                  class="type_label_1"
                  :model="modifyParametersForm_6"
                >
                  选择的瘦煤煤样:
                  <span
                    style="font-weight:bold"
                    v-for="(item) in modifyParametersForm_6.params"
                    :key="item.key"
                    class="selectedCoal_6"
                  >
                    ㅤ{{ item.paramName }}
                  </span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <p>
                ㅤ
                <el-button class='Blendingbutton_5' type="primary" @click="MakingDecision">
                  配煤决策
                </el-button>
              </p>
            </el-row>
          </el-form>
        </el-card>
      </div>
    </div>

    <!-- 左下方：三列容器 (保留原先三环形图) -->
    <div class="charts-wrapper-downleft">
      <h3 class="section-title">预测结果</h3>
      <div class="chart-container" ref="chart4"></div>
      <div class="chart-container" ref="chart5"></div>
      <div class="chart-container" ref="chart6"></div>
    </div>

    <!-- 右侧图表容器 (保留原先) -->
    <div class="charts-wrapper">
      <!-- chart1 区域 -->
      <div class="chart-container">
        <div class="info-block">
          <h3>输料工况</h3>
          <p>螺旋送料机：<span>运行</span></p>
          <p>称量料斗1质量：<span>500 g</span></p>
          <p>称量料斗2质量：<span>500 g</span></p>
          <p>称量料斗3质量：<span>500 g</span></p>
        </div>
      </div>

      <!-- chart2 区域 -->
      <div class="chart-container">
        <div class="info-block">
          <h3>搅拌工况</h3>
          <p>搅拌机转速：<span>20 转/分</span></p>
          <p>搅拌机运行时间：<span>5 分</span></p>
        </div>
      </div>

      <!-- chart3 区域 -->
      <div class="chart-container">
        <div class="info-block">
          <h3>捣固工况</h3>
          <p>当前压力：<span>10 Mpa</span></p>
          <p>当前位移：<span>45 mm</span></p>
          <p>超声波测量高度：<span>235 mm</span></p>
          <p>估算堆密度：<span>1.25 g/cm³</span></p>
          <p>当前捣固次数：<span>3/10</span></p>
        </div>
      </div>

      <!-- 工业相机画面部分 -->
      <div class="chart-container">
        <!-- 加载提示文本 -->
        <div v-if="loading" class="loading-message">
          <p>网络相机画面正在加载中，请等待...</p>
        </div>

        <!-- 使用 <video> 标签显示网络相机的实时画面 -->
        <video
          v-else
          src="你的网络摄像头视频流地址"
          autoplay
          style="width: 100%; height: 100%; object-fit: cover;"
        />
      </div>
    </div>

    <!-- 以下是「第二段代码」里各种 Dialog，对话框直接放在根容器里即可 -->
    <!-- 气煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog1"
      top="2vh"
      title="气煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible1"
      :append-to-body="true"
      width="75%"
      height="50%"
    >
      <pl-table
        @selection-change="handleSelectionChange"
        id="CoalTable"
        :data="coalList"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ qiCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 肥煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog2"
      top="7vh"
      title="肥煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible2"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_2"
        id="CoalTable"
        :data="coalList_2"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ feiCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_2">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 气肥煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog3"
      top="7vh"
      title="气肥煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible3"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_3"
        id="CoalTable"
        :data="coalList_3"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ qifeiCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_3">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 1/3焦煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog4"
      top="7vh"
      title="1/3焦煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible4"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_4"
        id="CoalTable"
        :data="coalList_4"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ jiao13Coalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_4">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 焦煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog5"
      top="7vh"
      title="焦煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible5"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_5"
        id="CoalTable"
        :data="coalList_5"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ jiaoCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_5">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 瘦煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog6"
      top="7vh"
      title="瘦煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible6"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_6"
        id="CoalTable"
        :data="coalList_6"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ souCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_6">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 配煤辅助决策(人工智能算法) - 综合选择后的弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog"
      top="7vh"
      title="配煤辅助决策(人工智能算法)"
      custom-class="userDig"
      center
      :show-close="false"
      :close-on-press-escape="false"
      :close-on-click-modal="false"
      :visible.sync="editCoalDetailVisible"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <el-form :model="modifyParametersForm_total">
        <el-row
          v-for="(item, index) in modifyParametersForm_total.params"
          :key="item.key"
        >
          <el-col :span="6">
            <el-form-item :label="`煤样名称：`">
              <span style="font-weight:bold">{{ item.paramName }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item :label="`煤种类型：`">
              <span style="font-weight:bold">{{ item.paramType }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item :label="`价格：`">
              <span style="font-weight:bold">{{ item.paramPrice }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            配煤比：
            <el-input
              style="font-weight:bold; width:70px"
              v-model="coalRatio[index]"
            />
            %
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="5">总配煤比：{{ totalRatio }} %</el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button class="Blendingbutton_2" type="primary" @click="predictBlendCoal">
          混合煤性质预测
        </el-button>
        <el-button class="Blendingbutton_2" type="primary" @click="predictBestRatio">
          最优配煤比预测
        </el-button>
        <el-button class="Blendingbutton_2" type="primary" @click="cancelDialog">
          取消
        </el-button>
      </span>
    </el-dialog>

    <!-- 混合煤性质预测结果弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog"
      top="7vh"
      title="混合煤性质预测结果"
      custom-class="userDig"
      center
      :show-close="true"
      :close-on-press-escape="true"
      :close-on-click-modal="true"
      :visible.sync="editBlendCoalVisible"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        :data-changes-scroll-top="false"
        ref="CoalTable"
        big-data-checkbox
        highlight-current-row
        :row-height="33"
        :data="blendCoalProperty"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column align="center" label="混合煤性质" key="21">
          <pl-table-column align="center" label="水分" prop="blendCoal_mad" />
          <pl-table-column align="center" label="灰分" prop="blendCoal_ad" />
          <pl-table-column align="center" label="挥发分" prop="blendCoal_vdaf" />
          <pl-table-column align="center" label="粘结指数G" prop="blendCoal_G" />
          <pl-table-column align="center" label="X" prop="blendCoal_X" />
          <pl-table-column align="center" label="Y" prop="blendCoal_Y" />
        </pl-table-column>
      </pl-table>
      <span slot="footer" class="dialog-footer">
        <el-button class="Blendingbutton_2" type="primary">
          上传至数据库
        </el-button>
        <el-button
          class="Blendingbutton_2"
          type="primary"
          @click="editBlendCoalVisible = false"
        >
          取消
        </el-button>
      </span>
    </el-dialog>

    <!-- 最优配煤比预测弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog"
      top="7vh"
      title="最优配煤比预测"
      custom-class="userDig"
      center
      :show-close="true"
      :close-on-press-escape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <el-form>
        <!-- 优化目标：成本价格 -->
        <el-row>
          <el-col :span="24">
            <el-form-item label="优化目标" style="font-weight:bold;">
              <span style="font-weight:normal">成本价格</span>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 限制条件 -->
        <el-row>
          <el-col :span="24">
            <span style="font-weight:bold">限制条件</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="10">
            <!-- CRI 范围 -->
            目标CRI范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[0]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[1]" />
          </el-col>
          <el-col :span="10">
            <!-- CSR 范围 -->
            目标CSR范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[2]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[3]" />
          </el-col>
        </el-row>
        <p style="margin: 10px 0;"></p>
        <el-row>
          <el-col :span="10">
            <!-- M10 范围 -->
            目标M10范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[4]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[5]" />
          </el-col>
          <el-col :span="10">
            <!-- M25 范围 -->
            目标M25范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[6]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[7]" />
          </el-col>
        </el-row>

        <!-- 预测结果 -->
        <el-row>
          <el-col :span="24">
            <p style="font-weight:bold">预测结果</p>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <span>最优成本价格：{{ returnPrice }} 元</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <span>最优配煤比：{{ returnRatio }}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24" style="font-size:80%;">
            <span>*最优配煤比预测采用的算法包含焦炭质量预测算法与遗传算法，结果仅供参考</span>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button class="Blendingbutton_2" type="primary" @click="predictRatio">
          开始预测
        </el-button>
        <el-button class="Blendingbutton_2" type="primary" @click="editRatioCoalVisible = false">
          取消
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
/**
 * 合并了第一段代码（Three.js & ECharts）和第二段代码（左上角面板 + 配煤逻辑）
 * 注意：
 *  - 若项目中无需某些功能，可自行删除对应部分
 *  - 若项目需 OrbitControls、DRACOLoader 等，可自行按需整合
 */
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import * as echarts from 'echarts'

// 这里是第一段代码中的模型与纹理
import coalPilesUrl from '../../assets/models/coalPiles.glb'
import gridTextureUrl from '../../assets/textures/grid4.jpg'

// 如果需要 DRACOLoader、OrbitControls，可自行 import 并使用
// import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

export default {
  name: 'CoalPilesStaticWithLabels',
  // 如果需要在 created 阶段去后端拉取数据，可在此进行
  created() {
    // 下列为“第二段代码”里根据不同煤种拉取数据的示例
    this.getCoalList()
    this.getCoalList_2()
    this.getCoalList_3()
    this.getCoalList_4()
    this.getCoalList_5()
    this.getCoalList_6()
    // 用于表格高度的示例
    this.height =
      window.screen.height > 850
        ? window.screen.height * 0.62
        : window.screen.height * 0.481
  },
  data() {
    return {
      loading: true,
      // ---------------- 第一段代码中的数据 ----------------
      scene: null,
      camera: null,
      renderer: null,
      // ECharts 实例
      chart4: null,
      chart5: null,
      chart6: null,
      chart1: null,
      chart2: null,
      chart3: null,

      // 两个示例表单(最初示例只有气煤和肥煤)，后面新增多种煤
      modifyParametersForm: { params: [] }, // 选中的气煤
      modifyParametersForm_2: { params: [] }, // 选中的肥煤

      // ---------------- 第二段代码新增的更多表单 ----------------
      modifyParametersForm_3: { params: [] }, // 选中的气肥煤
      modifyParametersForm_4: { params: [] }, // 1/3焦煤
      modifyParametersForm_5: { params: [] }, // 焦煤
      modifyParametersForm_6: { params: [] }, // 瘦煤
      modifyParametersForm_total: { params: [] },

      // 下列为“第二段代码”中的数据：
      coalList: [],
      coalList_2: [],
      coalList_3: [],
      coalList_4: [],
      coalList_5: [],
      coalList_6: [],

      multipleSelectionData: [],
      multipleSelectionData_2: [],
      multipleSelectionData_3: [],
      multipleSelectionData_4: [],
      multipleSelectionData_5: [],
      multipleSelectionData_6: [],

      // 控制弹窗显示/隐藏
      editRatioCoalVisible1: false,
      editRatioCoalVisible2: false,
      editRatioCoalVisible3: false,
      editRatioCoalVisible4: false,
      editRatioCoalVisible5: false,
      editRatioCoalVisible6: false,
      editCoalDetailVisible: false, // “配煤辅助决策”对话框
      editBlendCoalVisible: false, // “混合煤性质预测结果”对话框
      editRatioCoalVisible: false, // “最优配煤比推荐”对话框

      // 一些提示用变量
      qiCoalattention: '',
      feiCoalattention: '',
      qifeiCoalattention: '',
      jiao13Coalattention: '',
      jiaoCoalattention: '',
      souCoalattention: '',

      // 配煤相关
      coalRatio: [], // 存储煤比例
      totalRatio: 0,
      blendCoalProperty: [],
      preparedTotalResult: [], // 发送给后端的已选煤数据
      preparedDataforRatio: [], // 发送给后端的煤比例(最优配煤比推荐)
      returnRatio: '',
      returnPrice: '',
      newRatio: [],
      returnTotalRatio: 0,
      max: 0,
      paraRange: [],

      // 其余
      lastUpdateTime: 0,
      updateInterval: 5000,

      // 表格高度示例
      height: 600
    }
  },
  mounted() {
    // =========== 第一段代码中的 3D 初始化 + ECharts =============
    this.initScene()
    this.loadModel()
    this.initCharts()
    this.animate()
    this.loadCameraStream()
    window.addEventListener('resize', this.onWindowResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.onWindowResize)
    if (this.animationFrameId) cancelAnimationFrame(this.animationFrameId)
    if (this.renderer) this.renderer.dispose()

    // 释放 ECharts 实例
    if (this.chart4) this.chart4.dispose()
    if (this.chart5) this.chart5.dispose()
    if (this.chart6) this.chart6.dispose()
    if (this.chart1) this.chart1.dispose()
    if (this.chart2) this.chart2.dispose()
    if (this.chart3) this.chart3.dispose()
  },
  methods: {
    loadCameraStream() {
      // 模拟网络摄像头流的加载过程
      setTimeout(() => {
        this.loading = false // 加载完成，隐藏加载提示，显示视频流
      }, 5000) // 假设加载时间为 5 秒，你可以根据实际情况调整
    },
    /* ------------------------ 第一段代码中的方法（3D + ECharts） ------------------------ */
    initScene() {
      const container = this.$refs.container
      this.scene = new THREE.Scene()

      const textureLoader = new THREE.TextureLoader()
      textureLoader.load(
        gridTextureUrl,
        (texture) => {
          texture.wrapS = THREE.RepeatWrapping
          texture.wrapT = THREE.RepeatWrapping
          texture.repeat.set(1, 1)
          this.scene.background = texture
        },
        undefined,
        (err) => {
          console.error('加载背景纹理时出错:', err)
          this.scene.background = new THREE.Color(0x888888)
        }
      )

      this.camera = new THREE.PerspectiveCamera(
        60,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
      )
      // 可自行调整相机位置
      this.camera.position.set(18, 0, 0)
      this.camera.lookAt(0, 10, -4)

      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
      this.renderer.setSize(container.clientWidth, container.clientHeight)
      container.appendChild(this.renderer.domElement)

      this.renderer.outputEncoding = THREE.sRGBEncoding
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping
      this.renderer.toneMappingExposure = 1.0
    },
    loadModel() {
      const loader = new GLTFLoader()
      loader.load(
        coalPilesUrl,
        (gltf) => {
          const model = gltf.scene
          this.scene.add(model)
        },
        (xhr) => {
          console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
        },
        (err) => {
          console.error('加载煤堆模型时出错:', err)
        }
      )
    },
    animate() {
      this.animationFrameId = requestAnimationFrame(this.animate)
      this.renderer.render(this.scene, this.camera)
    },
    initCharts() {
      this.chart4 = echarts.init(this.$refs.chart4)
      this.chart4.setOption(this.getRingOption(0, '#ff6666', '煤种1'))

      this.chart5 = echarts.init(this.$refs.chart5)
      this.chart5.setOption(this.getRingOption(0, '#ffcc00', '煤种2'))

      this.chart6 = echarts.init(this.$refs.chart6)
      this.chart6.setOption(this.getRingOption(0, '#66ff66', '煤种3'))
    },
    getRingOption(value, color, title) {
      const remain = 100 - value
      return {
        backgroundColor: 'transparent',
        series: [
          {
            name: title,
            type: 'pie',
            center: ['50%', '50%'],
            radius: ['50%', '60%'],
            label: { show: false },
            labelLine: { show: false },
            data: [
              { value, itemStyle: { color } },
              { value: remain, itemStyle: { color: '#555555' } }
            ]
          }
        ],
        graphic: [
          {
            type: 'text',
            left: '50%',
            top: '40%',
            style: {
              text: `${value}%`,
              fill: color,
              font: 'bold 24px sans-serif',
              textAlign: 'center'
            }
          },
          {
            type: 'text',
            left: '50%',
            top: '60%',
            style: {
              text: title,
              fill: color,
              font: '20px sans-serif',
              textAlign: 'center'
            }
          }
        ]
      }
    },
    onWindowResize() {
      const container = this.$refs.container
      if (!container) return
      this.camera.aspect = container.clientWidth / container.clientHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(container.clientWidth, container.clientHeight)

      if (this.chart4) this.chart4.resize()
      if (this.chart5) this.chart5.resize()
      if (this.chart6) this.chart6.resize()
      if (this.chart1) this.chart1.resize()
      if (this.chart2) this.chart2.resize()
      if (this.chart3) this.chart3.resize()
    },

    /* ---------------------- 下面是“第二段代码”中的业务逻辑方法 ---------------------- */
    // 向后端拉取数据
    async getCoalList() {
      // 示例： this.$http.get('getQiCoal') ...
      // 下面用伪代码或示例结构
      // 根据实际接口返回的数据结构修改
      try {
        const ret = await this.$http.get('getQiCoal')
        this.coalList = ret.data.msg
        this.coalList.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_2() {
      try {
        const ret = await this.$http.get('getFeiCoal')
        this.coalList_2 = ret.data.msg
        this.coalList_2.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_3() {
      try {
        const ret = await this.$http.get('getQiFeiCoal')
        this.coalList_3 = ret.data.msg
        this.coalList_3.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_4() {
      try {
        const ret = await this.$http.get('get31JiaoCoal')
        this.coalList_4 = ret.data.msg
        this.coalList_4.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_5() {
      try {
        const ret = await this.$http.get('getJiaoCoal')
        this.coalList_5 = ret.data.msg
        this.coalList_5.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_6() {
      try {
        const ret = await this.$http.get('getShouCoal')
        this.coalList_6 = ret.data.msg
        this.coalList_6.reverse()
      } catch (error) {
        console.error(error)
      }
    },

    // pl-table 多选
    handleSelectionChange(val) {
      this.multipleSelectionData = val
    },
    handleSelectionChange_2(val) {
      this.multipleSelectionData_2 = val
    },
    handleSelectionChange_3(val) {
      this.multipleSelectionData_3 = val
    },
    handleSelectionChange_4(val) {
      this.multipleSelectionData_4 = val
    },
    handleSelectionChange_5(val) {
      this.multipleSelectionData_5 = val
    },
    handleSelectionChange_6(val) {
      this.multipleSelectionData_6 = val
    },

    // 选择/清空气煤
    selectQicoal() {
      this.editRatioCoalVisible1 = true
      this.qiCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList.length; i++) {
        if (this.coalList[i].store_number < 50) {
          k += 1
          this.qiCoalattention += this.coalList[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.qiCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deleteQicoal() {
      this.multipleSelectionData = []
      this.modifyParametersForm = { params: [] }
    },

    // 选择/清空肥煤
    selectFeicoal() {
      this.editRatioCoalVisible2 = true
      this.feiCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_2.length; i++) {
        if (this.coalList_2[i].store_number < 50) {
          k += 1
          this.feiCoalattention += this.coalList_2[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.feiCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deleteFeicoal() {
      this.multipleSelectionData_2 = []
      this.modifyParametersForm_2 = { params: [] }
    },

    // 选择/清空气肥煤
    selectQiFeicoal() {
      this.editRatioCoalVisible3 = true
      this.qifeiCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_3.length; i++) {
        if (this.coalList_3[i].store_number < 50) {
          k += 1
          this.qifeiCoalattention += this.coalList_3[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.qifeiCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deleteQiFeicoal() {
      this.multipleSelectionData_3 = []
      this.modifyParametersForm_3 = { params: [] }
    },

    // 选择/清空1/3焦煤
    select13jiaocoal() {
      this.editRatioCoalVisible4 = true
      this.jiao13Coalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_4.length; i++) {
        if (
          this.coalList_4[i].store_number < 50 &&
          this.coalList_4[i].store_number > 0
        ) {
          k += 1
          this.jiao13Coalattention += this.coalList_4[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.jiao13Coalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    delete13jiaocoal() {
      this.multipleSelectionData_4 = []
      this.modifyParametersForm_4 = { params: [] }
    },

    // 选择/清空焦煤
    selectjiaocoal() {
      this.editRatioCoalVisible5 = true
      this.jiaoCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_5.length; i++) {
        if (
          this.coalList_5[i].store_number < 50 &&
          this.coalList_5[i].store_number > 0
        ) {
          k += 1
          this.jiaoCoalattention += this.coalList_5[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.jiaoCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deletetjiaocoal() {
      this.multipleSelectionData_5 = []
      this.modifyParametersForm_5 = { params: [] }
    },

    // 选择/清空瘦煤
    selectshoucoal() {
      this.editRatioCoalVisible6 = true
      this.souCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_6.length; i++) {
        if (
          this.coalList_6[i].store_number < 50 &&
          this.coalList_6[i].store_number > 0
        ) {
          k += 1
          this.souCoalattention += this.coalList_6[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.souCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deletetshoucoal() {
      this.multipleSelectionData_6 = []
      this.modifyParametersForm_6 = { params: [] }
    },

    // 确认选择 => 将多选的煤保存到对应 form 中
    sendBlendingData() {
      this.modifyParametersForm = { params: [] }
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.modifyParametersForm.params.push({
          paramName: this.multipleSelectionData[i].coal_name,
          paramType: this.multipleSelectionData[i].coal_type,
          paramPrice: this.multipleSelectionData[i].coal_price
        })
      }
      this.editRatioCoalVisible1 = false
    },
    sendBlendingData_2() {
      this.modifyParametersForm_2 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_2.length; i++) {
        this.modifyParametersForm_2.params.push({
          paramName: this.multipleSelectionData_2[i].coal_name,
          paramType: this.multipleSelectionData_2[i].coal_type,
          paramPrice: this.multipleSelectionData_2[i].coal_price
        })
      }
      this.editRatioCoalVisible2 = false
    },
    sendBlendingData_3() {
      this.modifyParametersForm_3 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_3.length; i++) {
        this.modifyParametersForm_3.params.push({
          paramName: this.multipleSelectionData_3[i].coal_name,
          paramType: this.multipleSelectionData_3[i].coal_type,
          paramPrice: this.multipleSelectionData_3[i].coal_price
        })
      }
      this.editRatioCoalVisible3 = false
    },
    sendBlendingData_4() {
      this.modifyParametersForm_4 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_4.length; i++) {
        this.modifyParametersForm_4.params.push({
          paramName: this.multipleSelectionData_4[i].coal_name,
          paramType: this.multipleSelectionData_4[i].coal_type,
          paramPrice: this.multipleSelectionData_4[i].coal_price
        })
      }
      this.editRatioCoalVisible4 = false
    },
    sendBlendingData_5() {
      this.modifyParametersForm_5 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_5.length; i++) {
        this.modifyParametersForm_5.params.push({
          paramName: this.multipleSelectionData_5[i].coal_name,
          paramType: this.multipleSelectionData_5[i].coal_type,
          paramPrice: this.multipleSelectionData_5[i].coal_price
        })
      }
      this.editRatioCoalVisible5 = false
    },
    sendBlendingData_6() {
      this.modifyParametersForm_6 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_6.length; i++) {
        this.modifyParametersForm_6.params.push({
          paramName: this.multipleSelectionData_6[i].coal_name,
          paramType: this.multipleSelectionData_6[i].coal_type,
          paramPrice: this.multipleSelectionData_6[i].coal_price
        })
      }
      this.editRatioCoalVisible6 = false
    },

    // “配煤决策”按钮 => 打开对话框，收集所有煤种
    MakingDecision() {
      this.modifyParametersForm_total = { params: [] }
      // 将 6 类煤的多选结果合并
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData[i].coal_name,
          paramType: this.multipleSelectionData[i].coal_type,
          paramPrice: this.multipleSelectionData[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_2.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_2[i].coal_name,
          paramType: this.multipleSelectionData_2[i].coal_type,
          paramPrice: this.multipleSelectionData_2[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_3.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_3[i].coal_name,
          paramType: this.multipleSelectionData_3[i].coal_type,
          paramPrice: this.multipleSelectionData_3[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_4.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_4[i].coal_name,
          paramType: this.multipleSelectionData_4[i].coal_type,
          paramPrice: this.multipleSelectionData_4[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_5.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_5[i].coal_name,
          paramType: this.multipleSelectionData_5[i].coal_type,
          paramPrice: this.multipleSelectionData_5[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_6.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_6[i].coal_name,
          paramType: this.multipleSelectionData_6[i].coal_type,
          paramPrice: this.multipleSelectionData_6[i].coal_price
        })
      }
      // 打开配煤决策对话框
      this.editCoalDetailVisible = true
    },
    cancelDialog() {
      this.editCoalDetailVisible = false
      this.coalRatio = []
      this.totalRatio = 0
    },

    // 混合煤性质预测
    async predictBlendCoal() {
      this.totalRatio = 0
      if (this.coalRatio.length === 0) {
        this.$confirm('配煤比例总和须为100%', '提示', {
          confirmButtonText: '确定',
          type: 'warning',
          showCancelButton: false
        })
        return
      }
      // 计算用户输入的总配比
      for (let j = 0; j < this.coalRatio.length; j++) {
        this.totalRatio += Number(this.coalRatio[j])
      }
      if (this.totalRatio !== 100) {
        this.$confirm('配煤比例总和须为100%', '提示', {
          confirmButtonText: '确定',
          type: 'warning',
          showCancelButton: false
        })
        return
      }
      // 真正请求后端预测
      this.editBlendCoalVisible = true
      // 准备数据
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.preparedTotalResult.push({
          id: this.multipleSelectionData[i].id,
          coalRatio: this.coalRatio[i],
          coal_mad: this.multipleSelectionData[i].coal_mad,
          coal_ad: this.multipleSelectionData[i].coal_ad,
          coal_vdaf: this.multipleSelectionData[i].coal_vdaf,
          coal_std: this.multipleSelectionData[i].coal_std,
          G: this.multipleSelectionData[i].G,
          X: this.multipleSelectionData[i].X,
          Y: this.multipleSelectionData[i].Y
        })
      }
      // 依次把多选2~6里的也 push 进 preparedTotalResult，记得注意索引位置
      // 下方仅示例做法，需根据实际情况再行校正
      let offset = this.multipleSelectionData.length
      for (let i = 0; i < this.multipleSelectionData_2.length; i++) {
        this.preparedTotalResult.push({
          id: this.multipleSelectionData_2[i].id,
          coalRatio: this.coalRatio[offset + i],
          coal_mad: this.multipleSelectionData_2[i].coal_mad,
          coal_ad: this.multipleSelectionData_2[i].coal_ad,
          coal_vdaf: this.multipleSelectionData_2[i].coal_vdaf,
          coal_std: this.multipleSelectionData_2[i].coal_std,
          G: this.multipleSelectionData_2[i].G,
          X: this.multipleSelectionData_2[i].X,
          Y: this.multipleSelectionData_2[i].Y
        })
      }
      offset += this.multipleSelectionData_2.length
      for (let i = 0; i < this.multipleSelectionData_3.length; i++) {
        this.preparedTotalResult.push({
          id: this.multipleSelectionData_3[i].id,
          coalRatio: this.coalRatio[offset + i],
          coal_mad: this.multipleSelectionData_3[i].coal_mad,
          coal_ad: this.multipleSelectionData_3[i].coal_ad,
          coal_vdaf: this.multipleSelectionData_3[i].coal_vdaf,
          coal_std: this.multipleSelectionData_3[i].coal_std,
          G: this.multipleSelectionData_3[i].G,
          X: this.multipleSelectionData_3[i].X,
          Y: this.multipleSelectionData_3[i].Y
        })
      }
      offset += this.multipleSelectionData_3.length
      // 依次下去 ...
      // 这里示例省略，合并完后：
      // 发请求
      try {
        const res = await this.$http.post('predictBlendCoalQuality', this.preparedTotalResult)
        // 后端返回混合煤性质
        this.blendCoalProperty = res.data
      } catch (error) {
        console.error(error)
      }
      // 清空
      this.preparedTotalResult = []
    },

    // 最优配煤比预测
    predictBestRatio() {
      this.editRatioCoalVisible = true
    },

    // 在最优配煤比对话框中点击“开始预测”
    /* async predictRatio() {
      // 准备数据
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.preparedDataforRatio.push({
          coal_price: this.multipleSelectionData[i].coal_price,
          coke_CSR: this.multipleSelectionData[i].coke_CSR,
          coke_CRI: this.multipleSelectionData[i].coke_CRI,
          coke_M10: this.multipleSelectionData[i].coke_M10,
          coke_M25: this.multipleSelectionData[i].coke_M25
        })
      }
      // 类似地把 multipleSelectionData_2 ~ _6 也 push 进去
      // ...
      // 把用户输入的 paraRange 也放进去
      this.preparedDataforRatio.push(this.paraRange)

      try {
        const res = await this.$http.post('predictBestRatio', this.preparedDataforRatio)
        if (res.data[0] === 'NoPrice') {
          this.$confirm('选择的煤样中缺少价格参数', '提示', {
            confirmButtonText: '确定',
            type: 'warning',
            showCancelButton: false
          })
        } else if (res.data[0] === 'Error') {
          this.$confirm('未能从设定范围空间中寻找到最优配煤比，请重新设置或扩大参数范围', '提示', {
            confirmButtonText: '确定',
            type: 'warning',
            showCancelButton: false
          })
        } else {
          this.returnPrice = res.data['1'][0][0].toFixed(2)
          this.returnRatio = ''
          this.newRatio = []
          // 同时修正比例之和为100
          this.returnTotalRatio = 0
          this.max = res.data['0'][0][0]
          const arr = res.data['0'][0]
          for (let i = 0; i < arr.length; i++) {
            this.returnTotalRatio += arr[i] * 100
          }
          // 找到最大值下标，把多余或不足分配到此
          let idxMax = 0
          let valMax = arr[0]
          for (let i = 1; i < arr.length; i++) {
            if (arr[i] > valMax) {
              valMax = arr[i]
              idxMax = i
            }
          }
          if (this.returnTotalRatio < 100) {
            arr[idxMax] += (100 - this.returnTotalRatio) / 100
          } else if (this.returnTotalRatio > 100) {
            arr[idxMax] -= (this.returnTotalRatio - 100) / 100
          }
          // 生成最终显示
          for (let i = 0; i < arr.length; i++) {
            this.returnRatio += (arr[i] * 100).toFixed(2) + '%\xa0\xa0\xa0\xa0'
            this.newRatio.push((arr[i] * 100).toFixed(2))
          }
          // 覆盖到 coalRatio
          this.coalRatio = this.newRatio
        }
      } catch (error) {
        console.error(error)
      } finally {
        this.preparedDataforRatio = []
      }
    } */
    async predictRatio() {
      const arr = [0.41, 0.45, 0.14] // 比例
      this.returnPrice = 843.27 // 假装返回的价格
      this.returnRatio = '' // 用来拼接显示的文本
      this.newRatio = []

      let total = 0
      for (let i = 0; i < arr.length; i++) {
        total += arr[i] * 100
      }
      if (total === 100) {
        for (let i = 0; i < arr.length; i++) {
          // 把数值拼接成百分比字符串
          this.returnRatio += (arr[i] * 100).toFixed(2) + '%\xa0\xa0\xa0\xa0'
          this.newRatio.push((arr[i] * 100).toFixed(2))
        }
        // 覆盖到 coalRatio
        this.coalRatio = this.newRatio
        // 接下来，更新 3 个环形图：
        this.chart4.setOption(this.getRingOption(Number(this.newRatio[0]), '#ff6666', '兴义'))
        this.chart5.setOption(this.getRingOption(Number(this.newRatio[1]), '#ffcc00', '霍州'))
        this.chart6.setOption(this.getRingOption(Number(this.newRatio[2]), '#66ff66', '陆良'))
      }

      // 清空请求参数
      this.preparedDataforRatio = []
    }
  }
}
</script>

<style scoped>
/* 根容器 */
.main-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* Three.js 场景 */
.scene-container {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}

/* 右侧图表容器 */
.charts-wrapper {
  position: absolute;
  top: 2%;
  right: 20px;
  width: 400px;
  height: 95%;
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

/* 左上方容器 */
.charts-wrapper-upleft {
  position: absolute;
  top: 2%;
  left: 20px;
  width: 65%;
  height: 47%;
  z-index: 10;
  display: flex;
  flex-direction: row;
  gap: 20px;
  background: transparent !important;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5),
    0 0 30px rgba(0, 255, 255, 0.3);
  overflow: hidden;
}

/* 下方左侧：三列容器 */
.charts-wrapper-downleft {
  position: absolute;
  top: 53%;
  left: 20px;
  width: 65%;
  height: 44%;
  display: flex;
  flex-direction: row;
  gap: 20px;
  z-index: 10;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5),
    0 0 30px rgba(0, 255, 255, 0.3);
}

/* 通用图表容器 */
.chart-container {
  flex: 1;
  background-color: transparent;
  border-radius: 8px;
  box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2),
    0 0 10px rgba(0, 255, 255, 0.2);
  box-sizing: border-box;
  /* padding-right: 20px; <-- 可以改成 padding: 10px; 看情况 */
}

/* 整体文本框样式 */
.info-block {
  padding: 20px;
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(0, 204, 255, 0.3)); /* 渐变背景 */
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.2);
  transition: all 0.3s ease;
}

/* 信息行 */
.info-block p {
  color: #fff; /* 白色字体 */
  font-family: 'Orbitron', sans-serif; /* 使用科技感的字体 */
  font-size: 18px;
  margin: 15px 0;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.6), 0 0 16px rgba(0, 255, 255, 0.4); /* 发光效果 */
  letter-spacing: 0.5px; /* 增加字间距 */
}

/* 强调文本 (例如状态) */
.info-block span {
  font-weight: bold;
  font-size: 20px;
  color: #00ffcc; /* 亮绿色或者科技蓝 */
  text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1);
  animation: glow 1.5s infinite alternate;
}

/* 鼠标悬停时的效果 */
.info-block:hover {
  transform: scale(1.05);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.7), 0 0 60px rgba(0, 255, 255, 0.3);
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.5), rgba(0, 204, 255, 0.5)); /* 增强渐变效果 */
}

/* 增加小的动感效果 */
@keyframes glow {
  0% { text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1); }
  50% { text-shadow: 0 0 20px rgba(0, 255, 255, 1), 0 0 40px rgba(0, 255, 255, 1); }
  100% { text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1); }
}

/* 面板最外层 */
.CoalData {
  flex: 1; /* 若只放这一个元素，可让它撑满父容器 */
  background: transparent !important;
  border-radius: 8px;
  padding: 10px;
  color: #fff;
  overflow: auto;
}

/* 具体按钮和文字样式 */
.selectbutton {
  margin-bottom: 10px;
}
.BlendingTypebutton_1 {
  margin-bottom: 6px;
  background-color: rgb(106, 189, 120) !important;
  border-color: rgb(64, 174, 0) !important;
  width: 100px;
}
.BlendingTypebutton_2 {
  margin-bottom: 6px;
  background-color: rgb(0, 141, 86) !important;
  border-color: rgb(64, 174, 0) !important;
  width: 100px;
}
.BlendingTypebutton_3 {
  margin-bottom: 6px;
  background-color: rgb(21, 174, 103) !important;
  border-color: rgb(64, 174, 0) !important;
  width: 100px;
}
.BlendingTypebutton_4 {
  margin-bottom: 6px;
  background-color: rgb(20, 144, 126) !important;
  border-color: rgb(64, 174, 0) !important;
  width: 100px;
}
.BlendingTypebutton_5 {
  margin-bottom: 6px;
  background-color: rgb(0, 127, 119) !important;
  border-color: rgb(64, 174, 0) !important;
  width: 100px;
}
.BlendingTypebutton_6 {
  margin-bottom: 6px;
  background-color: rgb(66, 170, 145) !important;
  border-color: rgb(64, 174, 0) !important;
  width: 100px;
}

.type_label_1 {
  margin-top: 4px;
  color: white !important;
}
.selectedCoal {
  color: rgb(106, 189, 120) !important;
  margin-left: 6px;
}
.selectedCoal_2 {
  color: rgb(0, 141, 86) !important;
  margin-left: 6px;
}
.selectedCoal_3 {
  color: rgb(21, 174, 103) !important;
  margin-left: 6px;
}
.selectedCoal_4 {
  color: rgb(20, 144, 126) !important;
  margin-left: 6px;
}
.selectedCoal_5 {
  color: rgb(0, 127, 119) !important;
  margin-left: 6px;
}
.selectedCoal_6 {
  color: rgb(66, 170, 145) !important;
  margin-left: 6px;
}

/* 配煤按钮 */
.Blendingbutton_5 {
  float: right;
  margin-top: -5px !important;
  margin-bottom: 15px;
  background-color: rgb(64, 174, 0) !important;
  border-color: rgb(64, 174, 0) !important;
}

/* pl-table 的对话框一些样式示例 */
#abow_dialog1 #CoalTable td,
#abow_dialog1 #CoalTable th {
  border: 1px solid rgb(184, 184, 184) !important;
}
/* 依此类推，也可加全局 table 样式 */

/* 其它按钮 */
.Blendingbutton_3 {
  float: right;
  margin-top: 20px !important;
  margin-left: 500px !important;
  background-color: rgb(64, 174, 0) !important;
  border-color: rgb(64, 174, 0) !important;
}

/* 留一点空白的示例 */
.heightblank {
  height: 60px !important;
}

/* 提示文字颜色 */
.qiCoalattention {
  color: red !important;
}

/* 对话框底部按钮 */
.dialog-footer {
  text-align: right;
}

/* 其它小样式 */
.Blendingbutton_2 {
  background-color: rgb(64, 174, 0) !important;
  border-color: rgb(64, 174, 0) !important;
  margin-right: 10px;
}
/* 假设是全局样式（非 scoped）里 */
.box-card_6.el-card {
  background-color: transparent !important;
  box-shadow: none !important; /* 去掉卡片阴影 */
  border: none !important;
}
.box-card_6 .el-card__body {
  background-color: transparent !important;
}
.loading-message p {
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1);
}
.charts-wrapper h3 {
  font-weight: bold;
  color: white; /* 设置字体颜色为白色 */
  text-align: center; /* 居中 */
}
.ai-algorithm-title {
  font-size: 18px;  /* 设置字体大小 */
  font-weight: bold; /* 设置加粗 */
  color: white;  /* 设置文字颜色为白色 */
  margin: 10px 0;  /* 去除默认的上下间距 */
}
.section-title {
  text-align: center;  /* 居中对齐 */
  font-size: 24px;      /* 设置字体大小 */
  font-weight: bold;    /* 设置字体加粗 */
  color: white;         /* 设置文字颜色为白色 */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);  /* 设置阴影效果 */
  margin-bottom: 20px;  /* 添加下边距，使标题与下面的图表容器有些间距 */
}
</style>
