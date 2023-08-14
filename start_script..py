import subprocess

def run_server():
    # Активируем виртуальное окружение
    subprocess.run("/venv/scripts/activate", shell=True)

    # Запускаем сервер Django
    subprocess.run("python sneaker_store/manage.py runserver", shell=True)

if __name__ == "__main__":
    run_server()
