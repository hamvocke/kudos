#! /usr/bin/env python
import click
import pytest
import os
import yaml
from subprocess import call

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
@click.argument('environment')
def deploy(environment):
    marker()
    click.echo('Deploying to ', nl=False)
    click.echo(click.style(environment, fg='green', bold=True))

@cli.command()
@click.argument('version', default=lambda: os.environ.get('VERSION', 'local'))
def build(version):
    marker()
    click.echo('Building version ', nl=False)
    click.echo(click.style(version, fg='green', bold=True))

    directory = os.path.dirname(__file__)
    directory_name = os.getcwd().split(os.sep)[-1]
    project_name = config.get('project_name', directory_name)
    tag = '{0}/{1}:{2}'.format(config.get('dockerhub_user'), project_name, version)

    call(['docker', 'build', directory, '-t', tag])

@cli.command()
def test():
    marker()
    click.echo('Running tests')
    pytest.main()

if __name__ == '__main__':
    load_config()
    cli()
