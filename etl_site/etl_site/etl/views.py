# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import shortcuts, http
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from pickle import dumps, loads

from .forms import FileForm
from .models import Table as table_model

def form(request):
	'''Generates upload form on landing page'''
	request.session.flush()
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			table_instance = table_model(raw_file=request.FILES['raw_file'])
			table_instance.save()
			request.session['active_instance'] = table_instance.get_id()
			return HttpResponseRedirect('/manage-table/')
	else:
		form = FileForm()

	return render(request,
		'form.html',
		{'form': form})

def create_table(request):
	'''Instantiates a table object from CSV'''
	active_id = request.session.get('active_instance')
	table_instance = table_model.objects.get(id=active_id)
	table_instance.instantiate_table()
	request.session['sql_table'] = dumps(table_instance)
	return JsonResponse(table_instance.get_json())

def manage_table(request):
	'''Generates form for user to specify parameters'''
	if request.method == 'POST':
		loads(request.session.get('sql_table')).get_sql(
			request.POST.getlist('column_name'),
			request.POST.getlist('datatype'))
		return HttpResponseRedirect('/download/')

	return render(request,
		'manage-table.html')

def download(request):
	'''Generates download page'''
	active_id = request.session.get('active_instance')
	table_instance = table_model.objects.get(id=active_id)
	return render(request,
		'download.html',
		{'download_url': table_instance.get_sql_file()})

