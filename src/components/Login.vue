<template>
    <div class='login_container'> <!-- 修改这里填充满登录背景区域 -->
        <div class="particles">
          <vue-particles class="login-bg" color="#dedede" :particlesNumber="150" shapeType="circle" clickMode="repulse" hoverMode="repulse"></vue-particles>
        </div>
        <div class='login_box'>
            <div class='logo'>
              <img src='../assets/Picture5.png' alt='Logo' width="11.3%">
              <!-- <img class='carbon_logo' src= '../assets/carbon.gif' alt='Logo' width="6%"> -->
            </div>
            <!--头像标题区域-->
            <!-- <div class='avatar_box'>MSRI智慧炼焦配煤辅助决策软件系统(MSRI-AIES)(学术版V1.0)</div> -->
            <div class='avatar_box'>智慧炼焦配煤辅助决策软件系统<br/>（AIES）V0.92</div>
            <!--登录表单区域,ref是表单的引用对象-->
            <el-form ref='loginFormRef' :model="loginForm" :rules='loginFormRules' label-width="0px" class='login_form'> <!--ref为引用的名称,:model绑定表单数据,rules绑定验证规则，为elementui自带的-->
                <!--用户名-->
                <el-form-item prop='username'> <!--prop是为了验证规则rules可以生效,对应下方的loginFormRules-->
                    <el-input v-model='loginForm.username' placeholder="请输入用户账号" prefix-icon="el-icon-user-solid"></el-input>
                </el-form-item>
                <!--密码-->
                <el-form-item prop='password'>
                    <el-input v-model='loginForm.password' placeholder="请输入用户密码" prefix-icon="el-icon-s-goods" show-password auto-complete="new-password"></el-input>
                </el-form-item>
                <!--按钮区域-->
                <el-form-item class='btns'>
                    <el-button class='lgbtn' type="primary" @click='login'>登录</el-button>
                    <el-button class='reset' type="info" @click="resetLoginForm">重置</el-button>
                </el-form-item>
            </el-form>
            <!-- <p class='contact'>技术维护：Yohann <br/> 联系方式：yuhang.qiu@monash.edu</p> -->
            <p class='copyright'>技术维护：Yohann <br/> 联系方式：yuhang.qiu@monash.edu<br/><br/>版权所有：苏州龙泰氢一能源科技有限公司<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      show_useragreement: true,
      // 这是登录表单的数据绑定对象
      loginForm: {
        username: '',
        password: ''
      },
      // 这是表单的验证规则对象
      loginFormRules: {
        // 验证用户名是否合法
        username: [
          { required: true, message: '请输入登录账号', trigger: 'blur' }, // trigger:blur为文本框失去焦点的时候触发这个行为
          { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
        ],
        // 验证密码是否合法
        password: [
          { required: true, message: '请输入登录密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 点击重置按钮，重置登录表单,resetFields为elementui内置方法
    resetLoginForm() {
      this.$refs.loginFormRef.resetFields()
    },
    login() {
      // valid为true说明预验证成功，满足输入要求，false则是预验证失败
      this.$refs.loginFormRef.validate(async valid => { // valid为验证的结果，布尔值，满足输入rules，则返回true，否则false
        sessionStorage.setItem('showUserAgreement', JSON.stringify(this.show_useragreement)) // seesion存储用户协议对话窗口
        if (!valid) return 0
        const res = await this.$http.post('login', this.loginForm) // 将loginForm（账号密码）直接上传至后端，返回的是Promise对象,可以用函数async和变量await进行简化，data：res代表把返回的data取名为res操作，教程里的login可以更改成自己端口号
        if (res.status !== 200 || res.data === 'fail') return this.$message.error('请输入正确的用户名或密码！') // 登录失败则直接返回message，代码不进行下一步
        this.$message.success('登录成功！') // 在element.js已挂载elementui的message模块，用于弹窗显示
        // 保存由服务器返回的token，已便于记录用户状态，保存到sessionStorage中，在网站打开期间生效
        window.sessionStorage.setItem('token', 'I have login')
        this.$router.push('/home_new') // 登录成功后调整到home主页
      })
    }
  }
}
</script>

<style lang="less"> //支持less语法格式，scoped设置让这个样式只在当前组件内生效
.login_container{
    position: relative; // 父元素relative，子元素修改为absolute，方便进行定位
    background-image: url('../assets/5ab4cf7cecaf9.png'); // 需要用url才可以索引到图像
    background-size: 100% 100%; // 该div中需要有元素才可以显示100%，否则父元素会被浮动
    background-repeat: no-repeat;
    height: 110%; // 必须要加，尺寸和父尺寸保持一致，否则下方会留白色空白
    // background-color:#367CBA ;
    // transform: translate(-50%,-50%);
    // left: 50%;
    // top: 50%;
    // width: 100%;
}

.login_box{
    width: 450px;
    height: 250px;
    background-color:rgba(0,0,0,0.15);
    border-radius: 10px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%); // 移动元素本身的50%，50%，left，top50%之后，再加transform可以得到div居中

    .avatar_box{
        width: 800px;
        color: #ffffff;
        font-family: '微软雅黑';
        font-size: 320%;
        text-align: center;
        transform: translate(-23%,-160%);
        // position: absolute;
        // left: 55%;
        // height: 200px;
    }
}

.login_form{
    position: absolute;
    bottom: 10px;
    width: 100%;
    padding:0 20px;
    box-sizing: border-box;
}

.btns{
    display: flex;
    justify-content: flex-end;
}

.logo{
  position:absolute;
  top: -75%;
  left:168%;
  width: 1500px;
}
// 设置登录按钮的颜色，包括默认颜色，hover鼠标经过颜色，以及鼠标点击时active颜色，超链接伪类可以用在任意元素上
.lgbtn{
  background-color: #22b39a !important;
  border: #22b39a !important;;
  color: #ffffff !important;
  font-weight: 700 !important;
}
.lgbtn:active{
  background-color: #09927b !important;
}
.reset{
  color: #ffffff !important;
  font-weight: 700 !important;
}
.companyname{
  display: block;
  color: white;
  margin-left: 3.5%;
  margin-top: -3%;
  font-weight: 700;
  display: block;
  background-image: linear-gradient(to right, rgb(3, 91, 255),rgb(255, 255, 255),rgb(255, 255, 255), rgb(83, 250, 0));
  -webkit-background-clip: text;
  color: transparent;
}
.contact{
  left: 45%;
  text-align: right;
  color: rgb(255, 255, 255);
  position: absolute;
  bottom: -30%;
}
.copyright{
  font-weight: 900;
  text-align: center;
  font-size: 70%;
  position: absolute;
  color: rgb(255, 234, 0);
  bottom: -90%;
  transform: translate(300%,-50%);
}
.carbon_logo{
  position: absolute;
  left: 50%;
  top: 237%;
  width: 12%;
}
.particles{
  width: 100%;
  height: 150% !important;
}
.el-form-item__error{
  color: rgb(255, 234, 0) !important;
  font-weight: 700 !important;
}
</style>
