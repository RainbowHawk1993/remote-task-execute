import datetime
import psycopg2
import paramiko

DB_CONNECTION = psycopg2.connect(database="dbname", user="username", password="pass", host="hostname", port=5432)

def find_task(task_name, start_time, command):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("SELECT * from commands WHERE task_name=%s AND start_time=%s AND command=%s;",
                   (task_name, start_time, command))
    task = cursor.fetchall()

    if task:
        return task[0]
    else:
        print("No task found with the specified parameters.")
        return None

def execute_task_on_server(task, server_ip, username, password):
    if not task:
        print("No task to execute.")
        return

    command_to_execute = task[2]

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(hostname=server_ip, username=username, password=password)

    print(f"Executing command: {command_to_execute}")
    stdin, stdout, stderr = ssh_client.exec_command(command_to_execute)

    stdout_output = stdout.read().decode()
    stderr_output = stderr.read().decode()

    print("----- STDOUT -----")
    print(stdout_output)

    print("----- STDERR -----")
    print(stderr_output)

    ssh_client.close()


task = find_task(task_name="name1", start_time=datetime.datetime.now(), command="command1")

execute_task_on_server(task, server_ip="192.168.0.1", username="username1", password="password1")
