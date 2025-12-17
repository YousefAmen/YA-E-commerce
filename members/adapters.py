from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.shortcuts import resolve_url, get_object_or_404
from django.urls import reverse, reverse_lazy
from allauth.socialaccount.models import SocialAccount


class AccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        user = request.user
        if user.role == "merchant":
            return reverse_lazy(
                "complete_merchant", kwargs={"slug": user.slug, "id": user.id}
            )
        else:
            return reverse("home")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_redirect_url(self, request):
        user = request.user
        has_social_account = get_object_or_404(SocialAccount, user)
        if (
            has_social_account
            and not hasattr(has_social_account.user, "merchant")
            and not hasattr(has_social_account.user, "customer")
        ):
            return resolve_url("select_role")
        if user.role == "merchant":
            return reverse("complete_merchant")

        return super().get_signup_redirect_url(request)
