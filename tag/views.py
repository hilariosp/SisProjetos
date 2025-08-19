from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Tag  
from .forms import TagForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
def index(request): 

    tags = Tag.objects.all()
    return render(request, 'tag/index.html', {'tags': tags})

@login_required
def detail(request, id_tag):

    tag = Tag.objects.get(id=id_tag)
    return render(request, 'tag/detail.html', {'tag': tag})

@login_required
@permission_required('tag.add_tag', raise_exception=True)
def add(request): 

    if request.method == 'POST':

        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tag/')
    else:
        form = TagForm()

    return render(request, 'tag/add.html', { 'form': form })

@login_required
@permission_required('tag.change_tag', raise_exception=True)
def update(request, id_tag):

    tag = Tag.objects.get(id=id_tag)

    if request.method == 'POST':

        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tag/')
    else:
        form = TagForm(instance=tag)

    return render(request, 'tag/update.html', { 'form': form })

@login_required
@permission_required('tag.delete_tag', raise_exception=True)
def delete(request, id_tag):
    #recuperar a tag do banco de dados 
    Tag.objects.filter(id=id_tag).delete()

    return HttpResponseRedirect('/tag/')


