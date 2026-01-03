from django.db import models
from django_resized.forms import ResizedImageField 
# Create your models here.
class Settings(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название сайта")
    descriptions = models.TextField(verbose_name="Информационный текст", blank=True, null=True)
    logo = ResizedImageField(force_format="WEBP", quality=100,upload_to="logo/", verbose_name="Логотип")
    icon = ResizedImageField(force_format="WEBP", quality=100,upload_to="logo/", verbose_name="Иконка сайта")
    phone = models.CharField(max_length=255, verbose_name='Телефон номер')
    email = models.EmailField(max_length=255, verbose_name='Почта', blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name='Адрес')
    instagram = models.URLField(verbose_name='Instagram URL', blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "1) Основная настройка"
        verbose_name_plural = "1) Основные настройки"

class Banner(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    subtitle = models.CharField(max_length=255, verbose_name="Подзаголовок", blank=True, null=True)
    image = ResizedImageField(force_format="WEBP", quality=100,upload_to="banner/", verbose_name="Фотография")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "2) Баннер"
        verbose_name_plural = "2) Баннеры"