import subprocess
import argparse
import os

def list_available_files(directory):
    """List available files in the specified directory."""
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return []
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def run_ansible_playbook(data_file, playbook_file):
    """Run the specified Ansible playbook with the provided data file."""
    command = [
        "ansible-playbook",
        playbook_file,
        "--extra-vars",
        f"@{data_file}",
        "-i", "localhost,"
    ]

    try:
        print(f"Running command: {' '.join(command)}")  # For debugging
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Playbook executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while running playbook:")
        print(e.stderr)
        print("Command that failed:")
        print(" ".join(command))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Ansible playbook for configuration generation.")
    
    # Argument to list available files
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="List available templates or playbooks."
    )

    # Arguments for template, playbook, and data file
    parser.add_argument("--template", required=True, help="Template file name (e.g., router_config.j2).")
    parser.add_argument("--playbook", required=True, help="Playbook file name (e.g., generate_config.yml).")
    parser.add_argument(
        "--data-file",
        help="Path to the data YAML file (e.g., deployments/data.yml)."
    )

    args = parser.parse_args()

    # Base directories
    templates_dir = ""
    playbooks_dir = ""
    data_dir = ""

    if args.list_files:
        print("Available templates:")
        print("\n".join(list_available_files(templates_dir)))
        print("\nAvailable playbooks:")
        print("\n".join(list_available_files(playbooks_dir)))
    else:
        # Construct file paths
        template_file = os.path.join(templates_dir, args.template)
        playbook_file = os.path.join(playbooks_dir, args.playbook)
        data_file = args.data_file or os.path.join(data_dir, "data.yml")

        # Check if files exist
        if not os.path.exists(template_file):
            print(f"Template file '{template_file}' does not exist.")
            exit(1)
        if not os.path.exists(playbook_file):
            print(f"Playbook file '{playbook_file}' does not exist.")
            exit(1)
        if not os.path.exists(data_file):
            print(f"Data file '{data_file}' does not exist.")
            exit(1)

        print(f"Using template: {template_file}")
        print(f"Using playbook: {playbook_file}")
        print(f"Using data file: {data_file}")

        run_ansible_playbook(data_file, playbook_file)
