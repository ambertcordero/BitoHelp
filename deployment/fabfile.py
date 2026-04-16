from patchwork.transfers import rsync
from fabric import task
from fabric.connection import Connection
from dotenv import dotenv_values

# new server use 'docker compose' instead of old 'docker-compose'
DOCKER_COMPOSE_COMMAND="docker compose"

env_config = dotenv_values(".env_fabfile")
project = "cryptocare"


def __setup_context__(ctx):
    ctx.config.env = env_config["ENV"]
    ctx.config.user = env_config['SERVER_USER']
    ctx.config.project_dir = f'/{ctx.config.user}/{project}'
    ctx.config.run.env['conn'] = Connection(
        env_config['SERVER_HOST'],
        user=env_config['SERVER_USER'],
        connect_kwargs = { 'key_filename': env_config['SERVER_SSH_KEY'] }
    )

@task
def sync(ctx):
    __setup_context__(ctx)
    conn = ctx.config.run.env['conn']
    rsync(
        conn,
        '../',
        ctx.config.project_dir,
        exclude=[
            'node_modules',
            'venv',
            '.venv',
            '.git',
            '/static',
            '/media',
            '.DS_Store',
            '__pycache__',
            '*.pyc',
            '*.log',
            '*.pid'
        ]
    )


@task
def build(ctx):
    __setup_context__(ctx)
    conn = ctx.config.run.env['conn']
    with conn.cd(f'{ctx.config.project_dir}/deployment'):
        conn.run(f'{DOCKER_COMPOSE_COMMAND} -f prod.yml build')


@task
def up(ctx):
    __setup_context__(ctx)
    conn = ctx.config.run.env['conn']
    with conn.cd(f'{ctx.config.project_dir}/deployment'):
        conn.run(f'{DOCKER_COMPOSE_COMMAND} -f prod.yml up -d')


@task
def down(ctx):
    __setup_context__(ctx)
    conn = ctx.config.run.env['conn']
    with conn.cd(f'{ctx.config.project_dir}/deployment'):
        conn.run(f'{DOCKER_COMPOSE_COMMAND} -f prod.yml down --remove-orphans')


@task
def deploy(ctx):
    __setup_context__(ctx)
    print("Syncing")
    sync(ctx)
    print("Building")
    build(ctx)
    print("Restarting: closing")
    down(ctx)
    print("Restarting: running")
    up(ctx)


@task
def nginx(ctx):
    sync(ctx)
    conn = ctx.config.run.env['conn']
    with conn.cd(f'{ctx.config.project_dir}/deployment'):
        nginx_conf = f"/etc/nginx/sites-available/{project}"
        nginx_slink = f"/etc/nginx/sites-enabled/{project}"

        try:
            print("Removing previous nginx config")
            conn.run(f'sudo rm {nginx_conf}')
            conn.run(f'sudo rm {nginx_slink}')
        except:
            pass

        print("Updating nginx config")
        # direct "sudo cat ..." caused permission denied error
        # https://stackoverflow.com/a/10145083
        conn.run(f"sudo bash -c 'cat nginx.conf > {nginx_conf}'")
        conn.run(f'sudo ln -s {nginx_conf} {nginx_slink}')

        print("Restarting nginx service")
        conn.run('sudo service nginx restart')

@task
def streamlogs(ctx, tail=1000):
    __setup_context__(ctx)
    conn = ctx.config.run.env['conn']

    with conn.cd(f'{ctx.config.project_dir}/deployment'):
        conn.run(f'{DOCKER_COMPOSE_COMMAND} -f prod.yml logs --tail f{tail} --follow backend')
