from django.db import models


LEVEL_CHOICES = [
    ('DEBUG', 'DEBUG'),
    ('WARNING', 'WARNING'),
    ('ERROR', 'ERROR'),
]


class Log(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    details = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    origin = models.GenericIPAddressField(protocol='IPv4')
    events = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.description} - ({self.id})'
