from django.contrib import admin

# Register your models here.
from .models import(
    UploadedLogs,
    Alerts,
    DetectedIp,
    ReporttHistory
)

admin.site.register(UploadedLogs)
admin.site.register(Alerts)
admin.site.register(DetectedIp)
admin.site.register(ReporttHistory)
