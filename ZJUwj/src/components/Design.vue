<!--
程序名：问题设计页面
功能：对问卷中问题的添加、编辑、删除
-->
<template>
  <div class="Design" v-loading="loading" element-loading-text="加载中...">
    <h3>{{title}}</h3>
      <div class="top" v-if="desc!=''">
        {{desc}}
      </div>
    <el-card class="box-card" v-for="(item,index) in detail" style="margin: 10px;">
        <div slot="header" class="clearfix">
          <div class="questionTitle">
            <!--显示必填标识-->
            <span style="color: #F56C6C;">
              <span v-if="item.must">*</span>
              <span v-else>&nbsp;</span>
            </span>
            <span style="color: black;margin-right: 3px;">{{(index+1)+'.'}}</span>
            {{item.title}}
            <span style="color: black;margin-right: 3px;">
              <span v-if="item.numbertype=='int'">&nbsp;(整数填写)</span>
              <span v-if="item.numbertype=='float'">&nbsp;(小数填写)</span>
              <span v-if="item.numbertype=='both'">&nbsp;(整数或小数填写)</span>
              <span v-if="item.type=='cascade'">(级联问题{{Question[item.relatedId]}}的{{RelatedOption[item.relatedOp]}}选项)</span>
              <span v-else>&nbsp;</span>
            </span>
          </div>

          <div style="float: right;">
            <el-button style="padding: 2px" type="text" @click="editorQuestion(item)">编辑</el-button>
            <el-button style="padding: 2px;color: #F56C6C" type="text" @click="deleteQuestion(index)">删除</el-button>
          </div>
        </div>

        <!--评分题展示-->
        <div class="text item" v-if="item.type=='score'||item.selftype=='score'">
            <span style="color: black; margin-right: 3px;">{{item.lowdesc}}</span>
              <div class="ScoreButton" v-for="(index) in item.row">
                 <el-radio v-model="item.ScoreValue" :label="index" style="margin: 5px;">{{ index }}</el-radio>
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
          v-model="item.textValue">
        </el-input>
      </el-card>
      <el-button  icon="el-icon-circle-plus" @click="addQuestion" style="margin-top: 10px;">添加题目</el-button>

