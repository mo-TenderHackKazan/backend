from django.db import models


class ErrorDateAmount(models.Model):
    date = models.DateField()
    error = models.ForeignKey("errors.ErrorType", on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        unique_together = [("date", "error")]


class ErrorSummery(models.Model):
    parent = models.ForeignKey(
        "self", related_name="children", null=True, on_delete=models.SET_NULL
    )
    type = models.ForeignKey(
        "errors.ErrorType", related_name="entries_summery", on_delete=models.CASCADE
    )
    first_entry = models.DateTimeField()
    last_entry = models.DateTimeField()
    amount = models.IntegerField(default=0)

    class Meta:
        ordering = ["-last_entry"]
