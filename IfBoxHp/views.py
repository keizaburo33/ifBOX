from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.sessions import *
from django.db.models import Q

from IfBoxHp.models import *
from IfBoxHp.forms import *
import re


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
    template_name = "ifbox/ifboxtop.html"
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