<br><br><br><br><br>

    <!--添加题目弹窗-->
    <el-dialog :title="dialogTitle" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddQuestion" label-width="80px">
        <el-form-item label="题目类型" style="width: 100%;">
          <el-select v-model="willAddQuestion.type" placeholder="请选择题目类型" @change="typeChange">
          <el-option
            v-for="item in allType"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        </el-form-item>
        <el-form-item label="是否必填" style="width: 100%;">
          <el-checkbox v-model="willAddQuestion.must">必填</el-checkbox>
        </el-form-item>
        <el-form-item label="题目标题" style="width: 100%;">
          <el-input v-model="willAddQuestion.title" placeholder="请输入标题" ></el-input>
        </el-form-item>

        <template v-if="willAddQuestion.type=='radio'||willAddQuestion.type=='checkbox'">
          <el-form-item :label="'选项'+(index+1)" v-for="(item,index) in willAddQuestion.options" >
            <el-row>
              <el-col :span="16">
                <el-input  v-model="item.title" placeholder="请输入选项名" style="width: 90%;"></el-input>
              </el-col>
            <el-col :span="8">
              <el-button type="danger" plain class="" @click="deleteOption(index)" >删除选项</el-button>
            </el-col>
            </el-row>

          </el-form-item>
          <el-button type="primary" plain class="addOptionButton" @click="addOption">新增选项</el-button>
        </template>

        <template v-if="willAddQuestion.type=='score'">
        <el-form-item label="低分说明" style="width: 100%;">
          <el-input v-model="willAddQuestion.lowdesc" placeholder="请输入相应说明" ></el-input>
        </el-form-item>
        <el-form-item label="高分说明" style="width: 100%;">
          <el-input v-model="willAddQuestion.highdesc" placeholder="请输入相应说明" ></el-input>
        </el-form-item>
          <el-form-item label="评分等级">
            <el-input-number v-model="willAddQuestion.row" :min="3" :max="7" label="等级"></el-input-number>
          </el-form-item>
        </template>


        <template v-if="willAddQuestion.type=='text'">
          <el-form-item label="填空">
            <el-input type="textarea"
  :rows="willAddQuestion.row" style="width: 80%" resize="none"></el-input>
          </el-form-item>
          <el-form-item label="行数">
            <el-input-number v-model="willAddQuestion.row" :min="1" :max="10" label="描述文字"></el-input-number>
          </el-form-item>
        </template>


        <template v-if="willAddQuestion.type=='number'">
          <el-form-item label="数字类型" style="width: 100%;">
            <el-select v-model="willAddQuestion.numbertype" placeholder="请选择填写数字类型"> <!--  @change="typeChange" 这个应该是不需要吧 不用刷新页面 只要记录下来就行-->
            <el-option
              v-for="item in Numtype"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          </el-form-item>
            <el-form-item label="填写数字">
            <el-input type="textarea"
  :rows="willAddQuestion.row" style="width: 80%" resize="none"></el-input>
          </el-form-item>
        </template>

        <template v-if="willAddQuestion.type=='cascade'">
          <el-form-item label="关联题目" style="width: 100%;">
            <el-select v-model="willAddQuestion.relatedId" placeholder="请选择关联题目"> <!-- 记录关联题目.还没有写入后端-->
              <el-option
                v-for="(item,index) in detail"
                :key="item.id"
                :label="index+1"
                :value="item.id">
              </el-option>
            </el-select>  
          </el-form-item>
          <!-- 记录关联选项-->
          <el-form-item label="关联选项" style="width: 100%;">
            <el-select v-model="willAddQuestion.relatedOp" placeholder="请选择关联选项"> <!-- 动态操作 后端检测是否为选择题并且返回options-->
              <el-option
                v-for="item in Options[willAddQuestion.relatedId]"
                      :key="item.id"
                      :label="item.title"
                      :value="item.id">
              </el-option>
            </el-select>  
          </el-form-item>
          <el-form-item label="自身题目类型" style="width: 100%;">
            <el-select v-model="willAddQuestion.selftype" placeholder="请选择题目类型">
              <el-option
                v-for="item in SelfType"
                :key="item.value"
                :label="item.label"
                :value="item.value">
             </el-option>
            </el-select>
          </el-form-item>
          <template v-if="willAddQuestion.selftype=='radio'||willAddQuestion.selftype=='checkbox'">
            <el-form-item :label="'选项'+(index+1)" v-for="(item,index) in willAddQuestion.options" >
              <el-row>
                <el-col :span="16">
                  <el-input  v-model="item.title" placeholder="请输入选项名" style="width: 90%;"></el-input>
                </el-col>
              <el-col :span="8">
                <el-button type="danger" plain class="" @click="deleteOption(index)" >删除选项</el-button>
              </el-col>
              </el-row>

            </el-form-item>
            <el-button type="primary" plain class="addOptionButton" @click="addOption">新增选项</el-button>
          </template>

          <template v-if="willAddQuestion.selftype=='score'">
          <el-form-item label="低分说明" style="width: 100%;">
            <el-input v-model="willAddQuestion.lowdesc" placeholder="请输入相应说明" ></el-input>
          </el-form-item>
          <el-form-item label="高分说明" style="width: 100%;">
            <el-input v-model="willAddQuestion.highdesc" placeholder="请输入相应说明" ></el-input>
          </el-form-item>
            <el-form-item label="评分等级">
              <el-input-number v-model="willAddQuestion.row" :min="1" :max="7" label="等级"></el-input-number>
            </el-form-item>
          </template>


          <template v-if="willAddQuestion.selftype=='text'">
            <el-form-item label="填空">
              <el-input type="textarea"
    :rows="willAddQuestion.row" style="width: 80%" resize="none"></el-input>
            </el-form-item>
            <el-form-item label="行数">
              <el-input-number v-model="willAddQuestion.row" :min="1" :max="10" label="描述文字"></el-input-number>
            </el-form-item>
          </template>


          <template v-if="willAddQuestion.selftype=='number'">
            <el-form-item label="数字类型" style="width: 100%;">
              <el-select v-model="willAddQuestion.numbertype" placeholder="请选择填写数字类型"> <!--  @change="typeChange" 这个应该是不需要吧 不用刷新页面 只要记录下来就行-->
              <el-option
                v-for="item in Numtype"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            </el-form-item>
              <el-form-item label="填写数字">
              <el-input type="textarea"
    :rows="willAddQuestion.row" style="width: 80%" resize="none"></el-input>
            </el-form-item>
          </template>
        </template>

      </el-form>
      <br>
      <div style="width: 100%;text-align: right">
        <el-button style="margin-left: 10px;" @click="dialogShow=false">取消</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="checkAddQuestion">完成</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  import {designOpera} from './api'
  export default{
    data(){
      return{
        loading:false,//页面加载中
        dialogShow:false,
        dialogTitle:'',
        detail:[],
        Options:[],//存储related options
        Question:[],//存储id->index的关系
        RelatedOption:[],
        wjId:0,
        title:'',
        desc:'',

        TheNumber:{
          id:0,
          type:'',
          options:[
            {
              title:'',//数字种类
              id:0//种类id 没有和数据库同步
            }
          ],
        },

        willAddQuestion:{
          id:0,
          type:'',
          title:'',
          options:[
            {
              title:'',//选项标题
              id:0//选项id
            }
          ],
          row:1,
          must:false,//是否必填
          numbertype:false,//是否必填
          lowdesc:'',//评分题的低分描述
          highdesc:'',
          relatedId:false,
          relatedOp:false,
          selftype:false,
        },

        Numtype:[
          {
            value:'int',
            label:'整数',
          },
          {
            value:'float',
            label:'小数',
          },
          {
            value:'both',
            label:'整数或小数',
          },
        ],
        SelfType:[
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
          {
            value:'number',
            label:'数字填写题',
          },
          {
            value:'score',
            label:'评分题',
          },
          {
            value:'location',
            label:'地址题',
          },
        ],
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
          {
            value:'number',
            label:'数字填写题',
          },
          {
            value:'score',
            label:'评分题',
          },
          {
            value:'cascade',
            label:'级联选择题',
          },
          {
            value:'location',
            label:'地址题',
          },
        ],
      }
    },
    methods:{
      //初始化问卷所有问题
      init(wjId,title,desc){
        this.wjId=wjId;
        this.title=title;
        this.desc=desc;
        this.getQuestionList();
      },
      //获取问题列表(问卷内容)
      getQuestionList(){
        this.detail=[];
        this.loading=true;
        designOpera({
          opera_type:'get_question_list',
          username:'test',
          wjId:this.wjId,
        })
          .then(data=>{
            console.log(data);
            this.detail=data.detail;
            this.Options=data.options;
            this.Question=data.TheQuestion;
            this.RelatedOption=data.RelatedOption;
            this.loading=false;
          })
      },
      //点击添加问题按钮
      addQuestion(){
        if(this.wjId==0||this.wjId==null){
          this.$message({
            type: 'error',
            message: '请先创建问卷!'
          });
          return;
        }
        this.dialogTitle='添加题目';
        this.TheNumber={
          id:0,
          type:'',
          options:[
            {
              title:'',//数字种类
              id:0//种类id 没有和数据库同步
            }
          ],
        };
        this.willAddQuestion={
          id:0,
          type:'',
          title:'',
          options:[
            {
              title:'',//选项标题
              id:0//选项id
            }
          ],
          row:1,
          must:false,//是否必填
        };
        this.dialogShow=true;
      },
      //删除问题
      deleteQuestion(index){
        this.$confirm('确定删除此题目?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          designOpera({
            opera_type:'delete_question',
            username:'test',
            questionId:this.detail[index].id,
          })
            .then(data=>{
              console.log(data);
              if(data.code==0){
                this.detail.splice(index,1);
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
              }
              else{
                this.$message({
                  type: 'error',
                  message: data.msg
                });
              }
            })
        });

      },
      //确认添加/保存题目
      checkAddQuestion(){
        //添加保存问题
        let newItem={};//新添加的问题对象
        newItem={
          type:this.willAddQuestion.type,
          title:this.willAddQuestion.title,
          options:this.willAddQuestion.options,
          row:this.willAddQuestion.row,
          must:this.willAddQuestion.must,
          numbertype:this.willAddQuestion.numbertype,
          lowdesc:this.willAddQuestion.lowdesc,
          highdesc:this.willAddQuestion.highdesc,
          relatedId:this.willAddQuestion.relatedId,
          relatedOp:this.willAddQuestion.relatedOp,
          selftype:this.willAddQuestion.selftype,
        };
        newItem.radioValue=-1;
        newItem.checkboxValue=[];
        newItem.textValue='';
        designOpera({
          opera_type:'add_question',
          username:'test',
          wjId:this.wjId,
          questionId:this.willAddQuestion.id,
          title:this.willAddQuestion.title,
          type:this.willAddQuestion.type,
          options:this.willAddQuestion.options,
          row:this.willAddQuestion.row,
          must:this.willAddQuestion.must,
          numbertype:this.willAddQuestion.numbertype,
          lowdesc:this.willAddQuestion.lowdesc,
          highdesc:this.willAddQuestion.highdesc,
          relatedId:this.willAddQuestion.relatedId,
          relatedOp:this.willAddQuestion.relatedOp,
          selftype:this.willAddQuestion.selftype,
        })
          .then(data=>{
            console.log(data);
            newItem.id=data.id;
            if(data.code==0){
              this.dialogShow=false;
              this.$message({
                type: 'success',
                message: '保存成功!'
              });
              this.getQuestionList();
            }
            else{
              this.dialogShow=false;
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
            this.willAddQuestion={
              id:0,
              type:'',
              title:'',
              options:[''],
              row:1,
              must:false,
            };
          });
      },
      //点击编辑问题按钮
      editorQuestion(item){
        this.willAddQuestion.title=item.title;
        this.willAddQuestion.type=item.type;
        this.willAddQuestion.options=JSON.parse(JSON.stringify(item.options));
        this.willAddQuestion.text=item.text;
        this.willAddQuestion.row=item.row;
        this.willAddQuestion.must=item.must;
        this.willAddQuestion.id=item.id;
        this.willAddQuestion.lowdesc=item.highdesc;
        this.willAddQuestion.highdesc=item.lowdesc;
        this.willAddQuestion.numbertype=item.numbertype;
        this.dialogTitle='编辑问题';
        this.dialogShow=true;
      },
      //添加选项
      addOption(){
        this.willAddQuestion.options.push({
          title:'',
          id:0,
        });
      },
      //删除选项
      deleteOption(index){
        this.willAddQuestion.options.splice(index,1);
      },
      //切换问题类型
      typeChange(value){
        console.log(value);
        this.willAddQuestion.type=value;
        this.willAddQuestion.text='';
        this.row=1;
      },
      //切换数字类型
      NumChange(value){
        console.log(value);
        this.TheNumber.type=value;
        this.willAddQuestion.numbertype=value;
      },
    }
  }
</script>
<style scoped>

  .Design{

  }
  .Design .dialog{
    text-align: left;
  }
  .Design .questionTitle{
    display: inline-block;
    width: 80%;
    font-size: 16px;
    color: #303133;
  }
  .Design .addOptionButton{
    display: inline-block;
    margin-left: 80px;
  }
  .Design .ScoreButton{
    display: inline-block;
    margin-left: 30px;
  }
  .box-card{
    width: 100%;
    text-align: left;
  }
  .Design .top{
    color: #606266;
    margin-left: 20px;
    padding: 0 10px 10px 10px;
    border-bottom: 3px solid #409EFF;
    font-size: 15px;
    line-height: 22px;
    text-align: left;
  }
</style>
