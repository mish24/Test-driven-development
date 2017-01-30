from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
# to pass the test, we add a if statement providing a different code path for the post request.
def home_page(request):
	return render(request, 'home.html')

def view_list(request):
	items = Item.objects.all()
	context = {'items': items,}
	template_used = 'list.html'
	return render(request, template_used , context)

def new_list(request):
	Item.objects.create(text= request.POST['item_text'])
	return redirect('/lists/the-only-list-in-the-world/')
