import os

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import View

from whistle import settings


class ReactAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return redirect(f'https://localhost:3000/')
