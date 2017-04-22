from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the dashboard index.")
    return render_to_response('dashboard_main.html')
