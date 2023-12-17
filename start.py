import subprocess
import os

def run_server():
    subprocess.run('cd sneaker_store && venv\\Scripts\\activate && python manage.py runserver', shell=True)

if __name__ == "__main__":
    run_server()