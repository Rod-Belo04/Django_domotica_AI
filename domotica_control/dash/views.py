from django.shortcuts import render

def home(request):
    return render(request, 'dash/home.html')
def post(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        if field == 'thermo':
            temp = request.POST.get('temp')