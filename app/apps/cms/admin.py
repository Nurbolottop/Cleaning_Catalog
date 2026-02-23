from django.contrib import admin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.text import slugify
import uuid
from apps.cms import models as cms_models


# -------------------------------
# Категории организаций (бизнесы)
# -------------------------------
@admin.register(cms_models.CategoryOrganization)
class CategoryOrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("order", "name")

# -------------------------------
# Inline: Уборка по зонам / помещениям
# -------------------------------
class ServiceZoneItemInline(admin.TabularInline):
    model = cms_models.ServiceZoneItem
    extra = 1
    fields = ("zone", "text", "order", "is_active")
    ordering = ("zone", "order")

# -------------------------------
# Inline: Используемые средства
# -------------------------------
class ServiceChemicalItemInline(admin.TabularInline):
    model = cms_models.ServiceChemicalItem
    extra = 1
    fields = ("name", "description", "image", "order", "is_active")
    ordering = ("order",) 

# -------------------------------
# Inline: Используемые оборудование
# -------------------------------
class ServiceEquipmentItemInline(admin.TabularInline):
    model = cms_models.ServiceEquipmentItem
    extra = 1
    fields = ("name", "description", "image", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Часто задаваемые вопросы
# -------------------------------
class ServiceFAQItemInline(admin.TabularInline):
    model = cms_models.ServiceFAQItem
    extra = 1
    fields = ("question", "answer", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Требования к объекту
# -------------------------------
class ServiceRequirementItemInline(admin.TabularInline):
    model = cms_models.ServiceRequirementItem
    extra = 1
    fields = ("text", "description", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Условия выполнения работ
# -------------------------------
class ServiceWorkConditionItemInline(admin.TabularInline):
    model = cms_models.ServiceWorkConditionItem
    extra = 1
    fields = ("text", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Что НЕ входит
# -------------------------------
class ServiceExcludedItemInline(admin.TabularInline):
    model = cms_models.ServiceExcludedItem
    extra = 1
    fields = ("text", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Кейсы до/после
# -------------------------------
class ServiceCaseBeforeAfterInline(admin.TabularInline):
    model = cms_models.ServiceCaseBeforeAfter
    extra = 1
    fields = ("title", "description", "before_image", "after_image", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Клиенты/компании
# -------------------------------
class ServiceClientCompanyInline(admin.TabularInline):
    model = cms_models.ServiceClientCompany
    extra = 1
    fields = ("name", "business_type", "logo", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Документы
# -------------------------------
class ServiceDocumentInline(admin.TabularInline):
    model = cms_models.ServiceDocument
    extra = 1
    fields = ("doc_type", "title", "file", "url", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Inline: Цены услуг
# -------------------------------
class ServicePriceItemInline(admin.TabularInline):
    model = cms_models.ServicePriceItem
    extra = 1
    fields = ("title", "price", "description", "order", "is_active")
    ordering = ("order",)

# -------------------------------
# Услуги
# -------------------------------
@admin.register(cms_models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "is_active", "order", "has_360")
    list_filter = ("organization", "is_active", "has_360")
    search_fields = ("title",)
    ordering = ("order",)
    
    # Используем кастомный шаблон для формы редактирования
    change_form_template = "admin/cms/service/change_form.html"

    fieldsets = (
        ("Основное", {
            "fields": (
                "organization",
                "title",
                "is_active",
                "order",
            )
        }),
        ("Визуал", {
            "fields": (
                "cover_image",
                "cover_video_url",
            )
        }),
        ("360°", {
            "fields": (
                "has_360",
                "view_360_url",
            )
        }),
 
    )

    inlines = [
    ServiceZoneItemInline,
    ServiceChemicalItemInline,
    ServiceEquipmentItemInline,
    ServiceFAQItemInline,
    ServiceRequirementItemInline,
    ServiceWorkConditionItemInline,
    ServiceExcludedItemInline,
    ServiceCaseBeforeAfterInline,
    ServiceClientCompanyInline,
    ServiceDocumentInline,
    ServicePriceItemInline,
]

    actions = ['duplicate_service']

    def duplicate_service(self, request, queryset):
        """Дублирование выбранных услуг со всеми связанными данными"""
        duplicated_count = 0
        
        for service in queryset:
            try:
                # Создаем копию основной услуги
                original_title = service.title
                new_title = f"{original_title} (копия)"
                
                # Генерируем уникальный slug
                base_slug = slugify(original_title) + "-copy"
                slug = base_slug
                i = 1
                while cms_models.Service.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{i}"
                    i += 1
                
                # Копируем основную услугу
                new_service = cms_models.Service.objects.create(
                    organization=service.organization,
                    title=new_title,
                    slug=slug,
                    cover_image=service.cover_image,
                    cover_video_url=service.cover_video_url,
                    has_360=service.has_360,
                    view_360_url=service.view_360_url,
                    is_active=service.is_active,
                    order=service.order,
                )
                
                # Копируем все связанные данные
                self._duplicate_related_data(service, new_service)
                
                duplicated_count += 1
                self.message_user(request, f'Услуга "{original_title}" успешно дублирована как "{new_title}"', messages.SUCCESS)
                
            except Exception as e:
                self.message_user(request, f'Ошибка при дублировании услуги "{service.title}": {str(e)}', messages.ERROR)
        
        if duplicated_count == 0:
            self.message_user(request, 'Ни одна услуга не была дублирована', messages.WARNING)
    
    duplicate_service.short_description = 'Дублировать выбранные услуги'

    def response_add(self, request, obj, post_url_continue=None):
        """Переопределяем response_add для добавления кнопки дублирования"""
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """Добавляем кнопку дублирования в форму редактирования"""
        if '_duplicate' in request.POST:
            try:
                # Создаем копию услуги
                original_title = obj.title
                new_title = f"{original_title} (копия)"
                
                # Генерируем уникальный slug
                base_slug = slugify(original_title) + "-copy"
                slug = base_slug
                i = 1
                while cms_models.Service.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{i}"
                    i += 1
                
                # Копируем основную услугу
                new_service = cms_models.Service.objects.create(
                    organization=obj.organization,
                    title=new_title,
                    slug=slug,
                    cover_image=obj.cover_image,
                    cover_video_url=obj.cover_video_url,
                    has_360=obj.has_360,
                    view_360_url=obj.view_360_url,
                    is_active=obj.is_active,
                    order=obj.order,
                )
                
                # Копируем все связанные данные
                self._duplicate_related_data(obj, new_service)
                
                self.message_user(request, f'Услуга "{original_title}" успешно дублирована как "{new_title}"', messages.SUCCESS)
                
                # Перенаправляем на страницу редактирования новой услуги
                return redirect(f'admin:cms_service_change', new_service.id)
                
            except Exception as e:
                self.message_user(request, f'Ошибка при дублировании: {str(e)}', messages.ERROR)
        
        return super().response_change(request, obj)

    def _duplicate_related_data(self, original_service, new_service):
        """Копирование всех связанных данных услуги"""
        
        # Копируем пункты по зонам
        for item in original_service.zone_items.all():
            cms_models.ServiceZoneItem.objects.create(
                service=new_service,
                zone=item.zone,
                text=item.text,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем используемые средства
        for item in original_service.chemical_items.all():
            cms_models.ServiceChemicalItem.objects.create(
                service=new_service,
                name=item.name,
                description=item.description,
                image=item.image,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем оборудование
        for item in original_service.equipment_items.all():
            cms_models.ServiceEquipmentItem.objects.create(
                service=new_service,
                name=item.name,
                description=item.description,
                image=item.image,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем FAQ
        for item in original_service.faq_items.all():
            cms_models.ServiceFAQItem.objects.create(
                service=new_service,
                question=item.question,
                answer=item.answer,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем требования к объекту
        for item in original_service.requirement_items.all():
            cms_models.ServiceRequirementItem.objects.create(
                service=new_service,
                text=item.text,
                description=item.description,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем условия выполнения работ
        for item in original_service.work_condition_items.all():
            cms_models.ServiceWorkConditionItem.objects.create(
                service=new_service,
                text=item.text,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем исключения
        for item in original_service.excluded_items.all():
            cms_models.ServiceExcludedItem.objects.create(
                service=new_service,
                text=item.text,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем кейсы до/после
        for item in original_service.cases_before_after.all():
            cms_models.ServiceCaseBeforeAfter.objects.create(
                service=new_service,
                title=item.title,
                description=item.description,
                before_image=item.before_image,
                after_image=item.after_image,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем клиентов/компании
        for item in original_service.client_companies.all():
            cms_models.ServiceClientCompany.objects.create(
                service=new_service,
                name=item.name,
                business_type=item.business_type,
                logo=item.logo,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем документы
        for item in original_service.documents.all():
            cms_models.ServiceDocument.objects.create(
                service=new_service,
                doc_type=item.doc_type,
                title=item.title,
                file=item.file,
                url=item.url,
                order=item.order,
                is_active=item.is_active
            )
        
        # Копируем цены
        for item in original_service.price_items.all():
            cms_models.ServicePriceItem.objects.create(
                service=new_service,
                title=item.title,
                price=item.price,
                description=item.description,
                order=item.order,
                is_active=item.is_active
            )
