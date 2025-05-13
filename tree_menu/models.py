from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    name = models.CharField('Название меню', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE
    )
    title = models.CharField('Название пункта', max_length=100)
    url = models.CharField(
        'URL или name URL',
        max_length=200,
        help_text="Может быть абсолютный URL или name для реверса",
    )
    named_url = models.BooleanField(
        'URL это name для реверса?', default=False,
    )
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ('order',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.url)
            except NoReverseMatch:
                return "#url-not-found"
        return self.url