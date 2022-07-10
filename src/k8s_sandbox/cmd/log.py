import click
import logging

from k8s_sandbox import mylog
mylog.configure_log()


log = loggin.getLogger(__name__)

@click.command()
def main():
    print("Hello world")
