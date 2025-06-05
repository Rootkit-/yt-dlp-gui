# https://build-system.fman.io/qt-designer-download

import os


def compile(ui_path: str, py_path: str):
    os.system(f'pyuic6 -o {py_path} -x {ui_path}')
    with open(py_path, 'r') as f:
        contents = f.read()
    with open(py_path, 'w') as f:
        f.write(contents.replace('from PyQt6', 'from PySide6'))


if __name__ == '__main__':
    compile('./app/ui/app.ui', './app/ui/app_ui.py')
    # compile('./app/ui/download.ui', './app/ui/download_ui.py')