from django.db.models import manager, Count


class ProfileManager(manager.Manager):
    def get_regular_customers(self):
        return self.annotate(
            count_orders=Count('order'),
        ).filter(count_orders__gt=2).order_by('-count_orders')
