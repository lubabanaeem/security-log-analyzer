def load_logs(path):
    with open(path, "r") as file:
        logs = file.readlines()
    return logs