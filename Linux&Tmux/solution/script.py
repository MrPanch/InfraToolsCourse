#!/usr/bin/env python3

import libtmux
import os
from tqdm import tqdm
import argparse
import uuid
import logging
import socket


logging.basicConfig(level=logging.INFO)


def get_free_port():
    with socket.socket() as s:
        s.bind(('',0))
        return s.getsockname()[1]


def get_env_name_by_num(num):
    return 'user-{}'.format(num)

def start(num_users, base_dir='./'):
    """
    Запустить $num_users ноутбуков. У каждого рабочай директория $base_dir+$folder_num
    """
    tmux_server = libtmux.Server()
    session_name = str(uuid.uuid4())
    session = tmux_server.new_session(session_name=session_name)
    logging.info('started new tmux session with name: %s', session_name)

    for user_num in tqdm(range(1, num_users + 1)):
        # create user work dir
        folder_name = get_env_name_by_num(user_num)

        # working dir: <base_dir>/<session_name>/user-<num>
        work_dir = os.path.join(base_dir, session_name, folder_name)
        os.makedirs(work_dir)
        logging.info('created new working dir: %s', work_dir)

        # crete tmux-window for each user
        window = session.new_window(window_name=folder_name, start_directory=work_dir)
        logging.info('created new window for tmux session with name: %s', folder_name)
        pane = window.attached_pane

        # create python virtual env
        pane.send_keys('python3 -m venv .')
        logging.info('created virtual env')

        # activate virtual env
        pane.send_keys('source ./bin/activate')
        logging.info('activated virtual env')

        # start jupyter notebook
        cmd = 'jupyter notebook --ip {ip} --port {port} --no-browser --NotebookApp.token=\'{token}\' --NotebookApp.notebook_dir=\'{dir}\''.format(
            ip='0.0.0.0',
            port=get_free_port(),
            token=str(uuid.uuid4()),
            dir='.',
        )
        pane.send_keys(cmd)
        logging.info('started jupyter notebook')
        logging.info('%s', cmd)

    logging.info('session <%s> is runing', session_name)


def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    tmux_server = libtmux.Server()
    session = tmux_server.find_where({ "session_name": session_name })
    print(session)
    if not session:
        raise Exception('Invalid session_name or session is not running with same name')
    window_name = get_env_name_by_num(num)
    logging.info('stop window %s in session %s', window_name, session_name)
    session.kill_window(window_name)


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    tmux_server = libtmux.Server()
    session = tmux_server.find_where({ "session_name": session_name })
    if not session:
        raise Exception('Invalid session_name or session is not running with same name')
    logging.info('stop session %s', session_name)
    session.kill_session()


def main():
    parser = argparse.ArgumentParser(description='Start and stop several jupyter instances')
    parser.add_argument('cmd', type=str, choices=['start', 'stop', 'stop_all'])
    parser.add_argument('--num_users', type=int)
    parser.add_argument('--env_num', type=int)
    parser.add_argument('--base_dir', type=str, default='./')
    parser.add_argument('--session_name', type=str)
    args = parser.parse_args()
    if args.cmd == 'start':
        if args.num_users is None:
            parser.error('--num_users required option')
        start(args.num_users, args.base_dir)
    elif args.cmd == 'stop':
        if args.session_name is None:
            parser.error('--session_name required option')
        if args.env_num is None:
            parser.error('--env_num required option')
        stop(args.session_name, args.env_num)
    elif args.cmd == 'stop_all':
        if args.session_name is None:
            parser.error(message='--session_name required option')
        stop_all(args.session_name)

if __name__ == "__main__":
    main()
