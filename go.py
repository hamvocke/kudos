#! /usr/bin/env python
import os
from subprocess import call

import click
import pytest
import yaml

from kudos import app, db, initial_data

config = {}


def load_config():
    config_file = open('go.yml', 'r')
    global config
    config = yaml.load(config_file)


def marker():
    click.echo(click.style(u'\u2605 ', fg='yellow'), nl=False)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('version', default=lambda: os.environ.get('VERSION', 'local'))
def build(version):
    marker()
    click.echo('Building version ', nl=False)
    click.echo(click.style(version, fg='green', bold=True))

    build_frontend()

    directory = os.path.dirname(__file__)
    directory_name = os.getcwd().split(os.sep)[-1]
    project_name = config.get('project_name', directory_name)
    tag = '{0}/{1}:{2}'.format(config.get('dockerhub_user'), project_name, version)

    call(['docker', 'build', directory, '-t', tag])


@cli.command()
def push():
    tag = '{0}/{1}:latest'.format(
        config.get('dockerhub_user'),
        config.get('project_name')
    )

    call(['docker', 'push', tag])


@cli.command()
@click.argument('environment')
def deploy(environment):
    marker()
    click.echo('Deploying to ', nl=False)
    click.echo(click.style(environment, fg='green', bold=True))


@cli.command()
def test():
    marker()
    click.echo('Running tests')
    pytest.main()


@cli.command()
@click.argument('environment', default='config.DevelopmentConfig')
def run(environment):
    marker()
    os.environ['APP_PROFILE'] = environment
    build_frontend()
    click.echo('Starting server')
    app.run()


@cli.command()
def watch_sass():
    call(['sass', '--watch', 'kudos/static/sass:kudos/static/css'])


@cli.command()
def initdb():
    marker()
    click.echo('Initialising database')
    db.drop_all()
    db.create_all()
    initial_data.init_db()


@cli.command()
def frontend_test():
    marker()
    click.echo('Running frontend tests')
    build_frontend()
    call(['npm', 'test'])


def build_frontend():
    click.echo('Bundling assets')
    call(['npm', 'run', 'build'])

if __name__ == '__main__':
    load_config()
    cli()
