
# What's Next?

This repository is the cornerstone for the "What's Next?" project. It encompasses the complete solution—from infrastructure provisioning and VM configuration to application deployment and CI/CD pipeline automation. The project aims to simulate a real-world DevOps environment, integrating modern practices and tools such as Terraform, Ansible, Docker, Jenkins, and security auditing.

## Project Overview

The project includes the following key components:

- **AWS Infrastructure Provisioning:**  
  Provision and manage two virtual machines (VMs) using Terraform:
  - **Application VM:** Hosts the Flask API.
  - **Database VM:** Hosts the database engine (e.g., PostgreSQL).

- **Configuration Management with Ansible:**  
  Automate the configuration of the VMs:
  - Install and configure necessary packages (Python, Docker, etc.).
  - Set up the database server with security hardening.
  - Configure environment variables and connectivity between the VMs.

- **Flask API Development & Containerization:**  
  Develop a Flask-based API and package it using Docker to ensure consistency across environments.  

- **CI/CD Pipeline Automation with Jenkins:**  
  Automate the deployment process by:
  - Running Terraform plans and applies.
  - Executing Ansible playbooks.
  - Building, testing, and deploying the Docker container.
  - Integrating with Git and Jira to track changes and updates.

- **Security Audits & Compliance:**  
  Integrate security best practices by performing:
  - Static code analysis and vulnerability scans.
  - Reviews of IAM policies, key-based access, and RBAC configurations.

- **Demo Preparation:**  
  Prepare and document the complete demo environment and presentation, including a runbook/checklist for the final video demonstration.

## Architecture

The high-level architecture for this project includes:
- **AWS:** Hosting two VMs for application and database.
- **Terraform:** Managing the cloud infrastructure as code.
- **Ansible:** Configuring and managing the environment.
- **Flask API (Dockerized):** Providing the core application functionality.
- **Jenkins CI/CD Pipeline:** Automating builds, tests, and deployments.
- **Security Tools:** Ensuring the application and infrastructure comply with security standards.
- **Collaboration Tools:** Jira for issue tracking and Git for version control.

## Getting Started

### Prerequisites

- **Development Tools:**
  - Git
  - Python 3.12 or higher
  - Docker 
  - Terraform and Ansible 
  - Jenkins 

- **Accounts/Access:**
  - AWS account with appropriate IAM permissions.
  - Access to a container registry (Docker Hub, AWS ECR, etc.).

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/MariferVL/whats-next-api.git
   cd whats-next-api
   ```

2. **Set Up Your Python Environment:**

   ```bash
   python3 -m venv .venv
   .venv\Scripts\activate  # For Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Running the Flask API

1. **Environment Variables:**

   Set the necessary environment variables (e.g., in a `.env` file):

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

2. **Run the Application:**

   ```bash
   flask run
   ```

3. **Access the API:**

   Open your browser and navigate to [http://localhost:5000](http://localhost:5000).

## Future Work & Contributions

- **CI/CD Integration:**  
  Complete the Jenkins pipeline configuration for automated testing, deployment, and integration with Jira.

- **Enhanced Security:**  
  Integrate static analysis and vulnerability scanning tools into the pipeline.

- **Feature Development:**  
  Implement additional features based on project requirements and feedback.

## Contributing Guidelines

- Please follow the Git branching strategy:
  - Use Jira-linked branches for all feature/bug fix commits.
  - Reference the appropriate Jira ticket in commit messages.
- Submit pull requests for review before merging into the main branch.


