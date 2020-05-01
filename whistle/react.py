import os

from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.generic.base import View

from whistle import settings


class ReactAppView(View):
    def get(self, request: HttpRequest):
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return redirect(f'http://localhost:3000{request.get_full_path()}')
