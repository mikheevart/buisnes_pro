from django.db import models
from django.apps import apps
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    # Поля для секции Hero
    hero_title = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name="Заголовок Hero"
    )
    hero_subtitle = models.TextField(
        blank=True, 
        verbose_name="Подзаголовок Hero"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновая картинка Hero"
    )

    # Настраиваем отображение полей в админке Wagtail
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Ленивое получение модели статей блога для вывода новостей на главной
        try:
            BlogPageModel = apps.get_model('blog', 'BlogPage')
            context['latest_posts'] = BlogPageModel.objects.live().order_by('-first_published_at')[:3]
        except LookupError:
            context['latest_posts'] = []
        return context
