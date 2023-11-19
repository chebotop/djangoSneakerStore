import subprocess
import os

def run_server():
    subprocess.run('venv\\Scripts\\activate', shell=True)
    os.system("cd sneaker_store")

    command = "cd sneaker_store && python manage.py runserver"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    run_server()