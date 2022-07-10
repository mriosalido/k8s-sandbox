import os
import time
import click
import logging

from k8s_sandbox import mylog
mylog.configure_log()


log = logging.getLogger(__name__)

@click.command()
def main():
    try:
        log.info("Start init")
        sleep = os.environ.get("K8S_SANDBOX_INIT_SLEEP", 0) 
        time.sleep(int(sleep))
        log.info(f"End init. Sleep {sleep}")
    except Exception as ex:
        log.error(ex)
