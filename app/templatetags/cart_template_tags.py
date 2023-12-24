from django import template
from app.models import Order

register = template.Library()

@register.filter
def NavCart(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    else:
        return 0