/**
 * 程序名：api接口
 * 功能：与后端通讯的api接口定义
 */
import axios from 'axios'
axios.defaults.withCredentials = true; //配置为true
// 改成对应的服务端地址
axios.defaults.baseURL = 'http://120.79.35.153/'

//问卷设计者操作
export const designOpera=data=>{
  return axios.post('/api/design',data).then(res=>res.data);
};

//问卷回答者操作
export const answerOpera=data=>{
  return axios.post('/api/answer',data).then(res=>res.data);
};
