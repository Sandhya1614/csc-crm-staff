from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('add/',views.add_document,name='add_document' ),
    path('update/<int:id>/',views.update_document,name='update_document' ),
    path('delete/<int:id>/',views.delete_document,name='delete_document'),
    path('view/<int:id>/',views.view_document,name='view_document' ),
    path('verify/', views.verify_certificate, name='verify_certificate'),
    
]