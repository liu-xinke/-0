from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

def index_views(request):
    if request.method == 'POST':
        name = request.POST['uname']
        if not name:
            return HttpResponseRedirect('/')
        path = '/player/' + name
        return HttpResponseRedirect(path)
    else:
        return render(request,'index.html')

def redirect_views(request):
    return HttpResponseRedirect('/')
