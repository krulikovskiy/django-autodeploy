from django.db import models


class Release(models.Model):
    STATUS = (
        ('wait', 'Ожидает релиза'),
        ('success', 'Релиз прошёл успешно'),
        ('error', 'Ошибка при релизе'),
        ('missing', 'Пропущен'),
    )

    status = models.CharField(verbose_name='Статус', choices=STATUS, max_length=1, default='wait')
    commit = models.CharField(verbose_name='Действие', max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
