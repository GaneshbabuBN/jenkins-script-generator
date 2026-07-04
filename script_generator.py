from urllib.parse import urlparse


def get_repository_name(github_url):
    """
    Extract repository name from GitHub URL.

    Example:
    https://github.com/user/my-app.git

    returns

    my-app
    """

    path = urlparse(github_url).path

    repository = path.rstrip("/").split("/")[-1]

    if repository.endswith(".git"):
        repository = repository[:-4]

    return repository


def build_environment_variables(environment_variables):

    result = ""

    if not environment_variables.strip():
        return result

    for line in environment_variables.splitlines():

        line = line.strip()

        if "=" in line:

            result += f" -e {line}"

    return result


def generate_script(data):

    project_name = data["project_name"].strip()
    github_url = data["github_url"].strip()
    branch = data["branch"].strip()
    docker_image = data["docker_image"].strip()
    docker_container = data["docker_container"].strip()
    dockerhub_username = data["dockerhub_username"].strip()
    environment_variables = data["environment_variables"].strip()
    build_commands = data["build_commands"].strip()
    test_commands = data["test_commands"].strip()
    deployment_type = data["deployment_type"].strip()
    port = data["port"].strip()

    repository = get_repository_name(github_url)

    env_text = build_environment_variables(
        environment_variables
    )

    script = f"""#!/bin/bash

set -e

echo "==============================================="
echo " Jenkins Freestyle Deployment "
echo "==============================================="

echo ""

echo "Checking Git Installation..."

command -v git >/dev/null 2>&1 || {{
    echo "Git is not installed."
    exit 1
}}

echo "Git Found"

echo ""

echo "Checking Docker Installation..."

command -v docker >/dev/null 2>&1 || {{
    echo "Docker is not installed."
    exit 1
}}

echo "Docker Found"

echo ""

echo "Cleaning Previous Repository..."

if [ -d "{repository}" ]; then

    rm -rf "{repository}"

fi

echo ""

echo "Cloning Repository..."

git clone "{github_url}"

cd "{repository}"

echo ""

echo "Checking Out Branch..."

git checkout "{branch}"
"""

    if build_commands:

        script += f"""

echo ""

echo "==============================================="
echo " Running Build Commands "
echo "==============================================="

{build_commands}
"""

    if test_commands:

        script += f"""

echo ""

echo "==============================================="
echo " Running Test Commands "
echo "==============================================="

{test_commands}
"""

    script += f"""

echo ""

echo "==============================================="
echo " Cleaning Docker "
echo "==============================================="

docker stop {docker_container} 2>/dev/null || true

docker rm {docker_container} 2>/dev/null || true

docker image rm {docker_image} 2>/dev/null || true

echo ""

echo "==============================================="
echo " Building Docker Image "
echo "==============================================="

docker build -t {docker_image} .
"""

    if dockerhub_username:

        script += f"""

echo ""

echo "==============================================="
echo " Publishing Docker Image "
echo "==============================================="

docker tag {docker_image} {dockerhub_username}/{docker_image}:latest

docker push {dockerhub_username}/{docker_image}:latest
"""

    script += f"""

echo ""

echo "==============================================="
echo " Running Docker Container "
echo "==============================================="

docker run -d \\
--name {docker_container} \\
-p {port}:{port}{env_text} \\
{docker_image}

echo ""

echo "Deployment Type"

echo "{deployment_type}"

echo ""

echo "==============================================="
echo " Deployment Completed Successfully "
echo "==============================================="
"""

    return script