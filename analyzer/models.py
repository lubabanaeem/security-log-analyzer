from django.db import models

# Create your models here.
class UploadedLogs(models.Model):
    file = models.FileField(upload_to='logs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.file.name
    
class Alerts(models.Model):
    uploaded_log = models.ForeignKey(
        UploadedLogs,on_delete=models.CASCADE
        )
    ip_adress = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_adress
    
class DetectedIp(models.Model):
    uploaded_log = models.ForeignKey(
        UploadedLogs,on_delete=models.CASCADE
    )

    ip_adress = models.CharField(max_length=50)
    failed_no_attempts = models.IntegerField()
    first_seen_date = models.CharField(max_length=50)
    first_seen_time = models.CharField(max_length=50)

    def __str__(self):
        return self.ip_adress
    
class ReporttHistory(models.Model):
    uploaded_log = models.ForeignKey(
        UploadedLogs,on_delete=models.CASCADE
    )

    generated_at = models.DateTimeField(auto_now_add=True)
    total_alerts = models.IntegerField()

    def __str__(self):
        return f"Report {self.id}"
    