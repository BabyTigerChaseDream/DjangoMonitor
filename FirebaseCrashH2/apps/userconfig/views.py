from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django import forms

from .filters import UserConfigFilter

from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
#from django.http import HttpResponse
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
	#fields = ['team','team_id','start_date','end_date','slack_channel','email_address','contacts','crash_count','total_user','files','keywords','tags']
	#fields = ('team','slack_channel','email_address','crash_count','total_user','files','keywords')
	fields = ('team','slack_channel','email_address','crash_count','total_user','files','keywords')

	# get form and update required/optional fields 
	def get_form(self, form_class=None):
		form = super(ConfigCreateView, self).get_form(form_class)
		# team required
		#form.fields['team'].required = False
		form.fields['slack_channel'].required = False
		form.fields['email_address'].required = False
		form.fields['files'].required = False
		form.fields['keywords'].required = False

		return form

	def form_valid(self, form):
		'''
		## assignd default to items below:
		## dates: time slot
		#start_date = get_object_or_404(Config, slug=self.kwargs['start_date'])
		#form.instance.start_date = timezone.now()-timezone.timedelta(days=15)
		#threashold:  crashes / users
		#crash_count = get_object_or_404(Config, slug=self.kwargs['crash_count'])
		form.instance.crash_count = 50 
		'''

		# retrieve user input data 
		team = form.cleaned_data.get('team', 'anonymous team')
		slack_channel= form.cleaned_data.get('slack_channel', None)
		email_address= form.cleaned_data.get('email_address', None)
		files= form.cleaned_data.get('files', None)
		keywords= form.cleaned_data.get('keywords', None)

		messages.info(self.request, "[Debug] team:{team}, slack_channel:{slack_channel}, \
						email_address:{email_address}, files:{files}, keywords:{keywords} " \
							.format(team=team,slack_channel=slack_channel,email_address=email_address,files=files,keywords=keywords))
		messages.info(self.request, "[Debug Type] slack_channel:{slack_channel}, \
						email_address:{email_address}, files:{files}, keywords:{keywords} " \
							.format(slack_channel=type(slack_channel),email_address=type(email_address),files=type(files),keywords=keywords))
							
		'''
		messages.info(self.request, "[Debug Len] slack_channel:{slack_channel}, \
						email_address:{email_address}, files:{files}, keywords:{keywords} " \
							.format(slack_channel=len(slack_channel),email_address=len(email_address),files=len(files),keywords=len(keywords))
		'''
		##### slack and email logic check ##### 	
		# 1) need at least one 
		if (not len(slack_channel)) and (not len(email_address)):
			messages.error(self.request, "At least one channel required to receive info: slack/email ")
			return redirect('config-create')

		# 2) need at least one 
		# 2.1) email format 
		# TODO : email regex check 
		if email_address:
			if (not '@booking.com' in email_address):
				messages.error(self.request, "Please check your email: is it booking internal email ?")
				return redirect('config-create')
			else:
				pass
				#return redirect('userconfig-home-with-filter')
		'''
		# 2.2) slack format 
		# TODO : slack check  
		if slack_channel:
			if (not 'slack?' in slack_channel):
				messages.error(self.request, "Please check your slack format")
				return redirect('config-create')
			else:
				#return redirect('userconfig-home-with-filter')

		'''	
		############################################################

		if (not files) and (not keywords):
			messages.error(self.request, "Fill in at least one of files/keywords")
			#return redirect('config-create') 
		else:
			#return super(ConfigCreateView, self).form_valid(form)
			messages.success(self.request, 'Config Successfully created for {team}!'.format(team=team))
			#return redirect('userconfig-home-with-filter')

		# must save it !!!
		self.object = form.save()
		return redirect('userconfig-home-with-filter')
	success_url = '/'

class ConfigUpdateView(UpdateView):
	model = Config
	fields = ['team','team_id','start_date','end_date','slack_channel','email_address','contacts','crash_count','total_user','files','keywords','tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	success_url = '/'

'''
class ConfigTeamView(ListView):
    model = Config
    template_name = 'userconfig/config_team.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'config'
    paginate_by = 5

    def get_queryset(self):
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Config.objects.filter(team_id=team_id).order_by('-date_posted')
'''

class ConfigDeleteView(DeleteView):
	model = Config
	success_url = '/'

def crashlist(request):
	return render(request, 'userconfig/crashlist.html', {'title':'Crash List'})


def Filters(request):
    userconfig_list = Config.objects.all()
    userconfig_filter = UserConfigFilter(request.GET, queryset=userconfig_list)
    return render(request, 'userconfig/userconfig_filter.html', {'filter': userconfig_filter, 'configs':userconfig_list})
