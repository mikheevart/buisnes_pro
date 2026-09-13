from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

# Главная страница каталога (содержит список всех услуг)
class ServiceIndexPage(Page):
    intro = RichTextField(blank=True, verbose_name="Вводный текст")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    # Метод для передачи дочерних страниц услуг в HTML-шаблон
    def get_context(self, request):
        context = super().get_context(request)
        context['services'] = ServicePage.objects.child_of(self).live()
        return context

# Страница конкретной услуги
class ServicePage(Page):
    description = RichTextField(verbose_name="Описание услуги")
    price = models.CharField(max_length=100, verbose_name="Стоимость", default="от 10 000 ₽")
    icon_name = models.CharField(max_length=50, verbose_name="Иконка UIkit (например: laptop, cart)", default="laptop")

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('icon_name'),
    ]
