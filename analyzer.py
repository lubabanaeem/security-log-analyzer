
def load_logs():
    with open("sample.log","r") as file:
      logs = file.readlines()
      return logs
    
log_data = load_logs()

def get_failed_counts(log_data):

    ip_count = {}
    for line in log_data:
        if "Failed login" in line:
            my_list = line.split(" ")
            ip = my_list[-1].strip()
        
        
            if ip in ip_count:
                ip_count[ip] = ip_count[ip]+1
            else:
              ip_count[ip] = 1
    return ip_count
    
def get_failed_dates(log_data):
    ip_date = {}
    for line in log_data:
        if "Failed login" in line:
            my_list = line.split(" ")
            ip = my_list[-1].strip()
            date = my_list[0].strip()
            time = my_list[1].strip()

            if ip not in ip_date:
                ip_date[ip] = (date,time)
    return ip_date
               
failed_ip_counts = get_failed_counts(log_data)
first_seen_time = get_failed_dates(log_data)
def get_report(failed_ip_counts,first_seen_time):
 threshold = 3
 for ip in failed_ip_counts:
    if failed_ip_counts[ip] >= threshold:
        print("[ALERT]","IP", ip,"first seen at:",first_seen_time[ip], "-> detected with",failed_ip_counts[ip], "failed login attempts (exceeded threshold,possible brute-force attack)")
    else:
        print("[NORMAL] ","IP",ip,"first seen at:",first_seen_time[ip], "-> detected with" ,failed_ip_counts[ip], "failed login attempts")

get_report(failed_ip_counts,first_seen_time)  


        





