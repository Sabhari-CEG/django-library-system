from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import UserForm
from django.contrib.auth import authenticate,login
from django.views.generic import View

# # Create your views here.
# def index(request):
#     all_collection = Collection.objects.all()
#     context = {
#         "all_collection" : all_collection
#     }
#     print(context)
#     return render(request, "genre\\genretemplate.html", context)

class index(generic.ListView):
    template_name = "genre\genretemplate.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Collection.objects.all()

# def details(request, genre_id):
#     selected_collection = Collection.objects.get(pk=genre_id)
#     selected_piece = Piece.objects.filter(collection=selected_collection)
#     context = {
#         "selected_piece" : selected_piece
#     }
#     return render(request,"genre\\detailtemplate.html",context)

class details(generic.DetailView):
    model = Collection
    template_name = "genre\detailtemplate.html"

class UserformView(View):
    form_class = UserForm
    template_name = 'genre\\formtemplate.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})
    
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            newuser = authenticate(username=username,password=password)

            if newuser is not None:
                if newuser.is_active:
                    login(request,newuser)
                    return redirect("/genre")
                
        return render(request,self.template_name,{'form' : form})

