from django.contrib.auth.models import User
from django.db import models


class Gift(models.Model):
    """A gift someone wants their friends to pay for."""
    DRAFT = 'draft'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    DELETED = 'deleted'
    STATUS_CHOICES = (
        (DRAFT, DRAFT),
        (ACTIVE, ACTIVE),
        (COMPLETED, COMPLETED),
        (DELETED, DELETED),
    )
    VISIBLE_STATUSES = (ACTIVE, COMPLETED,)

    user = models.ForeignKey(User)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='uploads/gift_images/', blank=True)

    gift_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_ts',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'pony.gifts.views.detail', [self.id]
