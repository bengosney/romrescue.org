# Django
from django.http import HttpResponse

# Third Party
import unicodecsv as csv
from future.types.newstr import unicode


def export_as_csv_action(description="Export selected objects as CSV file", fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta

        field_names = [field.name for field in opts.fields] if not fields else fields
        response = HttpResponse()
        response['content_type'] = 'text/csv'
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response, encoding='utf-8')
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = description

    return export_as_csv
