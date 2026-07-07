

def generate_report(failed_ip_counts,first_seen_time,threshold):
    alerts = []

    for ip in failed_ip_counts:
     if failed_ip_counts[ip] >= threshold:
        alert = f"[ALERT] IP {ip} first seen at {first_seen_time[ip]} -> detected with {failed_ip_counts[ip]} failed login attempts (exceeded threshold,possible brute-force attack)"
        alerts.append(alert)
     else:
        normal = f"[NORMAL] IP {ip} first seen at {first_seen_time[ip]} -> detected with {failed_ip_counts[ip]} failed login attempts"
        alerts.append(normal)

    return alerts

 