with open("sample.log","r") as file:
    logs = file.readlines()

for lines in logs:
    print(lines.strip())




