#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления slug у существующих услуг
"""
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.cms.models import Service

def fix_slugs():
    """Исправление slug для всех услуг без slug"""
    services_without_slug = Service.objects.filter(slug__isnull=True) | Service.objects.filter(slug='')
    
    print(f"🔧 Найдено услуг без slug: {services_without_slug.count()}")
    
    for service in services_without_slug:
        service.save()  # Это вызовет автоматическую генерацию slug
        print(f"   ✅ Сгенерирован slug для {service.title}: {service.slug}")
    
    # Проверяем все услуги
    all_services = Service.objects.all()
    print(f"\n📊 Всего услуг в базе: {all_services.count()}")
    print(f"✅ Услуг с slug: {all_services.exclude(slug__isnull=True).exclude(slug='').count()}")
    
    print("\n🚀 Slug исправлены! Теперь услуги должны отображаться на сайте.")

if __name__ == "__main__":
    fix_slugs()

# Вызов функции при запуске через shell
fix_slugs()
