from django.db.models import manager, Count


class HouseManager(manager.Manager):

    def get_houses_by_dragons_count(self):
        return self.objects.annotate(
            dragon_count=Count('dragons'),
        ).order_by('-dragon_count', 'name')

