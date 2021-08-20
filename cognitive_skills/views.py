from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Test, Result

# Create your views here.
def index(request):
    worker_id = request.session.get('turk_id')
    context = {
        'title': 'Cognitive Skills App',
        'turk_id': request.session.get('turk_id', None),
        'available_tests': Test.objects.exclude(results__worker_id=worker_id) if worker_id else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker_id=worker_id) if worker_id else [],
    }

    return render(request, 'cognitive_skills/index.html', context)

def register(request):
    if request.method == 'POST':
        turk_id = request.POST.get('turk_id')
        request.session['turk_id'] = turk_id
        first_test = Test.objects.all().first()
        return HttpResponseRedirect(reverse('cognitive_skills:test', args=[first_test.slug]))
    return HttpResponseNotFound()

def score(request):
    worker_id = request.session.get('turk_id')
    if not worker_id:
        return HttpResponseRedirect('cognitive_skills:home')

    test = Test.objects.get(pk=request.POST.get('test'))
    
    next_test = Test.objects.filter(name__gt=test.name).order_by('name').first()
    
    result = Result(
        worker_id=worker_id,
        test=test,
        correct=request.POST.get('correct'),
        total=request.POST.get('total'),
    )
    try:
        result.save()
    except Exception as e:
        raise e

    if next_test:
        return HttpResponseRedirect(reverse('cognitive_skills:test', args=[next_test.slug]))
    else:
        return HttpResponseRedirect(reverse('cognitive_skills:summary'))

def reset(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('cognitive_skills:home'))

def test(request, slug):
    if not request.session.get('turk_id'):
        return HttpResponseRedirect(reverse('cognitive_skills:home'))
    
    worker_id = request.session.get('turk_id')
    context = {
        'available_tests': Test.objects.exclude(results__worker_id=worker_id) if worker_id else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker_id=worker_id) if worker_id else [],
        'test': get_object_or_404(Test, slug=slug),
        'turk_id': worker_id,
    }
    return render(request, 'cognitive_skills/test.html', context)

def summary(request):
    worker_id = request.session.get('turk_id')
    results = Result.objects.filter(worker_id=worker_id).order_by('test__name')
    
    context = {
        'turk_id': worker_id,
        'available_tests': Test.objects.exclude(results__worker_id=worker_id) if worker_id else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker_id=worker_id) if worker_id else [],
        'results': results,
    }

    return render(request, 'cognitive_skills/summary.html', context)