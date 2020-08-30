from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.sessions import *
from django.db.models import Q

from IfBoxHp.models import *
from IfBoxHp.forms import *
import re


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
                response=redirect("/mypage")
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
    template_name = "ifboxtop.html"
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
        if not "username" in request.session:
            if "p" in request.GET:
                if request.GET["p"] == "mypage":
                    request.session["page"]="mypage"
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

        pagenum = 10
        context=super(allfriendview,self).get_context_data(**kwargs)
        userid=request.session["userid"]
        friendusers=UserFriends.objects.filter(userid=userid).select_related()
        context["friendusers"]=friendusers
        lengs=len(friendusers)
        if lengs==0:
            context["message"]="友達は0人です"
            return render(self.request, self.template_name, context)
        pagenums=(lengs-1)%pagenum
        nowpage=1

        if "page" in request.GET:
            page=int(request.GET["page"])
            nowpage=page
            remainpage=lengs%pagenum
            if remainpage!=0:
                x=[pagenum*page+k for k in range(remainpage)]
            else:
                x=[k for k in range((page-1)*pagenum,page*pagenum)]
        else:
            if lengs>=pagenum:
                x=[k for k in range(pagenum)]
            else:
                x=[k for k in range(lengs)]
        context["x"]=x
        context["pagenums"]=[k for k in range(1,pagenums+1)]
        context["nowpage"]=nowpage
        return render(self.request,self.template_name,context)
