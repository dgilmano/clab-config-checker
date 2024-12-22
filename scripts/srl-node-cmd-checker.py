import paramiko
import yaml

def load_yaml(file_path):
    """Load YAML data from a file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def execute_commands_on_router(host, username, password, commands):
    """Connect to the router and execute a list of commands."""
    try:
        print(f"Connecting to {host}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        for command in commands:
            print(f"Executing: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if output:
                print(f"Output:\n{output}")
            if error:
                print(f"Error:\n{error}")

        ssh.close()
        print(f"Completed execution on {host}.")
    except Exception as e:
        print(f"Error connecting to {host}: {e}")

if __name__ == "__main__":
    # Paths to the credential and command files
    credentials_file = "/home/runner/work/clab-config-checker/clab-config-checker/credentials/nokia/srl/creds.yml"
    commands_file = "/home/runner/work/clab-config-checker/clab-config-checker/validations/nokia/cmd-nokia.yml"

    # Load credentials and commands
    credentials = load_yaml(credentials_file)
    commands = load_yaml(commands_file)

    # Execute commands for each router in credentials
    for router in credentials.get("routers", []):
        host = router.get("host")
        username = router.get("username")
        password = router.get("password")
        
        execute_commands_on_router(host, username, password, commands.get("commands", []))
