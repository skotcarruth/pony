from datetime import datetime
from decimal import Decimal

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
    PUBLIC_VISIBLE_STATUSES = (ACTIVE, COMPLETED,)
    CREATOR_VISIBLE_STATUSES = (DRAFT, ACTIVE, COMPLETED,)

    user = models.ForeignKey(User, null=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='uploads/gift_images/', blank=True)

    shared = models.BooleanField(default=False)

    gift_date = models.DateField(null=True, blank=True)
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

    @property
    def is_completed(self):
        """Is the gift completed and ready to be disbursed?"""
        return self.gift_date <= datetime.utcnow().date()

    def amount_raised(self):
        """Totals the amount chipped in for this gift by friends."""
        ### TODO: implement
        return Decimal('1234.56')

    def visible_to_user(self, user):
        """Returns true if the given user can see this gift."""
        if user == self.user:
            return self.status in self.CREATOR_VISIBLE_STATUSES
        return self.status in self.PUBLIC_VISIBLE_STATUSES
