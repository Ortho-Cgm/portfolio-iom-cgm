from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from .utils import send_quote_email
from django.utils.html import format_html

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service_type", "is_validated", "created_at")
    list_filter = ("service_type", "is_validated")
    search_fields = ("name", "email")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved")
    search_fields = ("name", "comment")
    list_editable = ("is_approved",)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "get_client_email",
        "amount",
        "is_approved",
        "email_sent",
        "created_at",
        "resend_button",
    )

    def get_client_email(self, obj):
        return obj.request.email

    get_client_email.short_description = "Email client"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:quote_id>/resend/",
                self.admin_site.admin_view(self.resend_email),
                name="quote_resend",
            ),
        ]
        return custom_urls + urls
    
    def resend_button(self, obj):
        url = reverse("admin:quote_resend", args=[obj.id])
        return format_html(
            '<a class="button" href="{}">📧 Renvoyer</a>',
            url
        )

    resend_button.short_description = "Action"

    def resend_email(self, request, quote_id):
        quote = Quote.objects.get(pk=quote_id)

        send_quote_email(quote.request, quote, manual=True)

        quote.email_sent = True
        quote.save(update_fields=["email_sent"])

        messages.success(
            request,
            f"📧 Email renvoyé à {quote.request.email}"
        )

        return redirect("admin:portfl_app_quote_change", quote_id)


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "quote",
        "sent_at",
        "is_read",
        "is_manual",
    )
    list_filter = ("is_read", "is_manual")
    readonly_fields = ("sent_at",)


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    # Colonnes visibles dans la liste
    list_display = (
        "ip_address",
        "browser",
        "os",
        "device",
        "page",
        "visited_at",
    )

    # Filtres latéraux
    list_filter = (
        "device",
        "browser",
        "os",
        "visited_at",
    )

    # Recherche rapide
    search_fields = (
        "ip_address",
        "browser",
        "os",
        "page",
        "user_agent",
    )

    # Ordre par défaut
    ordering = ("-visited_at",)

    # Pagination (important si beaucoup de visites)
    list_per_page = 50

    # Champs en lecture seule
    readonly_fields = (
        "ip_address",
        "browser",
        "os",
        "device",
        "page",
        "user_agent",
        "visited_at",
    )

    # Organisation de la vue détail
    fieldsets = (
        ("Informations visiteur", {
            "fields": (
                "ip_address",
                "device",
                "browser",
                "os",
            )
        }),
        ("Navigation", {
            "fields": (
                "page",
                "visited_at",
            )
        }),
        ("User Agent brut", {
            "fields": ("user_agent",),
            "classes": ("collapse",),
        }),
    )



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'likes', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'technologies')

@admin.register(ProjectLike)
class ProjectLikeAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'session_key', 'created_at')
    list_filter = ('ip_address', 'session_key')
    search_fields = ('ip_address', 'session_key')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    search_fields = ('email',)

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'status', 'issued_date')
    list_filter = ('status', 'provider')
    search_fields = ('title', 'provider', 'technologies')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'created_at')
    list_filter = ('order', 'question')
    search_fields = ('order', 'question')

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('name_sug', 'email_sug', 'likes', 'created_at')
    list_filter = ('email_sug', 'likes')
    search_fields = ('name_sug', 'email_sug')

@admin.register(SuggestionLike)
class SuggestionLikeAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'session_key', 'created_at')
    list_filter = ('ip_address', 'session_key')
    search_fields = ('ip_address', 'session_key')