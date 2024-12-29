import os
import sys
import argparse
import subprocess
from datetime import datetime

AUDIT_LOG = "playgroundengine.log"
PLAYGROUND_VERSION = "v0.1"
PLAYBOOK_DIR="playgroundengine/src/playbooks/"

def write_audit_log_entry(args):
    """Write an entry to the audit log."""
    with open(AUDIT_LOG, "a") as log_file:
        log_file.write(f"{datetime.now()} PLAYGROUND {PLAYGROUND_VERSION} {args}\n")

def audit_log_and_exit(exit_code):
    """Write exit status to the audit log and exit."""
    with open(AUDIT_LOG, "a") as log_file:
        log_file.write(f"{datetime.now()} PLAYGROUND {PLAYGROUND_VERSION} exit code {exit_code}\n")
    sys.exit(exit_code)

def run_ansible_playbook(playbook_path, vendor, subvendor):
    """Run the specified Ansible playbook."""
    if not os.path.isabs(playbook_path):
        playbook_path = os.path.join(os.path.dirname(__file__), PLAYBOOK_DIR, playbook_path)

    command = [
        "ansible-playbook",
        playbook_path,
        "-e", f"vendor={vendor}",
        "-e", f"subvendor={subvendor}",
        "-i", "localhost"
    ]

    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)

def main():
    parser = argparse.ArgumentParser(description="Playground Engine CLI")
    parser.add_argument("-v", "--vendor", required=True, help="Specify the vendor (e.g., nokia, arista, juniper).")
    parser.add_argument("-s", "--subvendor", required=True, help="Specify the subvendor (e.g., srl, eos).")
    parser.add_argument("-d", "--playbook", required=True, default=os.path.join(os.path.dirname(__file__), PLAYBOOK_DIR, 'generate_config.yml'), help="Path to the Ansible playbook.")
    parser.add_argument("--ansible-help", action="store_true", help="Show Ansible help.")

    args = parser.parse_args()

    if args.ansible_help:
        subprocess.run(["ansible-playbook", "--help"], check=True)
        sys.exit(0)

    write_audit_log_entry(sys.argv)

    try:
        run_ansible_playbook(args.playbook, args.vendor, args.subvendor)
    except subprocess.CalledProcessError as e:
        audit_log_and_exit(e.returncode)

    audit_log_and_exit(0)

if __name__ == "__main__":
    main()
