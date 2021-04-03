#!/usr/bin/env python3

import os
import shutil
import subprocess
from time import sleep

current_directory = os.path.abspath(os.getcwd())


def _execute_cmd(command):
    """Executes the command in current shell and waits for 0 exit code."""
    print('About to run command: %s' % command)
    subprocess.check_call(command, shell=True)


def prepare_css():
    """Prepares css for prod deployment."""
    minify_css_command = 'npm run minify-css'
    _execute_cmd(minify_css_command)

    # after that we need to copy
    shutil.copy(os.path.join(current_directory, 'css-dist/main.min.css'),
                os.path.join(current_directory, 'app/static/styles/main.min.css'))

    # remove css folder after that
    shutil.rmtree(os.path.join(current_directory, 'css-dist'))


def prepare_js():
    """prepare js for prod deployment."""

    # first remove all content of js folder
    js_folder_path = os.path.join(current_directory, 'app\static\js')
    shutil.rmtree(js_folder_path, ignore_errors=True)
    os.mkdir(js_folder_path)

    # generate new files
    generate_js_cmd = 'npm run build-dev'
    _execute_cmd(generate_js_cmd)


def main():
    """Runs release prod"""
    while True:
        prepare_css()
        prepare_js()
        sleep(15)


if __name__ == '__main__':
    main()
