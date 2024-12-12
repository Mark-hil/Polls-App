from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import CreatePollForm
from .models import Poll

def home(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'poll/home.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            # print (form.cleaned_data['question'])
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
            'form' : form
        }
    return render(request, 'poll/create.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else: 
            return HttpResponse(400,'invalid forms')
        
        poll.save()
        
        return redirect('results', poll_id)
        
    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)

def results(request,poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)
