from django.shortcuts import render
from apps.base import models as base_models
from apps.cms import models as cms_models
# Create your views here.
def index(request):
    settings = base_models.Settings.objects.first()
    banners = base_models.Banner.objects.all()
    categories = cms_models.CategoryOrganization.objects.all()
    return render(request, "pages/index.html", locals())