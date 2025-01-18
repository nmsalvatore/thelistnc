from django.shortcuts import redirect
from django.views.generic import TemplateView


def catch_all(request):
    return redirect("farewell")


def home(request):
    return redirect("the_list", sorting="by-date")


class FarewellView(TemplateView):
    template_name = "farewell.html"


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
