import subprocess
import argparse

def run_ansible_playbook(data_file, playbook_file):
    # Команда для запуска Ansible Playbook
    command = [
        "ansible-playbook",
        playbook_file,
        "--extra-vars",
        f"@{data_file}"
    ]

    try:
        # Выполнение команды
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Playbook executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while running playbook:")
        print(e.stderr)

if __name__ == "__main__":
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Run Ansible playbook for configuration generation.")
    parser.add_argument(
        "--data-file",
        required=True,
        help="Path to the data YAML file (e.g., deployments/data.yml)"
    )
    parser.add_argument(
        "--playbook",
        default="playgroundengine/nokia/generate_config.yml",
        help="Path to the Ansible playbook file (default: playgroundengine/nokia/generate_config.yml)"
    )
    args = parser.parse_args()

    # Запуск Ansible Playbook с переданными аргументами
    run_ansible_playbook(args.data_file, args.playbook)
