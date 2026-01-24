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
for values in ip_count:
    print(values, "->",ip_count[values], "failed login attempts")
   


        





