import os
import sys
import yaml
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

"""
Playground CLI
See README.md for more information

Usage:
playgroundengine <workflow> [deployment] [options]
            
    workflow:     playground workflows, e.g. build, deploy, generate-config
    deployment:   Name of the project's environment workflow to run, e.g. 'project-A'
    options:
        -h, --help:            Displays this help.
        -v, -vv, -vvv, -vvvv:  Runs with increasing levels of verbosity.
        --list:                Shows a list of all supported workflows.
"""

PLAYGROUND_VERSION = "v0.1"
AUDIT_LOG = "reports/playgroundengine.log"
PLAYBOOK_DIR = "playgroundengine/src/playbooks/"
#PLAYBOOK_DIR = os.path.join(os.path.dirname(__file__), 'src', 'playbooks')
DEPLOYMENT_DIR = "deployments/"
PLAYBOOK_BUILD = ""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(AUDIT_LOG),
        logging.StreamHandler()
    ]
)

def write_audit_log_entry(args):
    """Write an entry to the audit log."""
    logging.info(f"PLAYGROUND {PLAYGROUND_VERSION} {args}")

def audit_log_and_exit(exit_code):
    """Write exit status to the audit log and exit."""
    if exit_code == 0:
        logging.info(f"PLAYGROUND {PLAYGROUND_VERSION} exit code {exit_code}")
    else:
        logging.error(f"PLAYGROUND {PLAYGROUND_VERSION} exit code {exit_code}")
    sys.exit(exit_code)

def run_ansible_playbook(playbook_path, vars_file_path):
    """Run the specified Ansible playbook with a vars file."""
    if not os.path.isfile(playbook_path):
        print(f"Error: Playbook '{playbook_path}' does not exist.")
        sys.exit(1)

    command = [
        "ansible-playbook",
        playbook_path,
        "-e", f"@{vars_file_path}",
        "-i", "localhost,"
    ]

    print(f"Running: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Ansible playbook execution failed with return code {e.returncode}")
        audit_log_and_exit(e.returncode)

def load_build_vars(file_path):
    """Load variables from the build_vars.yml file."""
    if not os.path.exists(file_path):
        print(f"Error: Build variables file not found: {file_path}")
        sys.exit(1)
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def create_project_dir(project_name):
    """Create the project directory."""
    project_dir = os.path.join("deployments", project_name)
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f"Created project directory: {project_dir}")
    else:
        print(f"Project directory already exists: {project_dir}")
    return project_dir

def create_vars_file(vars_data, vars_file_path):
    """Create project directory if not exists"""
    os.makedirs(os.path.dirname(vars_file_path), exist_ok=True)
    
    """Create a vars file for Ansible playbook."""
    with open(vars_file_path, "w") as file:
        yaml.dump(vars_data, file)
    print(f"Created vars file: {vars_file_path}")

def generate_config_file(project_name, vars_file_path):
    """Generate a config file from vars.yml in the clabconfigs directory."""
    config_dir = os.path.join("deployments", project_name, "clabconfigs")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Created config directory: {config_dir}")
    config_file_path = os.path.join(config_dir)

    with open(vars_file_path, "r") as vars_file:
        vars_data = yaml.safe_load(vars_file)

    vendor = vars_data.get("vendor")
    if not vendor:
        print("Error: 'vendor' not found in vars.yml")
        sys.exit(1)

    playbook_path = os.path.join(PLAYBOOK_DIR, "generate_config.yml")
    run_ansible_playbook(playbook_path, vars_file_path)
    print(f"Generated config file: {config_file_path}")

def build_action(config_file: str):
    """Handle the 'build' action."""
    build_vars = load_build_vars(config_file)
    project_name = build_vars.get("project_name")
    topology_schema = build_vars.get("topology_schema")
    if not project_name:
        logging.error("'project_name' not found in config file")
        sys.exit(1)
    if not topology_schema:
        logging.error("'topology_schema' not found in config file")
        sys.exit(1)
    
    create_project_dir(project_name)

    vars_file_path = os.path.join("deployments", project_name, "vars.yml")
    create_vars_file(build_vars, vars_file_path)

    playbook_path = os.path.join(PLAYBOOK_DIR, "build.yml")
    logging.info(f"Playbook Path: {playbook_path}")
    run_ansible_playbook(playbook_path, vars_file_path)

def generate_config_action(config_file: str):
    """Handle the 'generate-config' action."""
    build_vars = load_build_vars(config_file)
    project_name = build_vars.get("project_name")
    if not project_name:
        logging.error("'project_name' not found in config file")
        sys.exit(1)

    vars_file_path = os.path.join("deployments", project_name, "vars.yml")
    create_vars_file(build_vars, vars_file_path)

    generate_config_file(project_name, vars_file_path)

def main():
    parser = argparse.ArgumentParser(description="Playground Engine CLI")
    parser.add_argument("action", type=str, help="Action to perform (e.g., 'build', 'generate-config').")
    parser.add_argument("config_file", type=str, help="Path to the deployment configuration file (e.g., 'deployments/project_NAME.yml').")
    args = parser.parse_args()

    logging.info(f"Action: {args.action}")
    logging.info(f"Config File: {args.config_file}")

    if args.action == "build":
        build_action(args.config_file)
    elif args.action == "generate-config":
        generate_config_action(args.config_file)
    else:
        logging.error(f"Unsupported action: {args.action}")
        audit_log_and_exit(1)

    audit_log_and_exit(0)

if __name__ == "__main__":
    main()
