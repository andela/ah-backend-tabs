from django.db import models
from authors.apps.authentication.models import User
from django.utils import timezone


class Connect(models.Model):
    user_from = models.ForeignKey(User, related_name = "rel_from_set", on_delete = models.CASCADE, blank = True)
    user_to = models.ForeignKey(User, related_name = "rel_to_set", on_delete = models.CASCADE, blank = True)
    created = models.DateTimeField(editable = False)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} is following {}'.format(self.user_from.username, self.user_to.username)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            connection_class = self.__class__
            con_exists = connection_class.objects.filter(user_from = self.user_from).filter(user_to = self.user_to)
            if not con_exists:
                return super(Connect, self).save(*args, **kwargs)


User.add_to_class("following", models.ManyToManyField('self', through = Connect, related_name = "followers", symmetrical = False))




