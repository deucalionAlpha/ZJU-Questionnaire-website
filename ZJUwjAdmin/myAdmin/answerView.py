"""
程序名：回答问卷请求接口
功能：回答问卷后台处理函数
"""
from django.shortcuts import HttpResponse
import json
from myAdmin.models import *
from django.db import transaction
import datetime


############################################################
#功能：问卷回答者操作主入口
#最后更新：2019-05-24
############################################################
def opera(request):
    response={'code':0,'msg':'success'}
    if request.method=='POST':
        body=str(request.body,encoding='utf-8')
        print(body)
        try:
            info = json.loads(body)#解析json报文
        except:
            response['code'] = '-2'
            response['msg'] = '请求格式有误'
        opera_type=info.get('opera_type')#获取操作类型
        if opera_type:
            if opera_type=='get_info':#获取问卷信息
                response=getInfo(info,request)
            elif opera_type=='Timecheck':#判断问卷是否过期
                response=TimeCheck(info,request)
            elif opera_type=='get_temp_info':#获取问卷信息
                response=getTempInfo(info,request)
            elif opera_type=='submit_wj':#提交问卷
                response=submitWj(info,request)
            elif opera_type=='logincheck':#填写问卷界面注册判断
                response=Logincheck(info,request)
            else:
                response['code'] = '-7'
                response['msg'] = '请求类型有误'
        else:
            response['code'] = '-3'
            response['msg'] = '确少必要参数'
    else:
        response['code']='-1'
        response['msg']='请求方式有误'

    return HttpResponse(json.dumps(response))


def TimeCheck(info,request):
    print("TimeCheck!!!!!!!!!")
    wjId=info.get('wjId')
    res=Wj.objects.get(id=wjId)#查询id为wjId
    response = {'code':0, 'msg': 'success'}
    #获取当前时间 
    NowTime=datetime.datetime.now()
    print("Now")
    print(NowTime)
    print("The opentime")
    print(res.OpenTime)
    delta=(NowTime-res.OpenTime).days
    if(res.days!=-1):
        if(delta>res.days):
            response['code']='404' 
    #response['code']='404'#测试所用
    return response





def Logincheck(info,request):
    wjId=info.get('wjId')
    res=Wj.objects.get(id=wjId)#查询id为wjId
    register=res.register
    response = {'code': 0, 'msg': 'success'}
    # 查询django_session中是否有username，查询失败抛出异常
    # 查询成功判断username是否为空，若为空，返回404错误，不为空，返回成功信息
    if register==1:       
        try:
            username = request.session.get('username')
        except:
            response['code']='-4'
            response['msg']='操作失败'
        else:
            if username:
                response['data']={'user':username}
            else:
                response['code'] = '404'
                response['msg'] = '未登录'
        return response
    else:
        response['data']={'user':username}
        return response


