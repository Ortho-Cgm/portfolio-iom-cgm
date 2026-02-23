from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('onglet/apropos/', views.propos, name="propos"),

    # services
    path('onglet/services/', views.service, name="service"),

    # créer une demande
    path('demande/', views.create_request, name="create_request"),

    path("email/open/<int:quote_id>/", views.email_open),

    path('onglet/project/', views.projet, name="project"),
    path("project/<int:pk>/like/", views.project_like, name="project_like"),

    path('newsletter/subscribe/', views.subscribe_newsletter, name='newsletter_subscribe'),

    path('onglet/certifications/', views.certification, name="certification"),

    path('onglet/faq/', views.faq, name="faq"),

    path('onglet/dashboard/', views.dashboard, name="dashboard"),

    path("suggestion/<int:suggestion_id>/like/", views.like_suggestion, name="like_suggestion"),
]


if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)