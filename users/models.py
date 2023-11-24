from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class AdminProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="admin_profile",
                                verbose_name="Пользователь",
                                )
    patronymic = models.TextField(blank=True,
                                  null=True,
                                  verbose_name="Отчество",
                                  )
    birthday = models.DateField(blank=True,
                                null=True,
                                verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Поля администратора"
        verbose_name_plural = "Поля администраторов"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if (created or not hasattr(instance, "admin_profile")) and instance.is_staff:
        AdminProfile.objects.create(user=instance)
    if instance.is_staff:
        instance.admin_profile.save()
