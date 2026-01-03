from django.contrib import admin
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
# Услуги
# -------------------------------
@admin.register(cms_models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "is_active", "order", "has_360")
    list_filter = ("organization", "is_active", "has_360")
    search_fields = ("title",)
    ordering = ("order",)

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
]
