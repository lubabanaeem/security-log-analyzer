from inspect import ismethod
from .log_parser import load_logs
from .detector import get_failed_counts, get_failed_dates
from .models import UploadedLogs, Alerts, DetectedIp, ReporttHistory

from django.shortcuts import render, redirect
from django.db import transaction
from django.urls import reverse

import hashlib
from django.contrib.auth.decorators import login_required

from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string


def get_file_hash(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


def get_record(upload, alerts_qs, detected_ip_qs):
    return {
        "total_alerts": alerts_qs.count(),
        "high_alerts": alerts_qs.filter(severity="HIGH").count(),
        "high_count": alerts_qs.filter(severity="HIGH").count(),
        "normal_count": alerts_qs.filter(severity="NORMAL").count(),
        "suspicious_ips": detected_ip_qs.count(),
        "latest_file": upload.file.name,
        "alerts": alerts_qs,
        "ips": detected_ip_qs,
        "upload": upload,
        "upload_id": upload.id,
        "report": ReporttHistory.objects.filter(uploaded_log=upload).first(),
        "top_ips": list(
            detected_ip_qs.order_by("-failed_no_attempts")[:5].values(
                "ip_adress", "failed_no_attempts"
            )
        ),
        "timeline": list(
            detected_ip_qs.order_by("first_seen_date", "first_seen_time").values(
                "ip_adress", "first_seen_date", "first_seen_time"
            )
        ),
    }


@login_required
def home(request):

    record = {}
    if request.method == "POST":
        uploaded_file = request.FILES["file"]

        try:
            if not (
                uploaded_file.name.endswith(".log")
                or uploaded_file.name.endswith(".txt")
            ):
                return render(request, "home.html", {"error": "Invalid file"})

            # Check file size (limit to 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                return render(
                    request,
                    "home.html",
                    {"error": "File too large. Maximum size is 5MB."},
                )

            # Check file content is actually plain text
            try:
                chunk = uploaded_file.read(1024)
                chunk.decode("utf-8")
                uploaded_file.seek(0)
            except UnicodeDecodeError:
                return render(
                    request,
                    "home.html",
                    {
                        "error": "Invalid file content. Only plain text files are accepted."
                    },
                )

            # Layer 2: hash must be stable
            uploaded_file.seek(0)
            file_hash = get_file_hash(uploaded_file)

            existing_upload = UploadedLogs.objects.filter(file_hash=file_hash).first()

            if existing_upload:
                alerts_qs = Alerts.objects.filter(uploaded_log=existing_upload)
                detected_ip_qs = DetectedIp.objects.filter(uploaded_log=existing_upload)

                return render(
                    request,
                    "home.html",
                    get_record(existing_upload, alerts_qs, detected_ip_qs),
                )

            file_path = f"media/{uploaded_file.name}"
            with open(file_path, "wb+") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            logs = load_logs(file_path)
            dateTime = get_failed_dates(logs)
            count = get_failed_counts(logs)

            # IMPORTANT: reset before DB + consistent file state
            uploaded_file.seek(0)

            # Layer 3: FULL atomic transaction
            with transaction.atomic():

                uploaded_obj = UploadedLogs.objects.create(
                    file=uploaded_file, file_hash=file_hash
                )

                for ip in count:

                    failed_attempts = count[ip]
                    first_seen = dateTime[ip]

                    if failed_attempts >= 3:
                        severity = "HIGH"
                        message = "Brute Force Detected"
                    else:
                        severity = "NORMAL"
                        message = "Normal Activity"

                    Alerts.objects.create(
                        uploaded_log=uploaded_obj,
                        ip_adress=ip,
                        severity=severity,
                        message=message,
                    )

                    if failed_attempts >= 3:
                        DetectedIp.objects.create(
                            uploaded_log=uploaded_obj,
                            ip_adress=ip,
                            failed_no_attempts=failed_attempts,
                            first_seen_date=first_seen[0],
                            first_seen_time=first_seen[1],
                        )

                ReporttHistory.objects.create(
                    uploaded_log=uploaded_obj,
                    total_alerts=Alerts.objects.filter(
                        uploaded_log=uploaded_obj
                    ).count(),
                )

            # Layer 1: PRG pattern (prevents POST resubmission issues)
            return redirect(f"{reverse('home')}?upload_id={uploaded_obj.id}")

        except Exception as e:
            return render(request, "home.html", {"error": str(e)})

    upload_id = request.GET.get("upload_id")

    if not upload_id:
        return render(request, "home.html", {})

    try:
        current_upload = UploadedLogs.objects.get(id=upload_id)
    except UploadedLogs.DoesNotExist:
        return render(request, "home.html", {})

    severity_filter = request.GET.get("severity")
    ip_search = request.GET.get("ip")

    alerts_qs = Alerts.objects.filter(uploaded_log=current_upload)

    if severity_filter:
        alerts_qs = alerts_qs.filter(severity=severity_filter)

    if ip_search:
        alerts_qs = alerts_qs.filter(ip_adress__icontains=ip_search)

    detected_ip_qs = DetectedIp.objects.filter(uploaded_log=current_upload)

    return render(
        request, "home.html", get_record(current_upload, alerts_qs, detected_ip_qs)
    )


@login_required
def alert_detail(request, alert_id):
    alert = Alerts.objects.get(id=alert_id)

    return render(request, "alert_detail.html", {"alert": alert})


@login_required
def export_report(request, upload_id):
    current_upload = UploadedLogs.objects.get(id=upload_id)
    alerts = Alerts.objects.filter(uploaded_log=current_upload).order_by("-severity")
    ips = DetectedIp.objects.filter(uploaded_log=current_upload)

    html_string = render_to_string(
        "report.html",
        {
            "upload": current_upload,
            "alerts": alerts,
            "ips": ips,
            "request": request,
            "high_count": alerts.filter(severity="HIGH").count(),
            "normal_count": alerts.filter(severity="NORMAL").count(),
        },
    )

    buffer = BytesIO()
    pisa.CreatePDF(html_string, dest=buffer)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="report_{upload_id}.pdf"'
    return response
