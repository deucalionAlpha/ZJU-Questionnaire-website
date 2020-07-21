<!--
程序名：问卷填写页面
功能：用户打开问卷链接对问卷进行填写
-->
<template>
  <div class="display">
    <div class="content">
      <h3>{{title}}</h3>
      <div class="top" v-if="desc!=''">
        {{desc}}   <!--Question[item.relatedId]=1 -->
      </div>    <!--Options[Question[item.relatedId]][detail[Question[item.relatedId]-1].radioValue]==item.relatedOp-->
      <el-card class="box-card" v-for="(item,index) in detail" v-if="item.type!='cascade'||Options[Question[item.relatedId]][detail[Question[item.relatedId]-1].radioValue]==item.relatedOp">  <!--detail[Question[item.relatedId]-1].radioValue==0  关联问题所选的选项索引 -->
        <div slot="header" class="clearfix">  <!--就这样判断 找好维护的数据结构即可  每个显示栏目都要添加 填写正常填写即可-->
          <div class="questionTitle">  
            <!--显示必填标识-->
            <span style="color: #F56C6C;">
              <span v-if="item.must">*</span>
              <span v-else>&nbsp;</span>
            </span>
            {{(index+1)+'.'+item.title}}
            <span style="color: black;margin-right: 3px;">
              <span v-if="item.numbertype=='int'">&nbsp;(整数填写)</span>
              <span v-if="item.numbertype=='float'">&nbsp;(小数填写)</span>
              <span v-if="item.numbertype=='both'">&nbsp;(整数或小数填写)</span>
              <span v-if="item.type=='cascade'">(级联问题{{Question[item.relatedId]}}的{{RelatedOption[item.relatedOp]}}选项)</span>
              <span v-else>&nbsp;</span>
            </span>
          </div>
        </div>


        <!--评分题展示-->
        <div class="text item" v-if="item.type=='score'||(item.selftype=='score')">
            <span style="color: black; margin-right: 3px;">{{item.lowdesc}}</span>
              <div class="ScoreButton" v-for="(index) in item.row">
                 <el-radio v-model="item.radioValue" :label="index" style="margin: 5px;">{{ index }}</el-radio> 
              </div>
            <span style="color: black; margin-right: 3px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{item.highdesc}}</span>
        </div>

        <!--单选题展示-->
        <div class="text item" v-if="item.type=='radio'||item.selftype=='radio'" v-for="(option,index) in item.options">
          <el-radio v-model="item.radioValue" :label="index" style="margin: 5px;">{{ option.title }}</el-radio>
        </div>
        
        <!--多选题展示-->
        <el-checkbox-group v-if="item.type=='checkbox'||item.selftype=='checkbox'" v-model="item.checkboxValue">
          <div class="text item"  v-for="(option,index) in item.options">
            <el-checkbox :label="index" style="margin: 5px;">{{ option.title }}</el-checkbox>
          </div>
        </el-checkbox-group>

        <!--填空题展示-->
        <el-input
          v-if="item.type=='text'||item.selftype=='text'"
          type="textarea"
          :rows="item.row"
          resize="none"
          v-model="item.textValue">
        </el-input>

        <!--数字填写题展示-->
        <el-input
          v-if="item.type=='number'||item.selftype=='number'"
          type="textarea"
          :rows="item.row" 
          resize="none"
          v-model="item.NumberValue">
        </el-input>
      </el-card>
       <el-button type="primary" style="margin: 5px;" @click="submit" :loading="submitLoading">{{submitText}}</el-button>

      <div class="bottom">
        <el-link type="info" href="/index">浙里问卷&nbsp;提供技术支持</el-link>
      </div>
    </div>
  </div>
