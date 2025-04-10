from django.db.models import manager, Count


class LabelManager(manager.Manager):
    def get_labels_by_albums_count(self):
        return self.annotate(
            album_count=Count('album')
        ).order_by('-album_count', 'name')
