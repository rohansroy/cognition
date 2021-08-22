from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Test, Result, Worker

# Create your views here.
def index(request):
    worker_id = request.session.get('worker_id')
    try:
        if worker_id:
            worker = Worker.objects.get(pk=worker_id)
        else:
            worker = None
    except Worker.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('cognitive_skills:home'))
    context = {
        'title': 'Cognitive Skills App',
        'worker': worker,
        'available_tests': Test.objects.exclude(results__worker=worker) if worker else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker=worker) if worker else [],
    }

    return render(request, 'cognitive_skills/index.html', context)

def register(request):
    if request.method == 'POST':
        turk_id = request.POST.get('turk_id')
        worker = Worker(turk_id=turk_id)
        worker.save()
        request.session['worker_id'] = str(worker.id)
        first_test = Test.objects.all().first()
        return HttpResponseRedirect(reverse('cognitive_skills:test', args=[first_test.slug]))
    return HttpResponseNotFound()

def score(request):
    worker_id = request.session.get('worker_id')
    try:
        if worker_id:
            worker = Worker.objects.get(pk=worker_id)
        else:
            worker = None
    except Worker.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('cognitive_skills:home'))

    test = Test.objects.get(pk=request.POST.get('test'))
    
    next_test = Test.objects.filter(name__gt=test.name).order_by('name').first()
    
    result = Result(
        worker=worker,
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
    worker_id = request.session.get('worker_id')

    if not worker_id:
        return HttpResponseRedirect(reverse('cognitive_skills:home'))

    try:
        if worker_id:
            worker = Worker.objects.get(pk=worker_id)
        else:
            worker = None
    except Worker.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('cognitive_skills:home'))
    
    context = {
        'available_tests': Test.objects.exclude(results__worker=worker) if worker else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker=worker) if worker else [],
        'test': get_object_or_404(Test, slug=slug),
        'worker': worker,
    }
    return render(request, 'cognitive_skills/test.html', context)

def summary(request):
    worker_id = request.session.get('worker_id')
    try:
        if worker_id:
            worker = Worker.objects.get(pk=worker_id)
    except Worker.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('cognitive_skills:home'))
    results = Result.objects.filter(worker=worker).order_by('test__name')
    
    context = {
        'worker': worker,
        'available_tests': Test.objects.exclude(results__worker=worker) if worker else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker=worker) if worker else [],
        'results': results,
    }

    return render(request, 'cognitive_skills/summary.html', context)