# Chicago Tribune News Applications fabfile
# No copying allowed

from fabric.api import *
from contextlib import contextmanager as _contextmanager

"""
Base configuration
"""
env.project_name = 'videotext'
env.apps = ['core',]
env.database_password = '9MeuHqkNt0'
env.site_media_prefix = "site_media"
env.admin_media_prefix = "admin_media"
env.path = '/home/newsapps/sites/%(project_name)s' % env
env.log_path = '/home/newsapps/logs/%(project_name)s' % env
env.env_path = '%(path)s/env' % env
env.repo_path = '%(path)s/repository' % env
env.apache_config_path = '/home/newsapps/sites/apache/%(project_name)s' % env
env.python = 'python2.6'
env.repository_url = "https://MrMetlHed@github.com/ReportersLab/TwitterVision.git"
env.multi_server = False
env.memcached_server_address = "cache.example.com"

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.hosts = ['reporterslab.org']
    env.user = 'newsapps'
    env.s3_bucket = 'media.reporterslab.org'

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.hosts = ['beta.reporterslab.org'] 
    env.user = 'newsapps'
    #env.s3_bucket = 'media.beta.reporterslab.org'
    env.s3_bucket = 'media.reporterslab.org/beta'
    


@_contextmanager
def virtualenv():
    """
    Activates the environment's virtualenv. This makes
    executing ./manage calls easier.
    """    
    with prefix('source %(env_path)s/bin/activate' % env):
        yield


    
"""
Branches
"""
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'

def master():
    """
    Work on development branch.
    """
    env.branch = 'master'

def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name
    
"""
Commands - setup
"""
def setup():
    """
    Setup a fresh virtualenv, install everything we need, and fire up the database.
    
    Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()
    destroy_database()
    create_database()
    load_data()
    install_requirements()
    install_apache_conf()

def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)
    run ('mkdir -p %(log_path)s;' % env)
    sudo('chgrp -R www-data %(log_path)s; chmod -R g+w %(log_path)s;' % env)
    run('ln -s %(log_path)s %(path)s/logs' % env)
    
def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    with virtualenv():
        run('sudo easy_install -U setuptools; sudo easy_install pip; sudo easy_install mercurial;' % env)

def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone %(repository_url)s %(repo_path)s' % env)

def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    with cd('%(repo_path)s' % env):
        run('git checkout %(branch)s; git pull origin %(branch)s' % env)

def install_requirements():
    """
    Install the required packages using pip.
    """
    with virtualenv():
        with cd('%(repo_path)s' % env):
            run('pip install -E %(env_path)s -r requirements.txt' % env)

def install_apache_conf():
    """
    Install the apache site config file.
    """
    sudo('cp %(repo_path)s/%(project_name)s/configs/%(settings)s/apache %(apache_config_path)s' % env)

"""
Commands - deployment
"""
def deploy():
    """
    Deploy the latest version of the site to the server and restart Apache2.
    
    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    with settings(warn_only=True):
        maintenance_up()
        
    checkout_latest()
    collect_static()
    gzip_assets()
    deploy_to_s3()
    run_migrations()
    maintenance_down()
    
def maintenance_up():
    """
    Install the Apache maintenance configuration.
    """
    sudo('cp %(repo_path)s/%(project_name)s/configs/%(settings)s/apache_maintenance %(apache_config_path)s' % env)
    reboot()
    

def collect_static():
    """
    Collects Static files from installed apps and places their
    content in the STATIC_ROOT. This allows that content to be
    pushed to S3, but not live in the repo.
    """
    with virtualenv():
        with cd('%(repo_path)s' % env):
            run('./manage collectstatic')


def gzip_assets():
    """
    GZips every file in the assets directory and places the new file
    in the gzip directory with the same filename.
    """
    with cd('%(repo_path)s' % env):
        run('python gzip_assets.py' % env)

def deploy_to_s3():
    """
    Deploy the latest project site media to S3.
    """
    env.gzip_path = '%(path)s/repository/%(project_name)s/gzip/assets/' % env
    run(('s3cmd -P --add-header=Content-encoding:gzip --guess-mime-type --rexclude-from=%(path)s/repository/s3exclude sync %(gzip_path)s s3://%(s3_bucket)s/%(project_name)s/%(site_media_prefix)s/') % env)

