from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from django.views import generic

from django.http import HttpResponse
from django.template import loader



from .models import Choice, Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'blogs/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blogs:results', args=(question.id,)))
    
    def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'blogs/results.html', {'question': question})
    
class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
         model = Question
         template_name = 'blogs/detail.html'

class ResultsView(generic.DetailView):
         model = Question
         template_name = 'blogs/results.html'