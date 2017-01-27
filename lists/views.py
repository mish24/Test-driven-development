from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request): #notice that when you made this error, the typeError was that home_page() took no argument
	return render(request, 'home.html')
