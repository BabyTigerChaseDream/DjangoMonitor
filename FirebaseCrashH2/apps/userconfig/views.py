from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crispy_forms.helper import FormHelper
from .filters import UserConfigFilter

from .models import Config, Crashissues

from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
#from django.http import HttpResponse

import django_tables2 as tables

def home(request):
	context = {
		'configs':Config.objects.all()
	}
	#return HttpResponse('<h1>Userconfig Home</h1>')
	return render(request, 'userconfig/home.html', context)

'''
class ConfigListView(ListView):
	model = Config
	# defaule view looking for :
	# <app>/<model>_<viewtype>.htm
	template_name = 'userconfig/home.html'
	context_object_name = 'configs'
	paginate_by = 2
'''
class ConfigDetailView(DetailView):
	model = Config

class ConfigCreateView(CreateView):
	model = Config
	fields = ('team','platform','slack_channel','email_address','crash_count','total_user','files','keywords')
	def __init__(self, *args, **kwargs):
		super(ConfigCreateView, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-horizontal'
		self.helper.help_text_inline = True	
	'''
	class Meta:
		model = Config
		fields=['slack_channel']
		labels={'slack_channel':'Slack channel of your team'}
		help_texts={'slack_channel':'Your slackID'}
        #help_texts={'slack_channel':"Enter Your slack ID"}
	'''

	# get form and update required/optional fields 
	def get_form(self, form_class=None):
		form = super(ConfigCreateView, self).get_form(form_class)

		# team required
		form.fields['team'].widget=forms.TextInput(attrs={'placeholder': 'name your config','size':'18'}) 
		
		form.fields['slack_channel'].required = False
		form.fields['slack_channel'].widget=forms.TextInput(attrs={'placeholder': '#slack_channel'})

		form.fields['email_address'].required = False
		form.fields['email_address'].widget=forms.TextInput(attrs={'placeholder': '<user>@booking.com'})

		form.fields['crash_count'].required = False
		form.fields['crash_count'].widget=forms.NumberInput(attrs={'placeholder': 'minimum crash occurence'})

		form.fields['total_user'].required = False
		form.fields['total_user'].widget=forms.NumberInput(attrs={'placeholder': 'minimum users affected'})

		form.fields['files'].required = False
		form.fields['files'].widget=forms.TextInput(attrs={'placeholder': 'files to monitor on crashes(split by \',\')','size':'50'})

		form.fields['keywords'].required = False
		form.fields['keywords'].widget=forms.TextInput(attrs={'placeholder': 'monitor crashes based on keywords filled in,split by \',\'','size':'50'})

		return form

	def form_valid(self, form):
		# retrieve user input data 
		team = form.cleaned_data.get('team', 'anonymous team')
		slack_channel= form.cleaned_data.get('slack_channel', None)
		email_address= form.cleaned_data.get('email_address', None)
		files= form.cleaned_data.get('files', None)
		keywords= form.cleaned_data.get('keywords', None)

		'''
		messages.info(self.request, "[Debug] team:{team}, slack_channel:{slack_channel}, \
						email_address:{email_address}, files:{files}, keywords:{keywords} " \
							.format(team=team,slack_channel=slack_channel,email_address=email_address,files=files,keywords=keywords))
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
			return redirect('config-create') 
		else:
			#return super(ConfigCreateView, self).form_valid(form)
			messages.success(self.request, 'Config Successfully created for {team}!'.format(team=team))

		# must save it !!!
		self.object = form.save()
		return redirect('userconfig-home-with-filter')
	success_url = '/'

class ConfigUpdateView(UpdateView):
	model = Config
	fields = ('team','platform','timeslot','end_date','slack_channel','email_address','crash_count','total_user','files','keywords','tags')
	'''
	def get_object(self):
		return self.model.objects.get(pk=self.request.GET.get('id')) 
	'''

	# get form and update required/optional fields 
	def get_form(self, form_class=None):
		form = super(ConfigUpdateView, self).get_form(form_class)
		# team required
		#form.fields['id'].widget.attrs['readonly'] = True
		form.fields['slack_channel'].required = False
		form.fields['email_address'].required = False
		form.fields['files'].required = False
		form.fields['keywords'].required = False

		return form
	def form_valid(self, form):
		# retrieve user input data 
		team = form.cleaned_data.get('team', 'anonymous team')
		slack_channel= form.cleaned_data.get('slack_channel', None)
		email_address= form.cleaned_data.get('email_address', None)
		files= form.cleaned_data.get('files', None)
		keywords= form.cleaned_data.get('keywords', None)

		#config_id = Config.objects.get('id')
		'''
		messages.info(self.request, "[Debug] team:{team}, slack_channel:{slack_channel}, \
						email_address:{email_address}, files:{files}, keywords:{keywords} " \
							.format(team=team,slack_channel=slack_channel,email_address=email_address,files=files,keywords=keywords))
		'''
		##### slack and email logic check ##### 	
		# 1) need at least one 
		if (not len(slack_channel)) and (not len(email_address)):
			messages.error(self.request, "At least one channel required to receive info: slack/email ")
			print('[JIAJIAJIA]',self.request.get_full_path, '[JIAPATH]',self.request.path)
			return redirect(self.request.path)

		# 2) need at least one 
		# 2.1) email format 
		# TODO : email regex check 
		if email_address:
			if (not '@booking.com' in email_address):
				messages.error(self.request, "Please check your email: is it booking internal email ?")
				return redirect(self.request.path)
			else:
				pass

		if (not files) and (not keywords):
			messages.error(self.request, "Fill in at least one of files/keywords")
			return redirect(self.request.path)
		else:
			messages.success(self.request, 'Config Successfully Updated for {team}!'.format(team=team))

		# must save it !!!
		self.object = form.save()
		return redirect('userconfig-home-with-filter')
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

	#paginator 
    paginator = Paginator(userconfig_list, 2)
    page = request.GET.get('page')
    try:
        userconfig_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        userconfig_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        userconfig_list = paginator.page(paginator.num_pages)

    #return render(request, 'userconfig/userconfig_filter_home.html', {'filter': userconfig_filter, 'configs':userconfig_list})
    return render(request, 'userconfig/userconfig_filter_home.html', {'filter': userconfig_filter, 'configs':userconfig_list})

#Crash Issue Detail Session
class CrashissuesTableView(tables.Table):
    class Meta:
        model = Crashissues

class TableView(tables.SingleTableView):
    table_class = CrashissuesTableView
    queryset = Crashissues.objects.all()
    template_name = "userconfig/crashissues_list.html"

def crashissues_list(request):
    table = Crashissues.objects.all()

    return render(
		request, 
		"userconfig/crashissues_list.html", 
		{ "tables": table }
	)

def crashissues_list_user(request, userconfig_id):
	default_issue_id = '0000-0000-0000-0000'
	print('In crashissues_list_user: ', userconfig_id)
	UserConfig = Config.objects.filter(id=userconfig_id)
	#print(UserConfig)
	issue_id_list = UserConfig[0].issue_id_list
	#team = UserConfig[0].team

	platform = UserConfig[0].platform

	if platform == 'ios':
		platform = 'iOS'
	elif platform == 'android':
		platform = 'Android'
	else:
		platform = 'Android' 

	print('In issue_id_list >> ', issue_id_list)

	issue_table_user = []

	if default_issue_id in issue_id_list:
		messages.info(request, "No Crash Detected for your configuration !")
	else:
		# get crash issue id in UserConfig 
		for issue_id in issue_id_list.split(','):
			try:
				one_issue = Crashissues.objects.filter(issue_id=issue_id)
			except:
				messages.error(request,'[missing crash id in database] ', issue_id)	
				continue
			issue_table_user.append(one_issue[0])

		print("Total issue for this user : ", len(issue_table_user))

		messages.info(request, "Crash Detected for your configuration !")
	return render(request,
				"userconfig/crashissues_list.html", 
				{ "tables": issue_table_user , 'platform':platform, 'userconfig_id':userconfig_id}
			)

def firebase(request,platform,issue_id):
	if 'ios' in platform.lower():
		platform = 'iOS'
	elif 'android' in platform.lower():
		platform = 'Android'
	else:
		platform = 'Android' 

	print('[Firebase] ', platform , issue_id)
	#return render(request, 'userconfig/firebase.html')
	url='https://ota.booking.com/crashes/{platform}/{issue_id}'.format(platform=platform, issue_id=issue_id) 
	print('[URL] ',url)	
	return redirect(url)