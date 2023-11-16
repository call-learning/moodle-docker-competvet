from git import Repo
import shutil
import os
import setup_utils
# If directory moodle-src does not exist, create it.
# Get current directory in CURRENT_DIR variable

CURRENT_DIR = os.getcwd()
MOODLE_SRC_DIR = os.path.join(CURRENT_DIR, 'moodle-src')
if not os.path.isdir(MOODLE_SRC_DIR):
    os.mkdir(MOODLE_SRC_DIR)
# Check if moodle-src is empty and has a git repository cloned already
if os.path.isdir(os.path.join(MOODLE_SRC_DIR, '.git')):
    print('moodle-src already has a git repository. Assuming this is the '
          'moodle repository.')
else:
    # Clone the moodle repository into moodle-src
    print('Cloning Moodle repository in moodle-src.')
    Repo.clone_from('http://github.com/moodle/moodle.git', 'moodle-src')
# Change directory to moodle-src
os.chdir(MOODLE_SRC_DIR)
# Checkout the latest stable version
Repo().git.checkout('MOODLE_401_STABLE')
# Then add two modules
print('Cloning CompetVetEval Module plugin.')
setup_utils.clone_or_update_modules(MOODLE_SRC_DIR, 'mod','competvet','https://github.com/call-learning/moodle-mod_competvet.git')

print('Cloning CompetVetEval Local plugin.')
setup_utils.clone_or_update_modules(MOODLE_SRC_DIR, 'local','competvet','https://github.com/call-learning/moodle-local_competvet.git')

setup_utils.setup_env(MOODLE_SRC_DIR)

# copy the moodle-docker/config.docker-template.php to moodle-src/config.php
if not os.path.isfile(os.path.join(MOODLE_SRC_DIR,'config.php')):
    shutil.copyfile(
        os.path.join(CURRENT_DIR, 'config.docker-template.php'),
        os.path.join(MOODLE_SRC_DIR, 'config.php'))

# depending if on windows or linux, run the appropriate docker-compose command to start the containers
print('Bringing container up.')
os.chdir(os.path.join(CURRENT_DIR, 'moodle-docker'))
DOCKER_COMPOSE_CMD = setup_utils.get_docker_compose_command()
os.system(DOCKER_COMPOSE_CMD + ' up -d')
setup_utils.wait_for_db()
# # Install Moodle
print('Installing Moodle.')
setup_utils.run_moodle_cli('admin/cli/install_database.php',
               '--agree-license',
               '--fullname="CompetVetMOODLE"',
               '--shortname="CompetVetMOODLE"',
               '--adminpass="test"',
               '--adminemail="admin@example.com"'
               )

print('Finished. You can now send your command with '
      '"bin/moodle-docker-compose.cmd" as per documented on '
      'https://github.com/moodlehq/moodle-docker/blob/master/README.md. and '
      'destroy the containers with "bin/moodle-docker-compose.cmd down"')
