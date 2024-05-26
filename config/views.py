from django.shortcuts import redirect
from django.views.generic import TemplateView

def home(request):
    return redirect('the_list', sorting='by-date')


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
