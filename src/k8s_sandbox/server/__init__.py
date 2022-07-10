import os
import time
import sys
import signal
import logging
from logging.config import dictConfig
import threading

from flask import Flask, current_app
from flask.cli import FlaskGroup

import click

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from k8s_sandbox import mylog
from k8s_sandbox.server import settings


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with current_app.app_context():
            config_file = current_app.config.get("K8S_SANDBOX_CONFIG_FILE", None)
            if config_file:
                current_app.config.from_pyfile(config_file)
                current_app.config["K8S_SANDBOX_CONFIG_FILE"] = config_file


class Watcher(threading.Thread):
    def stopme(self):
        self.runme = False

    def run(self):
        self.runme = True
        observer = Observer()
        observer.schedule(MyHandler(), "/home/marcos/Proyectos/Certification/sources/k8s-sandbox/k8s_sandbox.server.frontend_settings.cfg")
        observer.start()
        while self.runme:
            time.sleep(1)
        observer.stop()
        observer.join()


watcher_thread = Watcher()


def handler(signum, frame):
    watcher_thread.stopme()
    watcher_thread.join()
    sys.exit(0)


def configure_app(app):
    try:
        config_name = os.environ.get("K8S_SANDBOX_CFG_NAME", None)
        config_file = os.environ.get("K8S_SANDBOX_CFG_FILE", None)
        if config_file is not None:
            app.config.from_pyfile(config_file)
            app.config["K8S_SANDBOX_CONFIG_FILE"] = config_file
            watcher_thread.start()
        else:
            app.config.from_object(f'k8s_sandbox.server.settings.{config_name}Config')
            watcher_thread.start()
    except Exception as e:
        print(e)


def create_app():
    app = Flask(__name__)
    configure_app(app)

    from k8s_sandbox.server import views
    views.init_app(app)

    K8S_SANDBOX_STARTUP_DELAY = app.config["K8S_SANDBOX_STARTUP_DELAY"]
    if K8S_SANDBOX_STARTUP_DELAY > 0:
        app.logger.info(f"Startup delay {K8S_SANDBOX_STARTUP_DELAY}")
        time.sleep(int(K8S_SANDBOX_STARTUP_DELAY))
        app.logger.info("Startup delay ok")

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def frontend():
    mylog.configure_log()
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
#    os.environ["K8S_SANDBOX_CFG_NAME"] = 'Frontend'
    os.environ["K8S_SANDBOX_CFG_FILE"] = "/home/marcos/Proyectos/Certification/sources/k8s-sandbox/k8s_sandbox.server.frontend_settings.cfg"
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

@click.group(cls=FlaskGroup, create_app=create_app)
def backend():
    mylog.configure_log()
    # os.environ["K8S_SANDBOX_CFG_FILE"] = "/home/marcos/Proyectos/Certification/sources/k8s-sandbox/k8s_sandbox.server.backend_settings.cfg"
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    os.environ["K8S_SANDBOX_CFG_NAME"] = 'Backend'
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
