import subprocess
import os


def run_server():
    subprocess.run('venv\\Scripts\\activate && cd sneaker_store && python manage.py runserver', shell=True)


if __name__ == "__main__":
    run_server()