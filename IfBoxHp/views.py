from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.sessions import *
from django.db.models import Q


from IfBoxHp.models import *
from IfBoxHp.forms import *
import re

from datetime import date,datetime,timedelta
import calendar
from pytz import timezone
def checklogin(request):
    flag=False
    if not "username" in request.session:
        if "p" in request.GET:
            nextpage=request.GET["p"]
            request.session["page"]=nextpage
        flag=True
    return flag

def getcontext(request,url):
    url+="?"
    for j,i in enumerate(request.GET):
        param=request.GET[i]
        if j==0:
            url+=i+"="+param
        else:
            url += "&" + i + "=" + param
    return url

def makedatetime(s):
    return ("2000-01-01 "+s)
def makedobject(t):
    h=t.hour
    m=t.minute
    return datetime(2020,1,1,h,m)

def calctimedelta(s,e):
    flag=True
    x=list(map(int,s.split(":")))
    y=list(map(int,e.split(":")))
    start=datetime(2020,1,1,x[0],x[1])
    end=datetime(2020,1,1,y[0],y[1])
    if start>end:
        flag=False
    return flag


# Create your views here.


# トップページ
class toppage(TemplateView):
    template_name = "top.html"

    def get(self, request, *args, **kwargs):
        # Person.objects.create(name="田中")
        # workers=Person.objects.all()
        context=super(toppage,self).get_context_data(**kwargs)
        context["xx"]=[k for k in range(20)]
        if "p" in request.GET:
            if request.GET["p"]=="logout":

                request.session.clear()
        # context["person"]=workers
        if not "username" in request.session:
            context["username"]="ログイン"
        else:
            context["username"]=request.session["username"]
        return render(self.request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        searchword=request.POST["word"]
        context = super(toppage, self).get_context_data(**kwargs)
        context["errormessage"]=""
        userid=""
        if "userid" in request.session:
            userid=request.session["userid"]
        users=User.objects.filter(name=searchword).exclude(primkey=userid)
        context["users"]=users
        return render(self.request,self.template_name,context)

from django.contrib.sessions.backends.db import SessionStore

class newview(TemplateView):
    template_name = "top.html"

    def post(self,request,*args,**kwargs):
        context=super(newview,self).get_context_data(**kwargs)
        name=request.POST["name"]
        Person.objects.create(name=name)
        context["message"]=name+"さんが追加されました"
        return render(self.request,self.template_name,context)


# ログインページ
class loginview(TemplateView):
    template_name = "login.html"
    def get(self,request,*args,**kwargs):
        context=super(loginview,self).get_context_data(**kwargs)
        # form=UserCreateForm(request.POST)
        # context["form"]=form
        return render(self.request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        username=request.POST["username"]
        password=request.POST["password"]
        context = super(loginview, self).get_context_data(**kwargs)
        context["errormessage"]=""
        # User.objects.create(name=username,password=password)
        # for i in User.objects.all():
        #     print(i.primkey)
        #     print(i.name)
        #     print(i.password)
        userinfo=User.objects.filter(name=username,password=password)
        if len(userinfo)==0:
            context["errormessage"]="該当のユーザーは存在しません"
            return render(self.request, self.template_name, context)
        else:
            User.objects.filter(name=username, password=password).update()
            request.session["userid"]=userinfo[0].primkey
            request.session["username"]=userinfo[0].name
            if "page" in request.session:
                nextpage=request.session["page"]
                response=redirect("/"+nextpage)
                request.session.pop("page")
            else:
                response=redirect("/")
            return response

# 新規登録ページ
class createuserview(TemplateView):
    template_name = "create.html"
    def get(self,request,*args,**kwargs):
        context=super(createuserview,self).get_context_data(**kwargs)
        # form=UserCreateForm(request.POST)
        # context["form"]=form
        return render(self.request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        username=request.POST["username"]
        password=request.POST["password"]
        context = super(createuserview, self).get_context_data(**kwargs)
        context["errormessage"]=""
        # 半角英数字判定↓
        validpasschecker = re.compile(r'^[a-zA-Z0-9]+$')
        # User.objects.create(name=username,password=password)
        # for i in User.objects.all():
        #     print(i.primkey)
        #     print(i.name)
        #     print(i.password)
        userinfo=User.objects.filter(name=username)
        if len(userinfo)!=0:
            context["errormessage"]="ユーザー名は既に使用されています。"
            return render(self.request, self.template_name, context)
        elif validpasschecker.match(password) is None:
            context["errormessage"]="パスワードは半角英数字のみ利用できます。"
            return render(self.request, self.template_name, context)
        elif len(password)<6:
            context["errormessage"]="パスワードは6文字以上で設定してください。"
            return render(self.request, self.template_name, context)
        else:
            User.objects.create(name=username,password=password)
            userinfo = User.objects.filter(name=username)
            request.session["userid"]=userinfo[0].primkey
            request.session["username"]=userinfo[0].name
            request.session.set_expiry(10)

            response=redirect("/")
            return response


# 会社情報
class ifboxview(TemplateView):
    template_name = "Kintai.html"
    def get(self,request,*args,**kwargs):
        context=super(ifboxview,self).get_context_data(**kwargs)
        # form=UserCreateForm(request.POST)
        # context["form"]=form
        return render(self.request,self.template_name,context)


# マイページ
class mypageview(TemplateView):
    template_name = "mypage.html"
    def get(self,request,*args,**kwargs):
        context=super(mypageview,self).get_context_data(**kwargs)
        # form=UserCreateForm(request.POST)
        # context["form"]=form
        # if not "username" in request.session:
        #     if "p" in request.GET:
        #         if request.GET["p"] == "mypage":
        #             request.session["page"]="mypage"
        if checklogin(request):
            response=redirect("/login")
            return response
        articles=Diaries.objects.filter(primkey=request.session["userid"])
        context["articles"]=articles
        return render(self.request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        context=super(mypageview,self).get_context_data(**kwargs)
        if "edit" in request.POST or "write" in request.POST:
            article=request.POST["confirmd"]
        else:
            article=request.POST["diary"]
        context["article"]=article
        if len(article)<=10:
            context["message"]="日記の内容は10文字以上入力してください"
            return render(self.request, self.template_name, context)
        elif "confirm" in request.POST:
            context["article"]=article
            return render(self.request, "diaryconfirm.html", context)
        elif "edit" in request.POST:
            context["writearticle"]=article
            return render(self.request, self.template_name, context)
        Diaries.objects.create(primkey=request.session["userid"],article=article)
        context["message"] = "投稿しました"
        articles=Diaries.objects.filter(primkey=request.session["userid"])
        context["articles"]=articles
        return render(self.request,self.template_name,context)


class allfriendview(TemplateView):
    template_name = "allfriend.html"
    def get(self,request,*args,**kwargs):
        # for i in range(220):
        #     UserFriends.objects.create(userid=request.session["userid"],friendid=User(primkey=7))
        if checklogin(request):
            response=redirect("/login")
            return response
        context=super(allfriendview,self).get_context_data(**kwargs)
        context["title"]="友達一覧"
        if "searchtitle" in request.GET:
            context["title"]="ユーザー一覧"
            context["pagetype"]="users"
        pagenum = 10
        userid=request.session["userid"]
        friendusers=UserFriends.objects.filter(userid=userid).select_related()
        lengs=len(friendusers)
        if lengs==0:
            context["message"]="友達は0人です"
            return render(self.request, self.template_name, context)
        pagenums=(lengs-1)%pagenum
        nowpage=1

        first=0
        last=0

        if "page" in request.GET:
            page=int(request.GET["page"])
            nowpage=page
            remainpage=lengs%pagenum
            if remainpage!=0:
                first=pagenum*page
                last=first+remainpage
            else:
                first=(page-1)*pagenum
                last=page*pagenum
        else:
            if lengs>=pagenum:
                last=pagenum
            else:
                last=lengs
        friendusers=friendusers[first:last]
        context["friendusers"]=friendusers
        context["pagenums"]=[k for k in range(1,pagenums+1)]
        context["nowpage"]=nowpage
        return render(self.request,self.template_name,context)

class friendpageview(TemplateView):
    template_name = "friendpage.html"
    def get(self,request,*args,**kwargs):
        context=super(friendpageview,self).get_context_data(**kwargs)
        if checklogin(request):
            response=redirect("/login")
            return response
        userid=request.session["userid"]
        friendid=int(request.GET["friendid"])
        context["friendid"]=friendid
        friendinfo=User.objects.filter(primkey=friendid)
        context["friendinfo"]=friendinfo[0]
        friendcheck=UserFriends.objects.filter(userid=userid,friendid=friendid)
        if len(friendcheck)==0:
            context["friendcheck"]=-1
        return render(self.request,self.template_name,context)

class sendmessageview(TemplateView):
    template_name = "sendmessage.html"
    postredirecturl="/message"
    def get(self,request,*args,**kwargs):
        context=super(sendmessageview,self).get_context_data(**kwargs)
        if checklogin(request):
            response=redirect("/login")
            return response
        redirecturl=getcontext(request,self.postredirecturl)
        friendid=int(request.GET["friendid"])
        friendinfo=User.objects.filter(primkey=friendid)
        context["friendinfo"]=friendinfo[0]
        mail=UserMessage.objects.filter(userid=friendid,friendid=request.session["userid"])
        context["mail"]=mail
        for i in mail:
            print(i.primkey)
        return render(self.request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        for i in request.GET:
            print(i)
        context=super(sendmessageview,self).get_context_data(**kwargs)
        message=request.POST["message"]
        userid=request.session["userid"]
        friendid=int(request.GET["friendid"])
        UserMessage.objects.create(userid=User(primkey=userid),friendid=User(primkey=friendid),message=message,)
        response=redirect(getcontext(request,self.postredirecturl))
        return response

class readmailview(TemplateView):
    template_name = "readmail.html"
    def get(self,request,*args,**kwargs):
        context=super(readmailview,self).get_context_data(**kwargs)
        if checklogin(request):
            response=redirect("/login")
            return response
        mailid=int(request.GET["mailid"])
        mail=UserMessage.objects.filter(primkey=mailid)
        context["mail"]=mail[0]
        return render(self.request,self.template_name,context)



# 管理者ログインチェック
def AdminLoginCheck(request):
    flag=False
    if "AdminUser" in request.session:
       flag=True
    return flag


# 管理画面
class AdminView(TemplateView):
    template_name = "KintaiFiles/KintaiAdmin.html"
    def get(self, request, *args, **kwargs):
        context=super(AdminView,self).get_context_data(**kwargs)
        print("hello")
        # AdminInformation.objects.create(adminid="admin",adminpass1="abc303",adminpass2="parrot3003",adminname="管理者")
        print("hello2")
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        return render(self.request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        ID=request.POST["ID"]
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]
        llst=AdminInformation.objects.filter(adminid=ID,adminpass1=pass1,adminpass2=pass2)
        if len(llst)==0:
            context = super(AdminView, self).get_context_data(**kwargs)
            context["errormessage"]="IDまたはパスワードのいずれかが間違っています"
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)
        else:
            name=llst[0].adminname
            request.session["AdminUser"]=name
            response=redirect("/administrator")
            return response

# 本日稼働中情報管理
class AdminAttendance(TemplateView):
    template_name = "KintaiFiles/AdminShutuTaikin.html"
    def get(self, request, *args, **kwargs):
        context=super(AdminAttendance,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        todayat=RunningInfo.objects.filter(attendancetime__date=date.today())
        context["todayat"]=todayat

        return render(self.request,self.template_name,context)

# 従業員情報管理
class AdminEmployee(TemplateView):
    template_name = "KintaiFiles/AdminEmployee.html"
    def get(self, request, *args, **kwargs):
        context=super(AdminEmployee,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        employees=EmployeeInfo.objects.all()

        context["employee"]=employees

        return render(self.request,self.template_name,context)

# 従業員新規追加
class NewEmployee(TemplateView):
    template_name = "KintaiFiles/NewEmployee.html"
    def get(self, request, *args, **kwargs):
        context=super(NewEmployee,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        return render(self.request,self.template_name,context)
    def post(self, request, *args, **kwargs):
        context = super(NewEmployee, self).get_context_data(**kwargs)
        ename=request.POST["ename"]
        loginid=request.POST["loginid"]
        llst=EmployeeInfo.objects.filter(employeename=ename)
        llst2=EmployeeInfo.objects.filter(loginid=loginid)

        if len(llst)>=1:
            context["message"]="従業員名は既に登録されています、別の名前を登録してください"
            return render(self.request,self.template_name,context)
        if len(ename)==0:
            context["message"]="名前を入力してください"
            return render(self.request,self.template_name,context)
        if len(loginid)<=3:
            context["message"]="ログインIDは4文字以上で設定してください"
            return render(self.request,self.template_name,context)
        if len(llst)>=1:
            context["message"]="そのログインIDは既に"+llst2[0].employeename+"さんに使用されています、別のIDを使用してください"
            return render(self.request,self.template_name,context)
        else:
            # パスワード作成
            import random
            passlen=random.randint(7,13)
            moji="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            mojilen=len(moji)
            newpass=""
            for i in range(passlen):
                newpass+=moji[random.randint(0,mojilen-1)]
            EmployeeInfo.objects.create(employeename=ename,loginid=loginid,loginidpass=newpass)
            context["registok"]=1
            context["password"]=newpass
            context["loginid"]=loginid
            context["ename"]=ename
            return render(self.request,self.template_name,context)

# 従業員情報編集
class EmployeeEdit(TemplateView):
    template_name = "KintaiFiles/AdminEmployeeEdit.html"
    def get(self, request, *args, **kwargs):
        context=super(EmployeeEdit,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)
        id=request.GET["id"]
        empuser=EmployeeInfo.objects.filter(primkey=id)[0]
        context["euser"]=empuser
        return render(self.request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        context = super(EmployeeEdit, self).get_context_data(**kwargs)
        prim=request.POST["prim"]
        name=request.POST["name"]
        loginid=request.POST["loginid"]
        password=request.POST["pass"]
        empuser=EmployeeInfo.objects.filter(primkey=prim)[0]
        context["euser"]=empuser
        if len(name)==0:
            context["message"]="名前を空白にすることはできません"
            return render(self.request,self.template_name,context)
        if len(password)<=5:
            context["message"]="パスワードは6文字以上で設定してください"
            return render(self.request,self.template_name,context)
        if len(loginid)<4:
            context["message"]="ログインIDは4文字以上で設定してください"
            return render(self.request,self.template_name,context)
        x=EmployeeInfo.objects.filter(loginid=loginid).exclude(primkey=prim)
        y=EmployeeInfo.objects.filter(employeename=name).exclude(primkey=prim)
        if len(x)>0:
            context["message"]="そのログインIDは既に使用されています。別の物を使用して下さい"
            return render(self.request,self.template_name,context)
        if len(y)>0:
            context["message"]="その名前は既に使われています。別の名前にしてください"
            return render(self.request,self.template_name,context)
        EmployeeInfo.objects.filter(primkey=prim).update(employeename=name,loginid=loginid,loginidpass=password)
        return redirect("/employee")

# 従業員の今月出勤情報
class EmployeeShukkin(TemplateView):
    template_name = "KintaiFiles/EmployeeShukkin.html"
    def get(self, request, *args, **kwargs):
        context=super(EmployeeShukkin,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)
        id=request.GET["id"]
        emprun=RunningInfo.objects.filter(attendancetime__year=date.today().year,attendancetime__month=date.today().month,employeeofrun=id).order_by("attendancetime")
        context["emprun"]=emprun
        context["nissu"]=len(emprun)
        context["name"]=EmployeeInfo.objects.filter(primkey=id)[0].employeename
        return render(self.request,self.template_name,context)

# お客様管理画面
class AdminCustomer(TemplateView):
    template_name = "KintaiFiles/AdminCustomer.html"
    def get(self, request, *args, **kwargs):
        context=super(AdminCustomer,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        customers=CustomerInfo.objects.filter(nowrunning=True)
        for i in customers:
            print(i)
        context["customers"]=customers

        return render(self.request,self.template_name,context)

# お客様新規登録
class NewCustomer(TemplateView):
    template_name = "KintaiFiles/NewCustomer.html"
    def get(self, request, *args, **kwargs):
        context=super(NewCustomer,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        return render(self.request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        context = super(NewCustomer, self).get_context_data(**kwargs)
        cusname=request.POST["customername"]
        llst=CustomerInfo.objects.filter(compname=cusname)

        if len(llst)>=1:
            context["message"]="お客様名は既に登録されています"
            return render(self.request,self.template_name,context)
        if len(cusname)<=2:
            context["message"]="会社名称は3文字以上で登録してください"
            return render(self.request,self.template_name,context)
        else:
            CustomerInfo.objects.create(compname=cusname)
            context["message"]="会社名:"+cusname+"を新規に追加しました"
            return redirect("/customer")



class AdminGenba(TemplateView):
    template_name = "KintaiFiles/AdminGenba.html"
    def get(self, request, *args, **kwargs):
        context=super(AdminGenba,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        today=date.today()
        year=today.year
        month=today.month

        runninggenba=RunningInfo.objects.filter(attendancetime__year=year,attendancetime__month=month).order_by("genbainfo")
        runninggenba=[k.genbainfo.primkey for k in runninggenba]
        genba=GenbaInfo.objects.all()
        runninggenba=[{"id":k.primkey,"name":k.genbaname} for k in genba if k.primkey in runninggenba]
        print(runninggenba)
        context["runninggenba"]=runninggenba
        return render(self.request,self.template_name,context)



# 稼働中の現場情報管理
class GenbaKanri(TemplateView):
    template_name = "KintaiFiles/KadouGenbaKanri.html"

    def get(self, request, *args, **kwargs):
        context = super(GenbaKanri, self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request, "KintaiFiles/KintaiAdminLogin.html", context)

        genba = GenbaInfo.objects.filter(nowrunning=True)
        context["genba"] = genba
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = super(GenbaKanri, self).get_context_data(**kwargs)
        genbaid=request.POST["genbaid"]
        stime=request.POST["stime"+str(genbaid)]
        ttime=request.POST["ttime"+str(genbaid)]
        if stime=="" or ttime=="":
            context["message"]="出勤時刻と退勤時刻は両方入力してください"
            genba = GenbaInfo.objects.filter(nowrunning=True)
            context["genba"] = genba
            return render(self.request, self.template_name, context)
        if not calctimedelta(stime,ttime):
            context["message"]="退勤時刻が出勤時刻よりも前になっています"
            genba = GenbaInfo.objects.filter(nowrunning=True)
            context["genba"] = genba
            return render(self.request, self.template_name, context)
        x=list(map(int,stime.split(":")))
        y=list(map(int,ttime.split(":")))
        stime=datetime(2020,1,1,x[0],x[1]).astimezone(timezone('Asia/Tokyo'))
        ttime=datetime(2020,1,1,y[0],y[1])
        print(stime,ttime)

        GenbaInfo.objects.filter(primkey=genbaid).update(start=stime,end=ttime)
        x=GenbaInfo.objects.filter(primkey=genbaid)[0]
        print(x.start)
        print(x.end.astimezone())
        return redirect("/genbakanri")



# 現場別稼働状況
class GenbaBetu(TemplateView):
    template_name = "KintaiFiles/GenbaBetuKado.html"

    def get(self, request, *args, **kwargs):
        context = super(GenbaBetu, self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request, "KintaiFiles/KintaiAdminLogin.html", context)
        id=request.GET["id"]
        context["genbaname"]=GenbaInfo.objects.filter(primkey=id)[0].genbaname
        kado=[]
        year=date.today().year
        month=date.today().month
        lastdate=calendar.monthrange(year,month)[1]
        genbainfo=GenbaInfo.objects.filter(primkey=id)[0]
        e=genbainfo.end.astimezone()
        print(e.hour)
        hour=e.hour
        minute=e.minute
        sums=0
        for day in range(1,lastdate+1):
            today=datetime(year,month,day,hour,minute).astimezone(timezone('Asia/Tokyo'))
            x={"day":day}
            d = RunningInfo.objects.filter(attendancetime__year=year,attendancetime__month=month,attendancetime__day=day,genbainfo=id)
            # if len(d)>=1:
            #     print(d[1].leavetime)
            #     print(d[1].leavetime.hour)
            #     print(d[1].leavetime.astimezone(timezone('Asia/Tokyo')).hour)
            #     print(d[1].leavetime.astimezone().hour)


            # sumzangyo=sum([(k.leavetime.astimezone()-today).seconds for k in d if k.leavetime.astimezone(timezone('Asia/Tokyo'))>today])

            leng=len(d)
            sums+=leng
            x["ninku"]=leng
            names=",".join([k.employeeofrun.employeename for k in d])
            x["names"]=names
            kado.append(x)
            # x["sumzangyo"]=sumzangyo
        context["kado"] = kado
        context["kadoninku"]=sums
        return render(self.request, self.template_name, context)

#現場新規登録
class NewGenba(TemplateView):
    template_name = "KintaiFiles/NewGenba.html"
    def get(self, request, *args, **kwargs):
        context = super(NewGenba, self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request, "KintaiFiles/KintaiAdminLogin.html", context)
        companies=CustomerInfo.objects.filter(nowrunning=True)
        context["companies"]=companies
        return render(self.request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        context = super(NewGenba, self).get_context_data(**kwargs)
        genbaname=request.POST["genbaname"]
        compid=request.POST["compid"]
        stime=request.POST["stime"]
        ttime=request.POST["ttime"]
        if compid=="none":
            llst = GenbaInfo.objects.filter(genbaname=genbaname)
        else:
            llst=GenbaInfo.objects.filter(genbaname=genbaname,compofgenba=CustomerInfo(primkey=compid))
        companies=CustomerInfo.objects.filter(nowrunning=True)
        context["companies"]=companies

        if stime=="" or ttime=="":
            context["message"]="出勤時刻と退勤時刻は両方入力してください"
            return render(self.request, self.template_name, context)
        if not calctimedelta(stime,ttime):
            context["message"]="退勤時刻が出勤時刻よりも前になっています"
            return render(self.request, self.template_name, context)

        if len(llst)>=1:
            context["message"]="現場は既に登録されています"
            return render(self.request,self.template_name,context)
        if len(genbaname)<=1:
            context["message"]="現場名称は2文字以上で登録してください"
            return render(self.request,self.template_name,context)
        else:
            start=makedatetime(stime)
            end=makedatetime(ttime)
            if compid=="none":
                GenbaInfo.objects.create(genbaname=genbaname,start=start,end=end)
            else:
                GenbaInfo.objects.create(genbaname=genbaname,start=start,end=end,compofgenba=CustomerInfo(primkey=compid))
            context["message"]="現場名:"+genbaname+"を新規に追加しました"
            return redirect("/genbakanri")

# 過去の現場
class PastGenba(TemplateView):
    template_name = "KintaiFiles/PastGenba.html"
    def get(self, request, *args, **kwargs):
        context = super(PastGenba, self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request, "KintaiFiles/KintaiAdminLogin.html", context)
        genba = GenbaInfo.objects.filter(nowrunning=False)
        context["genba"]=genba
        return render(self.request, self.template_name, context)

class AdminEdit(TemplateView):
    template_name = "KintaiFiles/AdminKanri.html"
    def get(self, request, *args, **kwargs):
        context=super(AdminEdit,self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request,"KintaiFiles/KintaiAdminLogin.html",context)

        return render(self.request,self.template_name,context)


# 情報の追加など
class InfoChange(TemplateView):
    template_name = "KintaiFiles/KadouGenbaKanri.html"

    def get(self, request, *args, **kwargs):
        context = super(InfoChange, self).get_context_data(**kwargs)
        if not AdminLoginCheck(request):
            return render(self.request, "KintaiFiles/KintaiAdminLogin.html", context)

        action=request.GET["action"]
        id=request.GET["id"]

        if action=="delete":
            GenbaInfo.objects.filter(primkey=id).update(nowrunning=False)
            context["message"] = "稼働中の現場から外しました"
            return redirect("/genbakanri")

        elif action=="run":
            GenbaInfo.objects.filter(primkey=id).update(nowrunning=True)
            return redirect("/pastgenba")

# 従業員ログインチェック
def EmpLoginCheck(request):
    flag=False
    if "empuserid" in request.session:
        flag=True
    return flag


# 勤怠ログイン画面
class KintaiLogin(TemplateView):
    template_name = "KintaiFiles/KintaiLogin.html"
    def get(self, request, *args, **kwargs):
        if EmpLoginCheck(request):
            return redirect("/kintai")
        context=super(KintaiLogin,self).get_context_data(**kwargs)
        return render(self.request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        context=super(KintaiLogin,self).get_context_data(**kwargs)
        loginid=request.POST["id"]
        loginpas=request.POST["password"]
        user=EmployeeInfo.objects.filter(loginid=loginid,loginidpass=loginpas)
        if len(user)==0:
            context["message"]="IDまたはパスワードが違います"
            return render(self.request,self.template_name,context)
        user=user[0]
        request.session["empuserid"]=user.primkey
        request.session["username"]=user.employeename
        return redirect("/kintai")



# 従業員別勤怠入力画面
class KintaiView(TemplateView):
    template_name = "KintaiFiles/Kintai.html"
    def get(self, request, *args, **kwargs):
        context=super(KintaiView,self).get_context_data(**kwargs)
        if not EmpLoginCheck(request):
            return redirect("/emplogin")
        userid=request.session["empuserid"]
        user=EmployeeInfo.objects.filter(primkey=userid)[0]
        if user.jobstatus:
            lastrun=RunningInfo.objects.filter(employeeofrun=EmployeeInfo(primkey=userid))
            if lastrun.last().leavetime!=None :
                EmployeeInfo.objects.filter(primkey=userid).update(jobstatus=False)
                genba = GenbaInfo.objects.filter(nowrunning=True)
                context["genba"] = genba
                context["empuser"] = EmployeeInfo.objects.filter(primkey=userid)[0]
                return render(self.request, self.template_name, context)
            lastrun=lastrun.last()
            userstime=lastrun.attendancetime
            starttime=lastrun.genbainfo.start
            endtime=lastrun.genbainfo.end
            workingtime=endtime-starttime
            calcus=makedobject(userstime)
            calcgs=makedobject(starttime)
            if calcus!=calcgs:
                userstime-=calcus-calcgs

            userendtime=userstime+workingtime

            if (userendtime+timedelta(0,10)).astimezone()<(datetime.now()).astimezone() and (lastrun.attendancetime+timedelta(0,10)).astimezone()<datetime.now().astimezone():
                lastprim=lastrun.primkey
                RunningInfo.objects.filter(primkey=lastprim).update(leavetime=userendtime)
                EmployeeInfo.objects.filter(primkey=userid).update(lastgenba=lastrun.genbainfo.primkey,jobstatus=False)
                context["message"]=str(lastrun.attendancetime.day)+"日の"+lastrun.genbainfo.genbaname+"の現場において退勤打刻の押し忘れがありました。自動で定時退勤にしています。\n退勤時刻を修正する場合は出勤状況確認から該当日時の修正をしてください。"
                genba = GenbaInfo.objects.filter(nowrunning=True)
                context["genba"] = genba
            else:
                context["site"]=GenbaInfo.objects.filter(primkey=user.lastgenba)[0].genbaname
        else:
            genba=GenbaInfo.objects.filter(nowrunning=True)
            context["genba"]=genba
        context["empuser"]=EmployeeInfo.objects.filter(primkey=userid)[0]
        return render(self.request,self.template_name,context)


    def post(self,request,*args,**kwargs):
        if not EmpLoginCheck(request):
            return redirect("/emplogin")
        userid=request.session["empuserid"]
        status=request.POST["status"]
        if status=="sk":
            genbaid=request.POST["genbaid"]
            nowtime=datetime.now()
            genbainfo=GenbaInfo.objects.filter(primkey=genbaid)[0]
            starttime=genbainfo.start
            sg=makedobject(starttime).astimezone()
            su=makedobject(nowtime).astimezone()
            print(sg,su,"タオ")
            if sg>su:
                nowtime+=(sg-su)

            else:
                m=nowtime.minute
                if m%15!=0:
                    x=15-m%15
                    nowtime+=timedelta(0,x*60)
                print(nowtime)
                nowtime=datetime(nowtime.year,nowtime.month,nowtime.day,nowtime.hour,nowtime.minute)

            RunningInfo.objects.create(employeeofrun=EmployeeInfo(primkey=userid),genbainfo=GenbaInfo(primkey=genbaid),attendancetime=nowtime)
            EmployeeInfo.objects.filter(primkey=userid).update(jobstatus=True,lastgenba=genbaid)
        else:
            lastrun=RunningInfo.objects.filter(employeeofrun=EmployeeInfo(primkey=userid))
            nowtime=datetime.now()
            m=nowtime.minute
            nowtime-=timedelta(0,m%15*60)
            nowtime = datetime(nowtime.year, nowtime.month, nowtime.day, nowtime.hour, nowtime.minute)
            lastprim=lastrun.last().primkey
            RunningInfo.objects.filter(primkey=lastprim).update(leavetime=nowtime)
            EmployeeInfo.objects.filter(primkey=userid).update(jobstatus=False)

        return redirect("/kintai")

# 従業員別パスワード編集
class EmployeePassEdit(TemplateView):
    template_name = "KintaiFiles/EmpPassEdit.html"
    def get(self, request, *args, **kwargs):
        context=super(EmployeePassEdit,self).get_context_data(**kwargs)
        if not EmpLoginCheck(request):
            return redirect("/emplogin")
        userid=request.session["empuserid"]
        user=EmployeeInfo.objects.filter(primkey=userid)[0]
        context["empuser"]=user
        return render(self.request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        context=super(EmployeePassEdit,self).get_context_data(**kwargs)
        userid=request.session["empuserid"]
        user=EmployeeInfo.objects.filter(primkey=userid)[0]
        context["empuser"]=user
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]
        if pass1!=pass2:
            context["message"]="パスワードが一致しません"
            return render(self.request,self.template_name,context)
        if len(pass1)<6:
            context["message"]="パスワードは6文字以上で入力してください"
            return render(self.request,self.template_name,context)
        EmployeeInfo.objects.filter(primkey=userid).update(loginidpass=pass1)
        return redirect("/kintai")

# 従業員出勤情報
class EmployeeThisMonth(TemplateView):
    template_name = "KintaiFiles/EmpThisMonth.html"
    def get(self, request, *args, **kwargs):
        context=super(EmployeeThisMonth,self).get_context_data(**kwargs)
        if not EmpLoginCheck(request):
            return redirect("/emplogin")
        userid=request.session["empuserid"]
        user=EmployeeInfo.objects.filter(primkey=userid)[0]
        context["empuser"]=user
        year=date.today().year
        month=date.today().month
        context["month"]=month
        emprun=RunningInfo.objects.filter(attendancetime__year=year,attendancetime__month=month,employeeofrun=userid).order_by("attendancetime")
        context["emprun"]=emprun
        return render(self.request,self.template_name,context)

class ChangeInfoEmp(TemplateView):
    def get(self, request, *args, **kwargs):
        context=super(ChangeInfoEmp,self).get_context_data(**kwargs)
        if not EmpLoginCheck(request):
            return redirect("/emplogin")

        userid=request.session["empuserid"]
        action=request.GET["action"]

        if action=="delshukkin":
            id = request.GET["id"]
            RunningInfo.objects.filter(primkey=id).delete()
            return redirect("/empthismonth")
        if action=="logout":
            request.session.clear()
            return redirect("/kintai")


    def post(self,request,*args,**kwargs):
        context=super(ChangeInfoEmp,self).get_context_data(**kwargs)
        if not EmpLoginCheck(request):
            return redirect("/emplogin")
        userid=request.session["empuserid"]
        id=request.POST["id"]
        p = RunningInfo.objects.filter(primkey=id).first()
        t = request.POST["ltime" + str(id)]
        if t == "":
            year = date.today().year
            month = date.today().month
            context["message"] = "時間を入力してください"
            emprun = RunningInfo.objects.filter(attendancetime__year=year, attendancetime__month=month,
                                                employeeofrun=userid).order_by("attendancetime")
            context["emprun"] = emprun
            return render(self.request, "KintaiFiles/EmpThisMonth.html", context)
        year = p.attendancetime.year
        month = p.attendancetime.month
        day = p.attendancetime.day
        t = list(map(int, t.split(":")))
        t = datetime(year, month, day, t[0], t[1])
        RunningInfo.objects.filter(primkey=id).update(leavetime=t)
        return redirect("/empthismonth")