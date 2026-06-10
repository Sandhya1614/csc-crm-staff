from django.urls import path
from . import views

urlpatterns = [
    # Own document vault
    path('', views.document_vault, name='document_vault'),
    path('documents/upload/', views.upload_document, name='upload_document'),


    path('staff/<int:staff_id>/documents/', views.document_vault, name='staff_document_vault'),
    path('staff/<int:staff_id>/documents/upload/', views.upload_document, name='staff_upload_document'),
    
    # Document actions
    path('documents/<int:doc_id>/status/', views.update_document_status, name='update_document_status'),
    path('delete/<int:doc_id>/delete/', views.delete_document, name='delete_document'),
]
