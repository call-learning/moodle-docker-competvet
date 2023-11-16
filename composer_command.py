import argparse
import subprocess
import setup_utils
import os
CURRENT_DIR = os.getcwd()
# Step 1: Parse arguments
parser = argparse.ArgumentParser(description='Run docker-compose with custom arguments')
parser.add_argument('-f', '--file', help='Specify an alternate compose file')
parser.add_argument('command', help='docker-compose command (e.g., up, down, build)')

# Parse known arguments and leave the rest
known_args, unknown_args = parser.parse_known_args()
# Add known arguments if provided
DOCKER_COMPOSE_CMD = setup_utils.get_docker_compose_command()
MOODLE_SRC_DIR = CURRENT_DIR + '/moodle-src'
setup_utils.setup_env(MOODLE_SRC_DIR)

command_parts = [DOCKER_COMPOSE_CMD]
if known_args.file:
    command_parts.append(f'-f {known_args.file}')
# Add the main command
command_parts.append(known_args.command)
# Add any unknown arguments
command_parts.extend(unknown_args)
# Join the command parts to form the complete command
command = ' '.join(command_parts)

os.chdir(CURRENT_DIR + '/moodle-docker')
process = subprocess.run(command, shell=True, check=True)
