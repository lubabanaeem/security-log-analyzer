
def get_failed_counts(log_data):

    ip_count = {}
    for line in log_data:
        if "Failed login" in line:
            parts = line.split(" ")
            ip = parts[-1].strip()
        
        
            if ip in ip_count:
                ip_count[ip] = ip_count[ip]+1
            else:
              ip_count[ip] = 1
    return ip_count

def get_failed_dates(log_data):
    ip_date = {}
    for line in log_data:
        if "Failed login" in line:
            parts= line.split(" ")
            ip = parts[-1].strip()
            date = parts[0].strip()
            time = parts[1].strip()

            if ip not in ip_date:
                ip_date[ip] = (date,time)
    return ip_date
               
