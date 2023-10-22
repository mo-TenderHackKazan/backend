from django.db.models.signals import post_save
from django.dispatch import receiver

from error_handler.crm.models import ErrorDateAmount, ErrorSummery
from error_handler.errors.models import Error


@receiver(post_save, sender=Error)
def tag_create(sender, instance: Error, created, **kwargs):
    if created:
        for error_type in [instance.type] + instance.type.get_parent_list():
            s = ErrorDateAmount.objects.get_or_create(
                date=instance.created.date(), error=error_type
            )[0]
            s.amount += 1
            s.save()
            try:
                s = error_type.entries_summery.first()
                s.amount += 1
                if instance.created > s.last_entry:
                    s.last_entry = instance.created
                s.save()
            except (ErrorSummery.DoesNotExist, AttributeError):
                ...
