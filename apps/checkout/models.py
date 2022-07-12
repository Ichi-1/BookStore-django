from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):
    """
    The Delivery options table
    """
    DELIVERY_CHOISES = [
        ('IS', 'In Store'),
        ('HD', 'Home Delivery'),
        ('DD', 'Digital Delivery'),
    ]

    name = models.CharField(
        verbose_name=_('Delivery name'),
        help_text=_('Required'),
        max_length=255,
    )
    price = models.DecimalField(
        verbose_name=_('Delivery price'),
        help_text=_('Maximum 999.99'),
        max_digits=5,
        decimal_places=2,
        error_messages={
            'name':{
                'max_length':_('The price must be between 0 and 999.99'),
            },
        },
    )
    method = models.CharField(
        choices=DELIVERY_CHOISES,
        verbose_name=_('Delivery method'),
        help_text=_('Required'),
        max_length=255,
    )
    timeframe = models.CharField(
        verbose_name=_('Delivery timeframe'),
        help_text=_('Required'),
        max_length=255,
    )
    window = models.CharField(
        verbose_name=_('Delivery window'),
        help_text=_('Required'),
        max_length=255,
    )
    order = models.IntegerField(
        verbose_name=_('List Order'),
        help_text=_('Required'),
        default=0,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Delivery Option')
        verbose_name_plural = _('Delivery Options')

    def __str__(self):
        return self.name


class PaymentSelection(models.Model):
    """
    The Payment options table
    """
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('required'),
        max_length=255,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Payment Selection')
        verbose_name_plural = _('Payment Selections')
    
    def __str__(self):
        return self.name