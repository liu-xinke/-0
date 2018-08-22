from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

def help_1_views(request):
    return render(request,'help_1.html')
def help_2_views(request):
    return render(request,'help_2.html')
def help_3_views(request):
    return render(request,'help_3.html')
def help_4_views(request):
    return render(request,'help_4.html')
def help_5_views(request):
    return render(request,'help_5.html')
def redirect_views(request):
    return HttpResponseRedirect('/help/1/')
