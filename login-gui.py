#coding=utf-8
'''
登陆界面
'''
import wx
import webbrowser
import pickle
from wx.lib.embeddedimage import PyEmbeddedImage
import os

class LoginFrame(wx.Frame):
    fx = None #框架x轴位置
    fy = None #框架y轴位置
    mx = None #移动x轴位置
    my = None #移动y轴位置
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u'登陆',style=wx.SIMPLE_BORDER,size=(500,300))
        self.Center()
        self.SetBackgroundColour('#b3d8ff')
        # ******************主界面设计S
        mainBoxSizer = wx.BoxSizer(wx.VERTICAL)

        topPanel = wx.Panel(self,-1,size=(500,30))
        topPanel.SetBackgroundColour('#80beff')
        file = open('./source/images/close.png', 'rb')
        b64 = file.read().encode('base64')
        file.close()
        bitmap = PyEmbeddedImage(b64).GetBitmap()
        self.closeButton = wx.StaticBitmap(topPanel, -1 , bitmap,pos=(470,3))

        self.closeButton.Bind(wx.EVT_LEFT_DOWN,self.OnCloseApp)
        mainBoxSizer.Add(topPanel)

        #顶部导航
        mainBoxSizer.Add((0,10))
        titleLabel = wx.StaticText(self, -1, u'后台管理系统', style=wx.ALIGN_CENTER)
        titleFont = wx.Font(25, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        titleLabel.SetFont(titleFont)
        mainBoxSizer.Add(titleLabel, 1, wx.EXPAND)
        mainBoxSizer.Add((0, 10))
        #构造登陆部分
        loginPanel = wx.Panel(self,-1,size=(500,210))
        loginPanel.SetBackgroundColour('#e5f2ff')

        loginSizer = wx.GridBagSizer(hgap=5, vgap=5)

        #空一列
        loginSizer.Add((50,50),pos=(0,0),span=(5,1),flag=wx.EXPAND)
        loginSizer.Add((50, 50), pos=(0, 1),flag=wx.EXPAND)

        file = open('./source/images/head_image.jpg', 'rb')
        b64 = file.read().encode('base64')
        file.close()
        bitmap = PyEmbeddedImage(b64).GetBitmap()
        headImg = wx.StaticBitmap(loginPanel, -1, bitmap,size=(10,10))
        loginSizer.Add(headImg, pos=(1, 1), span=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL,border=10)

        loginSizer.Add((15, 0), pos=(0, 2), span=(5, 1), flag=wx.EXPAND)

        ctrlFont = wx.Font(18,wx.NORMAL, wx.NORMAL, wx.NORMAL)
        loginSizer.Add((50, 50), pos=(0, 3), flag=wx.EXPAND)
        self.userNameCtrl = wx.TextCtrl(loginPanel,-1,size=(190,30))
        self.userNameCtrl.SetFont(ctrlFont)
        loginSizer.Add(self.userNameCtrl, pos=(1, 3), flag=wx.EXPAND)

        self.passwordCtrl = wx.TextCtrl(loginPanel, -1,size=(190,30),style=wx.TE_PASSWORD)
        self.passwordCtrl.SetFont(ctrlFont)
        loginSizer.Add(self.passwordCtrl, pos=(2, 3), flag=wx.EXPAND)

        #记住密码和自动登陆
        pwdAutoSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.savePwd = wx.CheckBox(loginPanel, -1, u"记住密码")
        pwdAutoSizer.Add(self.savePwd)
        pwdAutoSizer.Add((40,10))
        self.autoLogin = wx.CheckBox(loginPanel, -1, u"自动登陆")
        pwdAutoSizer.Add(self.autoLogin)
        loginSizer.Add(pwdAutoSizer,pos=(3,3))


        self.loginButton = wx.Button(loginPanel, -1, label=u'登 录', size=(190,30))
        self.loginButton.Bind(wx.EVT_BUTTON,self.OnLoginButton)
        loginSizer.Add(self.loginButton, pos=(4, 3), span=(3, 1),flag=wx.ALIGN_CENTER_VERTICAL)

        loginSizer.Add((50, 50), pos=(0, 4), flag=wx.EXPAND)
        self.forgetPwd = wx.StaticText(loginPanel, -1,label=u'忘记密码')
        self.forgetPwd.Bind(wx.EVT_LEFT_DOWN,self.OnOpenUrl)
        loginSizer.Add(self.forgetPwd, pos=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        self.getHelp = wx.StaticText(loginPanel, -1,label=u'查看帮助')
        self.getHelp.Bind(wx.EVT_LEFT_DOWN,self.OnOpenUrl)
        loginSizer.Add(self.getHelp, pos=(2, 4), flag=wx.ALIGN_CENTER_VERTICAL)

        loginPanel.SetSizer(loginSizer)
        loginSizer.Fit(loginPanel)
        mainBoxSizer.Add(loginPanel)
        self.SetSizer(mainBoxSizer)
        # ******************主界面设计E




        #鼠标事件左键按下事件
        topPanel.Bind(wx.EVT_LEFT_DOWN,self.OnMouseLeftDown,topPanel)
        # 鼠标事件左键松开事件
        topPanel.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        #鼠标事件
        topPanel.Bind(wx.EVT_MOTION, self.OnMove)


        self.OnInit()
    #打开url地址
    def OnOpenUrl(self,event):
        webbrowser.open('http://www.baidu.com')

    #关闭应用
    def OnCloseApp(self,event):
        self.Destroy()
    #鼠标左键按下事件
    def OnMouseLeftDown(self,event):
        # 如果点击事件在右上角方位某个区域，就关闭窗口
        self.mx = event.x
        self.my = event.y
        self.fx, self.fy = self.GetPosition()


    # 鼠标左键松开事件
    def OnMouseLeftUp(self, event):
        self.fx = None  # 框架x轴位置
        self.fy = None  # 框架y轴位置
        self.mx = None  # 移动x轴位置
        self.my = None  # 移动y轴位置
    #鼠标移动事件
    def OnMove(self,event):

        if self.mx != None and self.my != None:
            x,y = event.x,event.y #当前鼠标移动的位置
            #鼠标移动的偏移量
            self.SetPosition((self.fx-(self.mx - x),self.fy-(self.my - y)))

            self.fx, self.fy = self.GetPosition()

    #初始化数据
    def OnInit(self):

        if os.path.exists('./source/file-data/data-user-login-login.pkl'):

            fp = open('./source/file-data/data-user-login-login.pkl', 'rb')
            userInfoDic = pickle.load(fp)

            if userInfoDic:
                if userInfoDic['savePassword'] == True or userInfoDic['autoLogin'] == True:
                    username = userInfoDic['username']
                    self.userNameCtrl.SetValue(username)
                    password = userInfoDic['password']
                    self.passwordCtrl.SetValue(password)
                    self.savePwd.SetValue(userInfoDic['savePassword'])
                    self.autoLogin.SetValue(userInfoDic['autoLogin'])

                    if userInfoDic['autoLogin'] == True:
                        self.OnLogin(username, password)


    #处理登陆点击按钮
    def OnLoginButton(self,event):
        username = self.userNameCtrl.GetValue()

        password = self.passwordCtrl.GetValue()

        savePassword = self.savePwd.GetValue()

        autoLogin = self.autoLogin.GetValue()

        if username == '':
            print u'请输入用户名'
            return False
        elif password == '':
            print u'请输入密码'
            return False
        elif savePassword == True or autoLogin == True:#需要将用户的登陆信息本地化存储
            userInfoDic = {'username':username,'password':password,'savePassword':savePassword,'autoLogin':autoLogin}
            fp = open('./source/file-data/data-user-login-login.pkl','wb')
            pickle.dump(userInfoDic,fp)
            fp.close()

        self.OnLogin(username,password)


    #处理登陆
    def OnLogin(self,username,password):
        print username
        print password


if __name__ == '__main__':
    app = wx.App()
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()