from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
# to pass the test, we add a if statement providing a different code path for the post request.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text = request.POST['item_text'])
		return redirect('/')
		
	items = Item.objects.all()
	context = {'items': items,}
	
	return render(request, 'home.html', context)