Theoptions={} #全局！
TheQuestion={}
############################################################
#功能：获取问卷信息
#最后更新：2019-05-24
############################################################
def getInfo(info,request):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    index=1
    username = request.session.get('username')
    if wjId:
        try:#判断问卷id是否存在
            res=Wj.objects.get(id=wjId)#查询id为wjId
            response['title']=res.title
            response['desc']=res.desc
            response['register']=res.register
            print("register!!!!!!!!!!!!!!!!!!!!!!!")
            print(res.register)
        except:
            response['code'] = '-10'
            response['msg'] = '问卷不存在'
        else:
            if res.username==username or res.status==1:#只有问卷发布者或者此问卷为已发布才能查看 (关于权限的判断)
                obj = Question.objects.filter(wjId=wjId)
                detail=[]
                RelatedOption={}
                for item in obj:
                    temp={}
                    temp['title']=item.title
                    temp['type']=item.type
                    temp['id']=item.id#问题id
                    TheQuestion[item.id]=index
                    index=index+1
                    temp['row']=item.row
                    temp['must']=item.must
                    temp['numbertype']=item.numbertype
                    temp['lowdesc']=item.lowdesc
                    temp['highdesc']=item.highdesc
                    temp['relatedId']=item.relatedId
                    temp['relatedOp']=item.relatedOp
                    temp['selftype']=item.selftype
                    #获取选项
                    temp['options']=[]
                    if temp['type'] in ['radio', 'checkbox'] or temp['selftype'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                        optionItems = Options.objects.filter(questionId=item.id)
                        for optionItem in optionItems:
                            temp['options'].append({'title': optionItem.title, 'id': optionItem.id})
                            RelatedOption[optionItem.id]=optionItem.title
                    temp['radioValue']=-1#接收单选框的值
                    temp['checkboxValue'] =[]#接收多选框的值
                    temp['textValue']=''#接收输入框的值
                    detail.append(temp)  #将该问题加入问题列表！！！！！！！！！！！！
                    Theoptions[item.id]=temp['options']
                response['detail']=detail
                response['TheQuestion']=TheQuestion# id -> index
                response['RelatedOption']=RelatedOption
            else:
                response['code'] = '-10'
                response['msg'] = '问卷尚未发布'
            #使用二维数组来维护结构 不需要的数据结构可以删除  option[Q_index][op_index] = Answer_id  可以使用Theoptions[item.id]来
            OptionLists = [[] for i in range(index)] #index-1个问题 0,1,2,index-2
            index=1
            #print("related options!")
            for item in obj:
                temp={}
                temp['type']=item.type
                temp['selftype']=item.selftype
                if temp['type'] in ['radio', 'checkbox'] or temp['selftype'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                    optionItems = Options.objects.filter(questionId=item.id)
                    for optionItem in optionItems:
                        OptionLists[index].append(optionItem.id)
                index+=1
            response['options']=OptionLists
            
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

############################################################
#功能：提交问卷
#最后更新：2019-06-08
############################################################
@transaction.atomic
def submitWj(info,request):
    response = {'code': 0, 'msg': 'success'}
    wjId = info.get('wjId')
    useTime=info.get('useTime')
    detail=info.get('detail')
    Options=info.get('Options')
    username = request.session.get('username')
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')

    flag=0
    #判断是否为同一人
    
    res=Wj.objects.get(id=wjId)
    
    if res.register==1:
        #利用username与wjid搜索 如果有 则不可填  与之前插入问题 编辑问题逻辑类
        print("we use name.")
        result = Submit.objects.filter(username=username,wjId=wjId)
        print(result)
        if(result):
            print("already!!")
            flag=1
    else:
        print("we use ip.")
        #判断是否有重复ip
        result = Submit.objects.filter(submitIp=ip,wjId=wjId)
        print(result)
        if(result):
            print("already!!")
            flag=1
    if(flag==1):
        response['code'] = '-12'#已作答
        return response
    

    s1 = transaction.savepoint()#设置事务保存点 回滚使用
    if wjId:
        try:  # 判断问卷id是否存在
            res = Wj.objects.get(id=wjId)  # 查询id为wjId
            response['title'] = res.title
            response['desc'] = res.desc
        except:
            response['code'] = '-10'
            response['msg'] = '问卷不存在'
            return response
        if res.status==0:#当问卷状态为1(已发布)时才可回答
            response['code'] = '-10'
            response['msg'] = '问卷尚未发布'
            return response
        #记录提交信息
        submitInfo=Submit.objects.create(
            wjId=wjId,
            submitTime=datetime.datetime.now(),
            submitIp=ip,
            useTime=useTime,
            username=username
        )
        qItems=Question.objects.filter(wjId=wjId,must=True)#查询所有必填题目
        musts=[]
        for qItem in qItems:
            musts.append(qItem.id)#记录所有必填题目的题目id
        #记录答案
        for item in detail:
            #bug!!!!!!!!!!!没有接收到 relatedid？是none？？？Thequestion传回来之后变味了
            #级联问题比较特殊 需要答则答 不需要答可以不答 可以选择与前端相同给的方式来判断、这里给一个需不需要答的判断  
            if item['type']=='cascade':
                flag=0
                print("let's judge!")
                if Options[TheQuestion[item['relatedId']]][detail[TheQuestion[item['relatedId']]-1]['radioValue']]==item['relatedOp']:#级联选择是否需要被填写
                    flag=1
                    print("It should be answered!")
                else:
                    print("don't need!")
            # print(item)
            if item['type']=='radio' or (item['selftype']=='radio' and (flag==1)):#单选题
                if item['id'] in musts and item['radioValue']==-1:#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答'
                    break
                Answer.objects.create(
                    questionId=item['id'],
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=item['type'],
                    answer=item['radioValue'] #这个value记录的是索引 0,1,2,
                )
            elif item['type']=='checkbox' or (item['selftype']=='checkbox' and (flag==1)):#多选题
                if item['id'] in musts and len(item['checkboxValue'])==0:#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答'
                    break
                for value in item['checkboxValue']:
                    Answer.objects.create(
                        questionId=item['id'],
                        submitId=submitInfo.id,
                        wjId=wjId,
                        type=item['type'],
                        answer=value
                    )
            elif item['type']=='text' or (item['selftype']=='text' and (flag==1)):#填空题
                if item['id'] in musts and item['textValue']=='':#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答 '
                    break
                Answer.objects.create(
                    questionId=item['id'],
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=item['type'],
                    answer=item['textValue']
                )
            elif item['type']=='number' or (item['selftype']=='number' and (flag==1)):#填空题
                if item['id'] in musts and item['NumberValue']=='':#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答 '
                    break
                Answer.objects.create(
                    questionId=item['id'],
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=item['type'],
                    answer=item['NumberValue']
                )
            elif item['type']=='score' or (item['selftype']=='score' and (flag==1)):#评分题
                if item['id'] in musts and item['radioValue']==-1:#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答 '
                    break
                Answer.objects.create(
                    questionId=item['id'],
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=item['type'],
                    answer=item['radioValue'] #这里的Option编号是真实的评分 不同于单选题
                )   

        #所有都无误的话 更新问卷的填写数量  以及判断填写数量
        res=Wj.objects.get(id=wjId)
        #res.totalrecord=1/
        
        if(res.totalnumber>0):#如果总填写次数有数量要求
            if(res.totalrecord<res.totalnumber):
                res.totalrecord=res.totalrecord+1#总填写次数+1
            else: #超出填写数目限制
                print("该问卷已达到总填写量!")
                response['code'] = '-11'
                response['msg'] = '该问卷已达到总填写量!'
                return response
        else:#没有数量要求 直接添加
            res.totalrecord=res.totalrecord+1#总填写次数+1
        #每日填写判断 如果到了新的一天 dayrecord进行更新 这个与设置填写周期也比较像  看一下submit那里的获取时间
        #response['code']='-11'
        #response['msg']='该问卷今日已达到总填写量!'
        
        res.save()             
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'

    return response
