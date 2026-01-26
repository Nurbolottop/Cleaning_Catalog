from django.shortcuts import get_object_or_404, render
import itertools
from apps.base import models as base_models
from apps.cms import models as cms_models
# Create your views here.
def category(request):
    settings = base_models.Settings.objects.first()
    banners = base_models.Banner.objects.all()
    categories = cms_models.CategoryOrganization.objects.all()
    return render(request, "pages/category.html", locals())


def category_detail(request, pk: int):
    settings = base_models.Settings.objects.first()
    banners = base_models.Banner.objects.all()
    categories = cms_models.CategoryOrganization.objects.all()
    category = get_object_or_404(cms_models.CategoryOrganization, pk=pk)
    services = category.services.filter(is_active=True)
    return render(request, "pages/category.html", locals())


def service_detail(request, slug: str):
    settings = base_models.Settings.objects.first()
    banners = base_models.Banner.objects.all()
    categories = cms_models.CategoryOrganization.objects.all()
    service = get_object_or_404(cms_models.Service, slug=slug, is_active=True)
    category = service.organization
    zone_items = (
        service.zone_items.filter(is_active=True)
        .order_by("zone", "order", "id")
    )
    zone_groups = []
    for zone, items_iter in itertools.groupby(zone_items, key=lambda x: x.zone):
        label = dict(cms_models.ServiceZoneItem.ZONE_CHOICES).get(zone, zone)
        zone_groups.append({"zone": zone, "label": label, "items": list(items_iter)})

    chemical_items = (
        service.chemical_items.filter(is_active=True)
        .order_by("order", "id")
    )

    equipment_items = (
        service.equipment_items.filter(is_active=True)
        .order_by("order", "id")
    )

    faq_items = (
        service.faq_items.filter(is_active=True)
        .order_by("order", "id")
    )

    requirement_items = (
        service.requirement_items.filter(is_active=True)
        .order_by("order", "id")
    )

    work_condition_items = (
        service.work_condition_items.filter(is_active=True)
        .order_by("order", "id")
    )

    excluded_items = (
        service.excluded_items.filter(is_active=True)
        .order_by("order", "id")
    )

    price_items = (
        service.price_items.filter(is_active=True)
        .order_by("order", "id")
    )

    cases_before_after = (
        service.cases_before_after.filter(is_active=True)
        .order_by("order", "id")
    )

    client_companies = (
        service.client_companies.filter(is_active=True)
        .order_by("order", "id")
    )

    documents = (
        service.documents.filter(is_active=True)
        .order_by("order", "id")
    )
    return render(request, "pages/service.html", locals())
