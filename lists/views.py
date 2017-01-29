from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# to pass the test, we add a if statement providing a different code path for the post request.
def home_page(request):
	return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', ''),})
	#this will give an unexpexted failure, we broke the code path where there is no post request. 
