from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Document
from .forms import DocumentForm

def dashboard(request):

    search = request.GET.get('search')

    if search:
        documents = Document.objects.filter(
            name__icontains=search
        )

    else:
        documents = Document.objects.all()

    context = {
        'documents': documents
    }

    return render( request,'staff/dashboard.html',context )



def add_document(request):

    form = DocumentForm()

    if request.method == 'POST':

        form = DocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            return redirect('dashboard')

    return render(
        request,
        'staff/add_document.html',
        {'form': form}
    )



def update_document(request, id):

    document = get_object_or_404(
        Document,
        id=id
    )

    form = DocumentForm(instance=document)

    if request.method == 'POST':

        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document
        )

        if form.is_valid():
            form.save()

            return redirect('dashboard')

    return render(
        request,
        'staff/update_document.html',
        {'form': form}
    )

def delete_document(request, id):

    document = get_object_or_404(
        Document,
        id=id
    )

    if request.method == 'POST':
        document.delete()
        return redirect('dashboard')

    return render(
        request,
        'staff/delete_document.html',
        {'document': document}
    )



def view_document(request, id):

    document = get_object_or_404(
        Document,
        id=id
    )

    return render(
        request,
        'staff/view_document.html',
        {'document': document}
    )

def verify_certificate(request):

    certificate = None

    search_id = request.GET.get('certificate_id')

    if search_id:

        certificate = Document.objects.filter(
            certificate_id=search_id
        ).first()

    context = {
        'certificate': certificate
    }

    return render(
        request,
        'staff/verify_certificate.html',
        context
    )
