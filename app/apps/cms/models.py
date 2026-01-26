from django.db import models
from django.utils.text import slugify
import uuid
from django_resized import ResizedImageField

# -------------------------------
# Категории организаций
# -------------------------------
class CategoryOrganization(models.Model):
    """
    Тип бизнеса / категория организации: офисы, кафе, медцентры и т.д.
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    image = ResizedImageField(
        force_format="WEBP",
        quality=100,
        upload_to="category_image/",
        verbose_name="Фотография",
        blank=True,
        null=True,
    )
    descriptions = models.TextField(verbose_name="Описание", blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "1) Категория организации"
        verbose_name_plural = "1) Категории организаций"
        ordering = ["order", "name"]
# -------------------------------
# Услуги
# -------------------------------
class Service(models.Model):
    organization = models.ForeignKey(
        "CategoryOrganization",
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Категория организации",
    )

    title = models.CharField(max_length=255, verbose_name="Название услуги")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    cover_image = ResizedImageField(
        force_format="WEBP",
        quality=95,
        upload_to="services/covers/",
        blank=True,
        null=True,
        verbose_name="Обложка (фото)",
    )
    cover_video_url = models.URLField(blank=True, verbose_name="Видео (URL)")

    has_360 = models.BooleanField(default=False, verbose_name="Есть 360°")
    view_360_url = models.URLField(blank=True, verbose_name="Ссылка на 360°")

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Авто-slag, если пустой
        if not self.slug:
            base = slugify(self.title)
            if not base:
                base = f"service-{uuid.uuid4().hex[:8]}"
            slug = base
            i = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

# -------------------------------
# Пункты по зонам
# -------------------------------
class ServiceZoneItem(models.Model):
    ZONE_CHOICES = (
        ("room", "Комната"),
        ("kitchen", "Кухня"),
        ("bath_wc", "Ванная и туалет"),
        ("hall", "Прихожая / входная группа"),
        ("office", "Офис / рабочая зона"),
        ("warehouse", "Склад / подсобка"),
        ("other", "Другое"),
    )

    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="zone_items",
        verbose_name="Услуга",
    )

    zone = models.CharField(
        max_length=30,
        choices=ZONE_CHOICES,
        verbose_name="Зона",
    )

    text = models.CharField(
        max_length=255,
        verbose_name="Пункт",
        help_text="Один пункт = одна строка (например: Удаление пыли со всех поверхностей)",
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Пункт по зонам"
        verbose_name_plural = "Пункты по зонам"
        ordering = ["zone", "order", "id"]

    def __str__(self):
        return f"{self.get_zone_display()}: {self.text}"


# -------------------------------
# Используемые средства
# -------------------------------
class ServiceChemicalItem(models.Model):
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="chemical_items",
        verbose_name="Услуга",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Название средства",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Где и для чего применяется",
        help_text="Например: Для кухни, удаления жира, рабочих поверхностей",
    )

    image = ResizedImageField(
        force_format="WEBP",
        quality=90,
        upload_to="services/chemicals/",
        blank=True,
        null=True,
        verbose_name="Фотография средства",
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Используемое средство"
        verbose_name_plural = "Используемые средства"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

# -------------------------------
# Используемые оборудование
# -------------------------------
class ServiceEquipmentItem(models.Model):
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="equipment_items",
        verbose_name="Услуга",
    )

    name = models.CharField(max_length=255, verbose_name="Название оборудования")
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Для чего используется / преимущества",
        help_text="Например: Для глубокой химчистки мебели, мощное всасывание",
    )

    image = ResizedImageField(
        force_format="WEBP",
        quality=90,
        upload_to="services/equipment/",
        blank=True,
        null=True,
        verbose_name="Фотография оборудования",
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Оборудование (услуги)"
        verbose_name_plural = "Оборудование (услуг)"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

# -------------------------------
# Часто задаваемые вопросы
# -------------------------------
class ServiceFAQItem(models.Model):
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="faq_items",
        verbose_name="Услуга",
    )

    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ответ",
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "FAQ (услуги)"
        verbose_name_plural = "FAQ (услуг)"
        ordering = ["order", "id"]

    def __str__(self):
        return self.question

# -------------------------------
# Требования к объекту
# -------------------------------
class ServiceRequirementItem(models.Model):
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE,
        related_name="requirement_items",
        verbose_name="Услуга"
    )
    text = models.CharField(max_length=255, verbose_name="Требование")
    description = models.CharField(max_length=500, verbose_name="Описание", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Требование к объекту"
        verbose_name_plural = "Требования к объекту"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text

# -------------------------------
# Условия выполнения работ (пункты)
# -------------------------------
class ServiceWorkConditionItem(models.Model):
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE,
        related_name="work_condition_items",
        verbose_name="Услуга"
    )
    text = models.CharField(max_length=255, verbose_name="Условие")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Условие выполнения работ"
        verbose_name_plural = "Условия выполнения работ"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text

# -------------------------------
# Что НЕ входит (пункты)
# -------------------------------
class ServiceExcludedItem(models.Model):
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE,
        related_name="excluded_items",
        verbose_name="Услуга"
    )
    text = models.CharField(max_length=255, verbose_name="Не входит в услугу")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Не входит (пункт)"
        verbose_name_plural = "Что НЕ входит"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text

# -------------------------------
# Кейсы / До-после
# -------------------------------
class ServiceCaseBeforeAfter(models.Model):
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE,
        related_name="cases_before_after",
        verbose_name="Услуга"
    )
    title = models.CharField(max_length=255, verbose_name="Название кейса")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Короткое описание")

    before_image = ResizedImageField(
        force_format="WEBP", quality=90,
        upload_to="services/cases/before/",
        blank=True, null=True,
        verbose_name="Фото ДО"
    )
    after_image = ResizedImageField(
        force_format="WEBP", quality=90,
        upload_to="services/cases/after/",
        blank=True, null=True,
        verbose_name="Фото ПОСЛЕ"
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Кейс До/После"
        verbose_name_plural = "Кейсы До/После"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

# -------------------------------
# Кто уже заказывал (логотип + название)
# -------------------------------
class ServiceClientCompany(models.Model):
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE,
        related_name="client_companies",
        verbose_name="Услуга"
    )
    name = models.CharField(max_length=255, verbose_name="Название компании")
    business_type = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Тип бизнеса (опционально)"
    )
    logo = ResizedImageField(
        force_format="WEBP", quality=90,
        upload_to="services/clients/logos/",
        blank=True, null=True,
        verbose_name="Логотип"
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Компания-клиент"
        verbose_name_plural = "Кто уже заказывал"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

# -------------------------------
# Документы (договор/счёт/акт)
# -------------------------------
class ServiceDocument(models.Model):
    DOC_TYPE_CHOICES = (
        ("contract", "Договор"),
        ("invoice", "Счёт"),
        ("act", "Акт"),
        ("other", "Другое"),
    )

    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Услуга"
    )
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, verbose_name="Тип документа")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (опционально)")

    file = models.FileField(
        upload_to="services/documents/",
        blank=True, null=True,
        verbose_name="Файл"
    )
    url = models.URLField(blank=True, null=True, verbose_name="Ссылка (если файл хранится где-то)")

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Документ услуги"
        verbose_name_plural = "Документы услуги"
        ordering = ["order", "id"]

    def __str__(self):
        return self.get_doc_type_display()

# -------------------------------
# Цены услуг
# -------------------------------
class ServicePriceItem(models.Model):
    service = models.ForeignKey(
        "Service", 
        on_delete=models.CASCADE,
        related_name="price_items",
        verbose_name="Услуга"
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Например: Генеральная уборка до 50 м²"
    )
    
    price = models.CharField(
        max_length=100,
        verbose_name="Стоимость",
        help_text="Например: от 15 000 сом или договорная"
    )
    
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Дополнительная информация о цене"
    )
    
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Цена услуги"
        verbose_name_plural = "Цены услуг"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title}: {self.price}"