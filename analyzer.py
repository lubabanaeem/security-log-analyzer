with open("sample.log","r") as file:
    logs = file.readlines()


ip_count = {}
for line in logs:
    if "Failed login" in line:
        my_list = line.split(" ")
        ip = my_list[-1].strip()
        
        if ip in ip_count:
            ip_count[ip] = ip_count[ip]+1
        else:
            ip_count[ip] = 1
threshold = 3
for ips in ip_count:
    if ip_count[ips] >= threshold:
        print("[ALERT]",ips, "->",ip_count[ips], "failed login attempts")
    else:
        print("[NORMAL]",ips, "->",ip_count[ips], "failed login attempts")

    
   


        





