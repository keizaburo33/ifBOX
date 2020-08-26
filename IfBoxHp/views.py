from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.sessions import *

from IfBoxHp.models import *
from IfBoxHp.forms import *

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

# 会社情報
class ifboxview(TemplateView):
    template_name = "ifboxtop.html"
    def get(self,request,*args,**kwargs):
        context=super(ifboxview,self).get_context_data(**kwargs)
        # form=UserCreateForm(request.POST)
        # context["form"]=form
        return render(self.request,self.template_name,context)

