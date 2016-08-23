# config valid only for current version of Capistrano
lock '3.5.0'

set :application, 'hacksoft'
set :repo_url, 'git@github.com:HackSoftware/hacksoft-wagtail.git'

# Default branch is :master
ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
deploy_to_directory = '/hack/hacksoft/'
set :deploy_to, deploy_to_directory

# Default value for :scm is :git
# set :scm, :git

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: 'log/capistrano.log', color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# set :linked_files, fetch(:linked_files, []).push('config/database.yml', 'config/secrets.yml')

# Default value for linked_dirs is []
set :linked_dirs, fetch(:linked_dirs, []).push('staticfiles', 'media')

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
# set :keep_releases, 5

namespace :deploy do

  task :pip_install do
    on roles(:all) do |h|
      execute "#{deploy_to_directory}shared/virtualenv/bin/pip install -r #{deploy_to_directory}current/requirements/production.txt"
    end
  end

  task :run_migrations do
    on roles(:all) do |h|
      execute "#{deploy_to_directory}shared/virtualenv/bin/python3 #{deploy_to_directory}current/manage.py migrate --noinput"
    end
  end

  task :run_collect_static do
    on roles(:all) do |h|
      execute "#{deploy_to_directory}shared/virtualenv/bin/python3 #{deploy_to_directory}current/manage.py collectstatic --noinput"
    end
  end

  task :restart do
    on roles(:all) do |h|
      execute "sudo restart hacksoft"
    end
  end

  after :published, :pip_install
  after :pip_install, :run_migrations
  after :run_migrations, :run_collect_static
  after :run_migrations, :restart

end
