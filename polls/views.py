# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from django.shortcuts import get_object_or_404, render, redirect, render_to_response

from .models import Question, Choice, CSVFile, SubFile
from .forms import CSVFileForm, SubFileForm


import pdb
# Create your views here.

#displays latest few questions

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list' 

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]

#detail page - displays a question text, with no results but with a form to vote.
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

#result page - displays results for a particular question.
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

#vote action -  handles voting for a particular choice in a particular question.
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def upload(request):
	# pid = csv_id
	if request.method == 'POST':
		desc = request.POST['description']
		pdb.set_trace()
		#for multiple files
		files = request.FILES.getlist('myfiles')
		for number, a_file in enumerate(files):
			instance = SubFile(
				pid = csv_id ,
				my_file = a_file,
				description = desc
				)
			instance.save()
		request.session['number_of_files'] = number + 1
		return redirect('polls:attachment_done')

	return render(request, 'polls/model_form_upload.html')

def attachment_done(request):
	return render_to_response('polls/attachment_done.html', context={"num_files": request.session["number_of_files"]})



def name_csv(request):
	if request.method == 'POST':
		# pid = request.POST['id']
		form = CSVFileForm(request.POST)
		pdb.set_trace()	
		if form.is_valid():
			obj = CSVFile(
				name_of = form.cleaned_data['name_of']
				)
			a = obj.save()
			pdb.set_trace()
			# print (a.id)
			csv_id = a.id
			return redirect('polls:upload')

	return render(request, 'polls/csv_upload.html')
# form = FileForm(request.POST, request.FILES)
# 	if form.is_valid():
# 		form.save()
# 		return redirect('/polls')
#	else:
# 		form = FileForm()