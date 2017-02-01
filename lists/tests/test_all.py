from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string


from lists.models import Item, List

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpResponse()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content) #you made an error by writing contents. check and improve. it would then give an assertionerror and not an attribute error
		#self.assertTrue(response.content.endswith(b'</html>'))
		#we did this because sometimes there's a problem with the text editor
		self.assertTrue(response.content.strip().endswith(b'</html>'))
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		#decode converts response.content into the unicode string, which allows us to compare string with strings. 

#now that one class test works, lets create one more test to see whether the right template is rendered or not

		


class ListViewTest(TestCase):
	
		
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' %(list_.id,))
		self.assertTemplateUsed(response, 'list.html')
		
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		
		response = self.client.get('/lists/%d/' %(correct_list.id,))
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')
		
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' %(correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)
#for the new list item entry, we would like to use the django test client
class NewListItem(TestCase):
	
	def test_saving_a_post_request(self):
		data = {'item_text': 'A new list item',}
		self.client.post('/lists/new', data)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_to_the_correct_url_after_post(self):
		data = {'item_text': 'A new list item',}
		new_list = List.objects.create()
		response = self.client.post('/lists/new', data)
		self.assertEqual(response.status_code, 302)
		#self.assertRedirects(response, '/lists/%d/' %(new_list.id,))
		
class NewItemTest(TestCase):
	
	def test_can_save_a_post_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		data = {'item_text': 'A new list item',}
		
		self.client.post('/lists/%d/add_item' %(correct_list.id), data)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		self.assertEqual(new_item.list, correct_list)
		
	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		data = {'item_text' : 'A new item for the list',}
		
		response = self.client.post('/lists/%d/add_item' %(correct_list.id), data)
		self.assertRedirects(response, '/lists/%d/' %(correct_list.id,))

class NewListTest(TestCase):
	
	def test_can_save_a_post_request(self):
		data = {'item_text' : 'A new list item',}
		self.client.post('/lists/new', data)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_post(self):
		data = {'item_text': 'A new list item',}
		response = self.client.post('/lists/new', data)
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' %(new_list.id,))

class ListItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List()
		#we create an object of the type list
		list_.save()
		#we have to save it as well
		
		first_item = Item()
		#the first item is an instance of the type item
		first_item.text = 'A test text for the ListItemModel'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		#the second item is also of the type item object
		second_item.text = 'A second text for the ListItemModel'
		second_item.list = list_
		#both belong to the same list
		second_item.save()
		#do not forget to save the object
		
		#now, we try to retrive the list we just created. Note that this is going to be the topmost list
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		#it has to be equal to the list we manually created for our work
		
		#next, let us try to compare the items we added to the lists
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2) #you saved 2 items, right?
		
		#next, let us try to compare whether the objects we entered as the items are the similar ones or not
		first_item_saved = saved_items[0]
		second_item_saved = saved_items[1]
		#we manually try to compare whether the text we entered is the same which is retrieved by the objects or not
		self.assertEqual(first_item_saved.text, 'A test text for the ListItemModel')
		self.assertEqual(second_item_saved.text, 'A second text for the ListItemModel')
		self.assertEqual(first_item_saved.list, list_)
		self.assertEqual(second_item_saved.list, list_)
		
