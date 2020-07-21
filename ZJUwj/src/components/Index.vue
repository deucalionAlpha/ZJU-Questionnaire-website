<!--
程序名：网站首页
功能：对网站进行介绍
-->
<template>
  <div class="main">
     <el-carousel  height="600px" >
        <el-carousel-item v-for="(item,index) in topImg" :key="index">
          <!--<div style="background-color: black;width: 100%;height: 100%;">-->
            <img :src="item.url" style="width: 100%;height: 100%;">
          <div class="cover">
            {{item.title}}<br>
            <span style="font-size: 35px">{{item.subTitle}}</span>
          </div>
        </el-carousel-item>
      </el-carousel>
    <!--<el-divider></el-divider>-->

<el-divider></el-divider>
    <img src="/static/images/demo1.png" class="demoImg"><br>
    <img src="/static/images/demo2.png" class="demoImg"><br><br>


  </div>
</template>
<script>
  export default{
    data(){
      return{
        topImg:[
          {
            'title':'在线问卷调查系统',
            'subTitle':'Online Questionnaire Survey System',
            'url':'/static/images/index_1.jpg'
          },
          {
            'title':'简洁的操作界面',
            'subTitle':'Simple Opening Method',
            'url':'/static/images/6.jpg'
          },
          {
            'title':'多样问卷结果统计',
            'subTitle':'Diversified data visualization',
            'url':'/static/images/11.jpg'
          },
        ]
      }
    }
  }
</script>
<style scoped>
  .main{
    position: relative;
    width: 100%;
    height: 100%;
  }
 .bottom{
    height: 150px!important;
    background-color: #4b5054;
    color: #9b9ea0;
    position: relative;
    padding: 20px;
  }
  .demoImg{
    width: 800px;
    height:500px;
    /*border-radius: 5px;*/

    margin-top: 20px;
     box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
  }
  .cover{
    position:absolute;width: 100%;height: 100%;background-color: rgba(0,0,0,0.6);z-index: 100;left: 0;top:0;color: white;font-size: 50px;line-height: 60px;padding-top: 240px;
  }
  .lj{

  }
  .b{
    font-weight: 700;
  }

</style>