def run_migrations():
    """
    Run South Migrations pulled in from the repo against the database
    """
    with virtualenv():
        with cd('%(repo_path)s' % env):
            for app in env.apps:
                run('./manage migrate %s' % app)
  
       
def reboot(): 
    """
    Restart the Apache2 server.
    """
    if env.multi_server:
        run('/mnt/apps/bin/restart-all-apache.sh')
    else:
        sudo('service apache2 restart')
    
def maintenance_down():
    """
    Reinstall the normal site configuration.
    """
    install_apache_conf()
    reboot()
    
"""
Commands - rollback
"""
def rollback(commit_id):
    """
    Rolls back to specified git commit hash or tag.
    
    There is NO guarantee we have committed a valid dataset for an arbitrary
    commit hash.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    maintenance_up()
    checkout_latest()
    git_reset(commit_id)
    gzip_assets()
    deploy_to_s3()
    maintenance_down()
    
def git_reset(commit_id):
    """
    Reset the git repository to an arbitrary commit hash or tag.
    """
    env.commit_id = commit_id
    run("cd %(repo_path)s; git reset --hard %(commit_id)s" % env)

"""
Commands - data
"""
def load_new_data():
    """
    Erase the current database and load new data from the SQL dump file.
    """
    require('settings', provided_by=[production, staging])
    
    maintenance_up()
    pgpool_down()
    destroy_database()
    create_database()
    load_data()
    pgpool_up()
    maintenance_down()
    
def create_database(func=run):
    """
    Creates the user and database for this project.
    """
    func('echo "CREATE USER %(project_name)s WITH PASSWORD \'%(database_password)s\';" | psql postgres' % env)
    func('createdb -O %(project_name)s %(project_name)s' % env)
    #func('createdb -O %(project_name)s %(project_name)s -T template_postgis' % env)
    
def destroy_database(func=run):
    """
    Destroys the user and database for this project.
    
    Will not cause the fab to fail if they do not exist.
    """
    with settings(warn_only=True):
        func('dropdb %(project_name)s' % env)
        func('dropuser %(project_name)s' % env)
        
def load_data():
    """
    Loads data from the repository into PostgreSQL.
    """
    run('psql -q %(project_name)s < %(path)s/repository/data/psql/dump.sql' % env)
    run('psql -q %(project_name)s < %(path)s/repository/data/psql/finish_init.sql' % env)
    
def pgpool_down():
    """
    Stop pgpool so that it won't prevent the database from being rebuilt.
    """
    sudo('/etc/init.d/pgpool stop')
    
def pgpool_up():
    """
    Start pgpool.
    """
    sudo('/etc/init.d/pgpool start')

"""
Commands - miscellaneous
"""
    
def clear_cache():
    """
    Restart memcache, wiping the current cache.
    """
    if env.multi_server:
        run('restart-memcache.sh %(memcached_server_address)' % env)
    else:
        sudo('service memcached restart')
    
def echo_host():
    """
    Echo the current host to the command line.
    """
    run('echo %(settings)s; echo %(hosts)s' % env)

"""
Deaths, destroyers of worlds
"""
def shiva_the_destroyer():
    """
    Remove all directories, databases, etc. associated with the application.
    """
    with settings(warn_only=True):
        run('rm -Rf %(path)s' % env)
        run('rm -Rf %(log_path)s' % env)
        pgpool_down()
        run('dropdb %(project_name)s' % env)
        run('dropuser %(project_name)s' % env)
        pgpool_up()
        sudo('rm %(apache_config_path)s' % env)
        reboot()
        run('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s' % env)

"""
Utility functions (not to be called directly)
"""
def _execute_psql(query):
    """
    Executes a PostgreSQL command using the command line interface.
    """
    env.query = query
    run(('cd %(path)s/repository; psql -q %(project_name)s -c "%(query)s"') % env)
    
def bootstrap():
    """
    Local development bootstrap: you should only run this once.
    """    
    create_database(local)
    local("sh ./manage syncdb --noinput")
    #local("sh ./manage load_shapefiles")

def shiva_local():
    """
    Undo any local setup.  This will *destroy* your local database, so use with caution.
    """    
    destroy_database(local)
