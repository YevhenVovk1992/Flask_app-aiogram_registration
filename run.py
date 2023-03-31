import multiprocessing
import subprocess


PYTHON_PATH = 'python3'
api_process = multiprocessing.Process(
    target=subprocess.run,
    kwargs={
        'args': f'{PYTHON_PATH} app.py',
        'shell': True
    })
bot_process = multiprocessing.Process(
    target=subprocess.run,
    kwargs={
        'args': f'{PYTHON_PATH} bot.py',
        'shell': True
    })


if __name__ == '__main__':
    api_process.start()
    bot_process.start()
