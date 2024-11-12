from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/<int:user_id>/update/<str:role>/', views.update_user_role, name='update_user_role'),
    
    path('article/<int:article_id>/', views.view_article, name='view_article'),
    path('admin/articles/', views.manage_articles, name='manage_articles'),
    path('admin/articles/add/', views.add_article, name='add_article'),
    path('admin/articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    
    path('admin/pdfs/', views.manage_pdfs, name='manage_pdfs'),
    path('admin/pdfs/add/', views.add_pdf, name='add_pdf'),
    path('admin/pdfs/<int:pdf_id>/edit/', views.edit_pdf, name='edit_pdf'),

     path('pdf/<int:pdf_id>/', views.pdf_view, name='pdf_view'),
]
