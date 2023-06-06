from django.http import HttpResponse
from django.shortcuts import render ,redirect



def index(request):
    return redirect("/ecom/")
    # return render(request,'main.html')