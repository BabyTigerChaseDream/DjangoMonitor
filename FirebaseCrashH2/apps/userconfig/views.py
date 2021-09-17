from django.shortcuts import render
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.http import HttpResponse
from .models import Config

'''
 	id            
 	team          
 	team_id       
 	contacts      
 	slack_channel 
 	email_address 
 	crash_count   
 	total_user    
 	files         
 	keywords      
 	tags          
 	start_date    
 	end_date 
'''

'''
Config = [
     
	{
		'author': 'Jia',
		'title': 'Blog 1',
		'content': 'first Config',
		'date_Configed':'Sep/16/2020'
	},
	{
		'author': 'Guo',
		'title': 'Blog 2',
		'content': 'second Config',
		'date_Configed':'Sep/18/2020'
	}
]
'''

def home(request):
	context = {
		'configs':Config.objects.all()
	}
	#return HttpResponse('<h1>Userconfig Home</h1>')
	return render(request, 'userconfig/home.html', context)

class ConfigListView(ListView):
	model = Config
	# defaule view looking for :
	# <app>/<model>_<viewtype>.htm
	template_name = 'userconfig/home.html'
	context_object_name = 'Configs'
	ordering = ['-date_Configed']

class ConfigDetailView(DetailView):
	model = Config

class ConfigCreateView(CreateView):
	model = Config
	fields = ['team','team_id','start_date','end_date','slack_channel','email_address','contacts','crash_count','total_user','files','keywords','tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	success_url = '/'

class ConfigUpdateView(UpdateView):
	model = Config
	fields = ['team','team_id','start_date','end_date','slack_channel','email_address','contacts','crash_count','total_user','files','keywords','tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	success_url = '/'

class ConfigDeleteView(DeleteView):
	model = Config
	success_url = '/'

def about(request):
	return render(request, 'userconfig/about.html', {'title':'About'})
