# Clab Config Validation

## Overview
`Clab Config Checker` is a simple tool designed to automate configuration management for network multi-vendor routers. It covers the full lifecycle of configuration files, including **generation**, **validation**, and **deployment**. I am tying to make a tool supports multiple network vendors like Nokia, Juniper and Arista with plans to expand to others in the future and integrates seamlessly with GitHub Actions to enable continuous integration workflows for configuration testing and deployment.

---

## Features
1. **Config Generation**
   - Supports pre-defined templates and user-customizable data files for router's configs generation.
   - Configurations can be generated for various topologies and placed in structured directories.

2. **Validation**
   - Validates generated configurations using predefined `show` commands.
   - Includes vendor-specific validation logic for Nokia, Juniper, and Arista devices.

3. **Deployment**
   - Automatically applies validated configurations to routers using SSH.
   - Generates detailed output logs for easy debugging and tracking.

4. **Integration with GitHub Actions**
   - CI/CD pipelines for validation and deployment:
     - Triggered by changes to configuration files.
     - Automatically validates and applies configurations.
     - Sends notification upon success or failure.

---

## Directory Structure
```plaintext
├── configs/
│   ├── nokia/
│   │   ├── srl/
│   │   └── sros/
│   ├── arista/
│   └── juniper/
├── topology/
│   ├── nokia/
│   ├── arista/
│   └── juniper/
├── validations/
│   ├── nokia.yml
│   ├── arista.yml
│   └── juniper.yml
├── credentials/
│   ├── nokia_credentials.yaml
│   ├── cisco_credentials.yaml
│   └── juniper_credentials.yaml
├── output/
│   └── validation_results/
├── templates/
│   ├── build-vars-srl.yaml
│   ├── build-vars-ceos.yaml
│   ├── build-vars-jnpr.yaml
│   └── ...
└── .github/
    └── workflows/
        ├── nokia_ci.yml
        ├── arista_ci.yml
        └── juniper_ci.yml
```

---

## Getting Started

1. ### Installation
**Clone the Repository**  
   Download the repository to your local environment:
   ```bash
   git clone https://github.com/dgilmano/clab-config-checker.git
   cd clab-config-checker

2. ### Generate Configurations
**Generate router configurations using predefined templates and variables:**
   ```bash
   python scripts/srl-node-cmd-checker.py
   --data templates/build-vars-srl.yaml
   --output configs/nokia/srl/

### Generate Configurations
3. **Trigger the CI pipeline to validate configuration files automatically:**
   Add and Commit Configurations:
   ```bash
   git add configs/nokia/srl/srl1.cfg
   git commit -m "Add Nokia SRL1 configuration"
   git push

**Run Validation: Once pushed, GitHub Actions will:**

1. Spin up a Containerlab topology.
2. Connect to the router using credentials from the credentials/ directory.
3. Execute the specified show commands from the validations/ directory.
4. Save the validation results to the output/ directory.

### Apply Configurations
4. **Deploy validated configurations to the target routers:**
   ```bash
   python scripts/apply_configs.py
   --target nokia
   --configs configs/nokia/srl1.cfg

### Check Validation Results
5. **Validation outputs are stored in the output/ directory with filenames matching the executed commands. For example:**
output/
└── show_system_interfaces.txt