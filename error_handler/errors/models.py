from django.contrib.postgres.fields import ArrayField
from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field


class ErrorType(models.Model):
    parent_error = models.ForeignKey(
        "self", related_name="children", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=250, null=True)
    resolved = models.BooleanField(default=False)
    error_description = models.TextField()
    notification_description = models.TextField()
    classes = ArrayField(models.CharField(max_length=250, blank=True))
    solutions = ArrayField(models.TextField())

    @property
    @extend_schema_field(OpenApiTypes.BOOL)
    def has_children(self) -> bool:
        return self.children.exists()

    def get_parent_list(self):
        res = []
        obj = self
        while obj.parent_error:
            res.append(obj.parent_error)
            obj = obj.parent_error
        return res


class Error(models.Model):
    eid = models.CharField(max_length=32)
    type = models.ForeignKey(
        "ErrorType", related_name="entries", on_delete=models.CASCADE
    )
    params = ArrayField(models.CharField(max_length=250, blank=True))
    created = models.DateTimeField()
    filtered = models.TextField()
    body = models.TextField()

    class Meta:
        ordering = ["-created"]
