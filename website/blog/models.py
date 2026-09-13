from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel

class BlogIndexPage(Page):
    intro = RichTextField(blank=True, verbose_name="Описание блога")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # Чтобы избежать циклической зависимости, используем специальный метод get_children()
        # Он берет все дочерние страницы текущего индекса без импорта самого класса BlogPage!
        context['blogposts'] = self.get_children().live().specific().order_by('-first_published_at')
        
        return context


class BlogPage(Page):
    date = models.DateField("Дата публикации", auto_now_add=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Превью"
    )
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", label="Подзаголовок")),
        ('paragraph', blocks.RichTextBlock(label="Текст (абзац)")),
        ('image', ImageChooserBlock(label="Одиночное изображение")),
        ('quote', blocks.BlockQuoteBlock(label="Цитата / Важная мысль")),
    ], use_json_field=True, verbose_name="Контент статьи", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('feed_image'),
        FieldPanel('body'),
    ]

    def get_excerpt(self):
        for block in self.body:
            if block.block_type == 'paragraph':
                from django.utils.html import strip_tags
                return strip_tags(block.value.source)[:150] + "..."
        return ""