</template>
<script>
  import {answerOpera} from './api'
  import {designOpera} from './api'
  export default{
    data(){
      return{
        dialogShow:false,
        dialogTitle:'',
        dialogType:1,//1添加 2修改
        oldItem:null,//编辑中问题的对象
        willAddQuestion:{
          type:'',
          title:'',
          options:[''],
          text:'',
          row:1,
        },
        allType:[
          {
            value:'radio',
            label:'单选题',
          },
          {
            value:'checkbox',
            label:'多选题',
          },
          {
            value:'text',
            label:'填空题',
          },
        ],
        title:'',
        desc:'',
        register:'',
        detail:[],
        Options:[],//存储related options
        Question:[],//存储id->index的关系
        RelatedOption:[],
        startTimestamp:0,//填写问卷开始时间戳 毫秒
        submitLoading:false,//提交按钮 加载中状态
        submitText:'提交',//提交按钮文字
      }
    },
    mounted(){
      var wjId=this.$route.params.id;
      answerOpera({
          opera_type:'Timecheck',
          wjId:wjId,
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){ //检查问卷是否已过期
            this.$message({
              type: 'error',
              message: '此问卷已经过期，谢谢您的参与！',
              showClose: true
            });
            this.$router.push({path:'/Timeout'})
          }
          else{
            this.getWjList();
          }
      })
      answerOpera({
          opera_type:'logincheck',
          wjId:wjId,
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){//如果返回的错误是404，跳转到登录页面
            this.$message({
              type: 'error',
              message: '此问卷需要已注册用户回答，请先登录或注册！',
              showClose: true
            });
            this.$router.push({path:'/login'})
          }
          else{
            this.getWjList();
          }
        })
      answerOpera({
        opera_type:'get_info',
        wjId:wjId,
        username:'test'//增加登录验证后不需传递（后端从session获取）
      })
        .then(data=>{
          console.log(data);
          if(data.code==0){
            this.title=data.title;
            this.desc=data.desc;
            this.detail=data.detail;
            this.Options=data.options;
            this.Question=data.TheQuestion;
            this.RelatedOption=data.RelatedOption;
            this.register=data.register;
            document.title=data.title;
          }
          else{
            this.$message({
              type: 'error',
              message: data.msg
            });
          }
        })
      this.startTimestamp = new Date().getTime();//时间戳 毫秒
    },
    methods:{
      //提交问卷
      submit(){
        this.submitLoading=true;
        this.submitText='提交中';
        var wjId=this.$route.params.id;
        let useTime=parseInt((new Date().getTime()-this.startTimestamp)/1000);//填写问卷用时 秒
        answerOpera({
          opera_type:'submit_wj',
          wjId:wjId,
          useTime:useTime,
          detail:this.detail,
          Options:this.Options,//存储related options
          Question:this.Question//存储id->index的关系
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){//在这里分支判断 如果是已经填写过了 会有一个提示已经填写过的页面
              //提交成功
              this.submitLoading=false;
              this.submitText='提交';
              this.$router.push({path:'/thankyou'});//跳到欢迎页
            }
            else if(data.code==-12)
            {
              this.submitLoading=false;
              this.submitText='提交';
              this.$router.push({path:'/Done'});//跳到已提交提示页
            }
            else{
              this.submitLoading=false;
              this.submitText='提交';
              this.$notify.error({
                title: '错误',
                message: data.msg,
              });
            }
          })
      }
    }
  }
</script>
<style scoped>
  .display{
    text-align: center;
    padding: 20px;
  }
  .display .top{
    color: #606266;
    padding: 0 10px 10px 10px;
    border-bottom: 3px solid #409EFF;
    font-size: 15px;
    line-height: 22px;
    text-align: left;
  }
  .display .content{
    width: 100%;
    max-width: 800px;
    display: inline-block;
    text-align: center;
  }
  .display .box-card{
    text-align: left;
    width: 100%;
    margin:10px 0 10px 0;
  }
  .display .ScoreButton{
    display: inline-block;
    margin-left: 30px;
  }
  .display .bottom{
    margin: 20px 10px 20px 10px;
    color: #909399;
  }
  .display a:link,a:visited,a:active {
    color: #909399;
    text-decoration:none;
  }
</style>
