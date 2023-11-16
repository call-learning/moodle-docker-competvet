# Create a function setup_env
import os
from git import Repo

def setup_env(moodle_src_dir):
    os.environ['MOODLE_DOCKER_WWWROOT'] = moodle_src_dir
    os.environ['MOODLE_DOCKER_DB'] = 'mysql'
    os.environ['MOODLE_DOCKER_WEB_PORT'] = '8000'

def get_docker_compose_command():
    if os.name == 'nt':
        return os.path.join('bin', 'moodle-docker-compose.cmd')
    else:
        return os.path.join('bin', 'moodle-docker-compose')

def clone_or_update_modules(MOODLE_SRC_DIR, MODULE_INSTALL_DIR,MODULE_NAME,GIT_REPO_URL):
    os.chdir(os.path.join(MOODLE_SRC_DIR, MODULE_INSTALL_DIR))
    MODULE_FULLDIR = os.path.join(MOODLE_SRC_DIR, MODULE_INSTALL_DIR,MODULE_NAME)
    if not os.path.isdir(MODULE_FULLDIR):
        Repo.clone_from(
        GIT_REPO_URL,
        MODULE_NAME)
    else:
        print('Module plugin already cloned. Assuming this is the '
          'plugin repository, updating it.')
        Repo(MODULE_FULLDIR).git.pull()

def wait_for_db():
    DOCKER_COMPOSE_CMD = get_docker_compose_command()
    print("Waiting for database to be ready...")
    result = os.popen(DOCKER_COMPOSE_CMD + ' logs db').read()
    # Wait until result contains 'DATABASE IS READY TO USE!'
    while '/usr/sbin/mysqld: ready for connections' not in result:
        result = os.popen(DOCKER_COMPOSE_CMD + ' logs db').read()

def run_moodle_cli(CLI_COMMAND, *ARGS):
    DOCKER_COMPOSE_CMD = get_docker_compose_command()
    # Call a external command and send argments separated by space
    os.system(DOCKER_COMPOSE_CMD + ' exec -T webserver php ' + CLI_COMMAND + ' ' + ' '.join(ARGS))

