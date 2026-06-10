import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Document
from .forms import DocumentUploadForm


def document_vault(request,staff_id=None):
    

    if staff_id:
        
        staff_user = get_object_or_404(Staff, id=staff_id)
    else:
        staff_user = request.user


    documents = Document.objects.filter(uploaded_by=staff_user)


    # Stats
    verified_count = documents.filter(status='verified').count()
    pending_count = documents.filter(status='pending').count()
    rejected_count = documents.filter(status='rejected').count()

    upload_form = DocumentUploadForm()

    context = {
        
        'documents': documents,
        'upload_form': upload_form,
        'verified_count': verified_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        
    }
    return render(request, 'staff/dashboard.html', context)



@require_POST
def upload_document(request):
    """ upload  document ."""


    form = DocumentUploadForm(request.POST, request.FILES)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if form.is_valid():
        doc = form.save()


        if is_ajax:
            return JsonResponse({
                'success': True,
                'document': {
                    'id': doc.id,
                    'name': doc.name,
                    'filename': doc.filename,
                    'doc_type': doc.doc_type,
                    'status': doc.status,
                    'status_display': doc.get_status_display(),
                    'uploaded_at': doc.uploaded_at.strftime('%d %b %Y, %I:%M %p'),
                    'file_url': doc.file.url,
                }
            })
        messages.success(request, f'"{doc.name}" uploaded successfully.')
        return redirect('document_vault')







@require_POST
def update_document_status(request, doc_id):
    """Update a document's status (managers only)."""
    

    doc = get_object_or_404(Document, pk=doc_id)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    try:
        data = json.loads(request.body)
        new_status = data.get('status')
    except (json.JSONDecodeError, AttributeError):
        new_status = request.POST.get('status')

    valid_statuses = [s[0] for s in Document.STATUS_CHOICES]
    if new_status not in valid_statuses:
        
            return JsonResponse({'success': False, 'error': 'Invalid status.'}, status=400)
    

    doc.status = new_status
    doc.save()

    return JsonResponse({
            'success': True,
            'status': doc.status,
            'status_display': doc.get_status_display(),
        })



# @require_POST
# def delete_document(request, doc_id):
    
#     """Delete a document. Owner or manager only."""
#     doc = get_object_or_404(Document, pk=doc_id)
    

#     try:
#         doc.file.delete(save=False)
#     except Exception:
#         pass
#     doc.delete()

    
#     return JsonResponse({'success': True, 'message': 'Document deleted successfuly.'})
@require_POST
def delete_document(request, doc_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Safely fetch the document or throw a 404 if it doesn't exist
        document = get_object_or_404(Document, id=doc_id)
        
        try:
            # Delete the actual file from storage and the record from the database
            document.file.delete() # Deletes file from media folder
            document.delete()      # Deletes record from database
            
            return JsonResponse({
                'success': True, 
                'message': 'Document deleted successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'An error occurred: {str(e)}'
            }, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)
def edit_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    if request.method == 'POST':
        form = DocumentUploadForm(
            request.POST,
            request.FILES,
            instance=document
        )
        if form.is_valid():
            form.save()
            return redirect('document_vault')
    else:
        form = DocumentUploadForm(instance=document)

    return render(request, 'staff/dashboard.html', {
        'form': form,
        'document': document
    })