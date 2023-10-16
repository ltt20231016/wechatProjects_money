// pages/login/login.js
const app=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    username:'',
    password:'',
  },
  login(){
      //1. 发送网络请求
      //2. 数据绑定
      wx.showLoading({
        mask: true,
      })  //进入页面时的加载框
      wx.request({
        url: 'http://127.0.0.1:8000/api/login/',
        method: "POST",
        data: {
          username: this.data.username,
          password: this.data.password
        },
        header:{
          'content-type': 'application/json'
        },
        success: res => {
          console.log(res)
          if(res.data.status==500){
            //登陆失败
            wx.showToast({
              title: res.data.msg,
              icon: 'error'
            })
          }
          else{
            wx.showToast({
              title: '登录成功',
              icon: 'success'
            })
            //登录成功，token赋值
            app.globalData.userInfo=res.data.user
            console.log( " App.globalData.UserInfo："+app.globalData.userInfo)
            //登录成功，跳转到首页
            // wx.navigateTo({
            //   url: '/pages/index/index',
            // })
            wx.switchTab({
              url: '/pages/index/index',
            })
          }
        }
      })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})