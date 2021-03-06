from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
# to pass the test, we add a if statement providing a different code path for the post request.
def home_page(request):
	return render(request, 'home.html')


def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' %(list_.id,))

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' %(list_.id,))

def view_list(request, list_id):
	list_ = List.objects.get(id= list_id)
	return render(request, 'list.html', {'list': list_})

