from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Test, Result, Worker
from .forms import RegisterForm, ResultForm

# Create your views here.
def index(request, register_form=None):
    worker_id = request.session.get('worker_id')
    try:
        if worker_id:
            worker = Worker.objects.get(pk=worker_id)
        else:
            worker = None
    except Worker.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('cognitive_skills:home'))

    register_form = register_form or RegisterForm()
    
    context = {
        'title': 'Cognitive Skills App',
        'worker': worker,
        'available_tests': Test.objects.exclude(results__worker=worker) if worker else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker=worker) if worker else [],
        'register_form': register_form
    }

    return render(request, 'cognitive_skills/index.html', context)

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            turk_id = register_form.cleaned_data['turk_id']
            worker = Worker(turk_id=turk_id)
            worker.save()
            request.session['worker_id'] = str(worker.id)
            first_test = Test.objects.all().first()
            return HttpResponseRedirect(reverse('cognitive_skills:test', args=[first_test.slug]))
        else:
            context = {
                'title': 'Cognitive Skills App',
                'worker': None,
                'available_tests': Test.objects.all(),
                'completed_tests': [],
                'register_form': register_form
            }
            return render(request, 'cognitive_skills/index.html', context)
    context = {
        'title': 'Cognitive Skills App',
        'worker': None,
        'available_tests': Test.objects.all(),
        'completed_tests': [],
        'register_form': RegisterForm()
    }
    return render(request, 'cognitive_skills/index.html', context)

def score(request):
    if request.method == "POST":
        worker_id = request.session.get('worker_id')
        try:
            if worker_id:
                worker = Worker.objects.get(pk=worker_id)
            else:
                worker = None
        except Worker.DoesNotExist:
            request.session.flush()
            return HttpResponseRedirect(reverse('cognitive_skills:home'))

        result = ResultForm(request.POST)
        if result.is_valid():
            result.save()
        else:
            test = Test.objects.get(pk=request.POST.get('test'))
            return render(request, 'cognitive_skills/score.html', {
                'worker': worker,
                'test': test,
                'result_form': result,
            })
        
        test = result.cleaned_data['test']
        next_test = Test.objects.filter(name__gt=test.name).order_by('name').first()

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
        worker = Worker.objects.get(pk=worker_id)
    except Worker.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('cognitive_skills:home'))

    test = get_object_or_404(Test, slug=slug)
    
    result_form = ResultForm(initial={
        'worker': worker,
        'test': test,
    })

    context = {
        'available_tests': Test.objects.exclude(results__worker=worker) if worker else Test.objects.all(),
        'completed_tests': Test.objects.filter(results__worker=worker) if worker else [],
        'test': test,
        'worker': worker,
        'result_form': result_form,
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