from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Usuario 
from .forms import UsuarioForm, UsuarioEditForm

@login_required
@permission_required('usuario.view_usuario', raise_exception=True)
def index(request):
    usuario = Usuario.objects.all().order_by('nome') 
    return render(request, 'usuario/index.html', {'usuario': usuario})

@login_required
@permission_required('usuario.add_usuario', raise_exception=True)
def add(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('usuario:usuario_index')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/add.html', {'form': form})

@login_required
@permission_required('usuario.view_usuario', raise_exception=True) 
def detail(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    return render(request, 'usuario/detail.html', {'usuario': usuario})

@login_required
@permission_required('usuario.change_usuario', raise_exception=True)
def update(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuario:usuario_index')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'usuario/update.html', {'form': form})

@login_required
@permission_required('usuario.delete_usuario', raise_exception=True)
def delete(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    usuario.delete()
    return redirect('usuario:usuario_index')