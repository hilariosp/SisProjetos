from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Criterio  
from .forms import CriterioForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('criterio.view_criterio', raise_exception=True)

def index(request): 

    criterios = Criterio.objects.all()
    return render(request, 'criterio/index.html', {'criterios': criterios})

@login_required
@permission_required('criterio.view_criterio', raise_exception=True)
def detail(request, id_criterio):

    criterio = Criterio.objects.get(id=id_criterio)
    return render(request, 'criterio/detail.html', {'criterio': criterio})

@login_required
@permission_required('criterio.add_criterio', raise_exception=True)
def add(request): 

    if request.method == 'POST':

        form = CriterioForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/criterio/')
    else:
        form = CriterioForm()

    return render(request, 'criterio/add.html', { 'form': form })

@login_required
@permission_required('criterio.change_criterio', raise_exception=True)
def update(request, id_criterio):

    criterio = Criterio.objects.get(id=id_criterio)

    if request.method == 'POST':

        form = CriterioForm(request.POST, instance=criterio)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/criterio/')
    else:
        form = CriterioForm(instance=criterio)

    return render(request, 'criterio/update.html', { 'form': form })

@login_required
@permission_required('criterio.delete_criterio', raise_exception=True)
def delete(request, id_criterio):

    Criterio.objects.filter(id=id_criterio).delete()

    return HttpResponseRedirect('/criterio/')


