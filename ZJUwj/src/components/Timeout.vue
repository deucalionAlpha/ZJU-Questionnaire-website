<!--
程序名：题型页面
功能：重复填写问卷跳转的页面
-->
<template>
  <div class="Timeout">
    <el-card shadow="never" style="font-size: 18px;line-height: 40px;padding: 10px;">
      <i class="el-icon-warning" style="color: red;font-size: 50px"></i><br>
      本问卷已过期，感谢您的参与！<br><br>
      <el-divider></el-divider>
      <el-link type="info" href="/index">浙里问卷&nbsp;提供技术支持</el-link>
    </el-card>
  </div>
</template>
<style scoped>
  .Done{
    padding: 40px;
  }
</style>
<style>
  .el-divider--horizontal{
    margin: 10px;
  }
</style>
