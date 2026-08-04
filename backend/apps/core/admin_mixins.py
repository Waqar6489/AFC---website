"""Reusable Django Admin mixins shared across apps (CSV export, etc.)."""

import csv

from django.http import HttpResponse


class CSVExportMixin:
    """Adds a 'Export selected as CSV' bulk action to any ModelAdmin.
    Set `csv_export_fields = [...]` on the admin class to control which
    fields are included; defaults to all concrete model fields."""

    csv_export_fields = None
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        fields = self.csv_export_fields or [f.name for f in self.model._meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f"attachment; filename={self.model._meta.model_name}_export.csv"
        )

        writer = csv.writer(response)
        writer.writerow(fields)
        for obj in queryset:
            writer.writerow([getattr(obj, field, "") for field in fields])
        return response

    export_as_csv.short_description = "Export selected as CSV"
