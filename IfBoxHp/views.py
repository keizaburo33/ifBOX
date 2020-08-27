from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.sessions import *

from IfBoxHp.models import *
from IfBoxHp.forms import *
import re

print(200)

# Create your views here.


# トップページ
class toppage(TemplateView):
    template_name = "top.html"

    def get(self, request, *args, **kwargs):
        # Person.objects.create(name="田中")
        # workers=Person.objects.all()
        context=super(toppage,self).get_context_data(**kwargs)
        context["xx"]=[k for k in range(20)]
        print(request.GET)
        if "p" in request.GET:
            print("kjl")
            if request.GET["p"]=="logout":

                request.session.clear()
        # context["person"]=workers
        if not "username" in request.session:
            context["username"]="ログイン"
        else:
            context["username"]=request.session["username"]
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
            request.session["userid"]=userinfo[0].primkey
            request.session["username"]=userinfo[0].name
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
            response=redirect("/")
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


