from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from . models import *
from django.db.models import F
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
import threading

# Create your views here.


# portfl_app/utils.py (ou en haut du fichier views.py)

def send_newsletter_email(email):
    try:
        send_mail(
            "Bienvenue 🎉",
            "Merci de vous être abonné à la newsletter.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )
    except Exception as e:
        print("Newsletter email error:", e)

def health(request):
    return JsonResponse({"status": "ok"})

def accueil(request):
    return render(request, 'onglet/accueil.html')

def propos(request):
    return render(request, 'onglet/propos.html')


def service(request):
    reviews = Review.objects.filter(is_approved=True).order_by("-created_at")

    if request.method == "POST":
        Review.objects.create(
            name=request.POST["name"],
            rating=request.POST["rating"],
            comment=request.POST["comment"],
            is_approved=False  # IMPORTANT
        )

        return render(request, "onglet/service.html", {
            "reviews": reviews,
            "success": True
        })

    paginator = Paginator(reviews, 4)  # 6 avis par page
    page_number = request.GET.get("page")
    reviews = paginator.get_page(page_number)

    return render(request, "onglet/service.html", {
        "reviews": reviews
    })


def create_request(request):
    service_type = request.GET.get('type')

    if request.method == "POST":
        ServiceRequest.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            service_type=request.POST['service_type'],
            description=request.POST['description']
        )

        return render(request, 'onglet/request_form.html', {
            'service_type': service_type,
            'success': True
        })

    return render(request, 'onglet/request_form.html', {
        'service_type': service_type
    })


def email_open(request, quote_id):
    EmailLog.objects.filter(
        quote_id=quote_id,
        is_read=False
    ).update(is_read=True)
    return HttpResponse(status=204)


def projet(request):

    subscribers_count = Subscriber.objects.count()
    context = {
        'projects_realises': Project.objects.filter(status='realise'),
        'projects_encours': Project.objects.filter(status='encours'),
        'projects_futurs': Project.objects.filter(status='futur'),
        'subscribers_count': subscribers_count
    }
    return render(request, 'onglet/project.html', context)


@require_POST
def project_like(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # session
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # ip
    ip = request.META.get("REMOTE_ADDR")

    # déjà liké ?
    already_liked = ProjectLike.objects.filter(
        project=project,
        ip_address=ip,
        session_key=session_key
    ).exists()

    if already_liked:
        return JsonResponse({
            "status": "error",
            "message": "Déjà liké"
        }, status=400)

    # enregistrer le like
    ProjectLike.objects.create(
        project=project,
        ip_address=ip,
        session_key=session_key
    )

    # incrément atomique
    Project.objects.filter(pk=pk).update(likes=F("likes") + 1)
    project.refresh_from_db()

    return JsonResponse({
        "status": "success",
        "likes": project.likes
    })


def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscriber, created = Subscriber.objects.get_or_create(email=email)

        if created:
            # ENVOI EMAIL ASYNCHRONE (NON BLOQUANT)
            threading.Thread(
                target=send_newsletter_email,
                args=(email,),
                daemon=True
            ).start()

            messages.success(request, "✅ Merci pour votre abonnement.")
        else:
            messages.warning(request, "⚠️ Cet email est déjà abonné.")

    return redirect(request.META.get("HTTP_REFERER", "/"))


def certification(request):
    context = {
        'certifications_obtenues': Certification.objects.filter(status='obtenue'),
        'certifications_encours': Certification.objects.filter(status='encours'),
        'certifications_futures': Certification.objects.filter(status='future'),
    }
    return render(request, 'onglet/certifi.html', context)


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'onglet/faq.html', {
        'faqs': faqs
    })


def dashboard(request):

    # VISITES PAR JOUR
    visits_by_day = (
        VisitorLog.objects
        .annotate(day=TruncDay("visited_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    visit_labels = [v["day"].strftime("%d %b") for v in visits_by_day]
    visit_data = [v["total"] for v in visits_by_day]

    # ENVOI D’UNE SUGGESTION
    if request.method == "POST":
        name = request.POST.get("name_sug")
        email = request.POST.get("email_sug")
        message = request.POST.get("message_sug")

        if name and message:
            Suggestion.objects.create(
                name_sug=name,
                email_sug=email,
                message_sug=message
            )
            return redirect("dashboard")

    # SERVICES LES PLUS DEMANDÉS
    services_stats = (
        ServiceRequest.objects
        .values("service_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # PAGINATION DES SUGGESTIONS
    suggestions_qs = Suggestion.objects.order_by("-created_at")
    paginator = Paginator(suggestions_qs, 6)  # 6 suggestions par page

    page_number = request.GET.get("page")
    suggestions_page = paginator.get_page(page_number)

    context = {
        "visits_count": VisitorLog.objects.count(),
        "projects_count": Project.objects.count(),
        "total_likes": Project.objects.aggregate(total=Sum("likes"))["total"] or 0,
        "certifications_count": Certification.objects.count(),
        "subscribers_count": Subscriber.objects.filter(is_active=True).count(),

        "visit_labels": visit_labels,
        "visit_data": visit_data,

        "services_stats": services_stats,
        "suggestions": suggestions_page,   # ⬅ pagination
    }

    return render(request, "onglet/dashboard.html", context)


@require_POST
def like_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)

    # session
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # ip
    ip = request.META.get("REMOTE_ADDR")

    already_liked = SuggestionLike.objects.filter(
        suggestion=suggestion,
        ip_address=ip,
        session_key=session_key
    ).exists()

    if already_liked:
        return JsonResponse({
            "status": "error",
            "message": "Déjà liké"
        }, status=400)

    # enregistrer le like
    SuggestionLike.objects.create(
        suggestion=suggestion,
        ip_address=ip,
        session_key=session_key
    )

    # incrément atomique
    suggestion.likes = F("likes") + 1
    suggestion.save(update_fields=["likes"])
    suggestion.refresh_from_db()

    return JsonResponse({
        "status": "success",
        "likes": suggestion.likes
    })