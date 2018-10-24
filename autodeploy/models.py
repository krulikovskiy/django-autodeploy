from django.db import models


class Release(models.Model):
    STATUS = (
        ('wait', 'Ожидает релиза'),
        ('success', 'Релиз прошёл успешно')
    )

    status = models.CharField(verbose_name='Статус', choices=STATUS, max_length=1)
    commit = models.CharField(verbose_name='Действие', max_length=255)
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
