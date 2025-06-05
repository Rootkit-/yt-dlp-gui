import os
import platform
import shutil
import stat
from io import StringIO
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta
import tarfile
import zipfile
from pyunpack import Archive
import re

import requests
from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QWidget
from tqdm import tqdm

from ui.download_ui import Ui_Download
from utils import ROOT

BIN = "bin"
os.environ['PATH'] = os.pathsep.join([os.path.join(os.getcwd(), BIN), os.environ['PATH']])



def if_download_file(file_path):
    
    file = file_path
    if platform.system() == 'Windows': file += '.exe'
    
    if not os.path.exists(os.path.join(BIN, file)):
        return True
    try:
        current_date = datetime.now()
        one_month_ago = current_date - timedelta(days=30)
        mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(BIN, file)))
        return mod_time < one_month_ago
    except:
        return True

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

class DownloadWindow(QWidget, Ui_Download):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pb.setMaximum(100)
        self.missing = []

        self.get_missing_dep()

        if self.missing:
            self.show()
            self.download_init()
        else:
            QTimer.singleShot(0, self.finished.emit)

    def get_missing_dep(self):
        binaries = {
            "Linux": {
                "ffmpeg": "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-linux64-gpl-shared.tar.xz",
                "yt-dlp": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux"
            },
            "Darwin": {
                "ffmpeg": ["https://evermeet.cx/ffmpeg/get/zip", "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"],
                "yt-dlp": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            },
            "Windows": {
                "ffmpeg": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
                "yt-dlp": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            },
        }

        exes = [exe for exe in ["ffmpeg", "ffprobe", "yt-dlp"] if if_download_file(exe)]
        os_ = platform.system()

        if exes:
            if os.path.exists(BIN):
                shutil.rmtree(BIN, ignore_errors=False, onerror=onerror)
            if not os.path.exists(BIN):
                os.makedirs(BIN)
                
            url = binaries[os_]['yt-dlp']
            filename = os.path.join(BIN, f"yt-dlp.exe" if os_ == "Windows" else 'yt-dlp')
            self.missing += [[url, filename]]
            
            if os_ == 'Darwin':
                url = binaries[os_]['ffmpeg'][0]
                filename = os.path.join(BIN, "ffmpeg_archive.zip")
                self.missing += [[url, filename]]
                url = binaries[os_]['ffmpeg'][1]
                filename = os.path.join(BIN, "ffprobe_archive.zip")
                self.missing += [[url, filename]]
            
            else:
                url = binaries[os_]['ffmpeg']
                filename = os.path.join(BIN, "ffmpeg_archive." + ('zip' if os_ == 'Windows' else 'tar.xz'))
                self.missing += [[url, filename]]
            

    def download_init(self):
        url, filename = self.missing[0]
        self.downloader = _D_Worker(url, filename)
        self.downloader.progress.connect(self.update_progress)
        self.downloader.finished.connect(self.downloader.deleteLater)
        self.downloader.finished.connect(self.on_download_finished)
        self.downloader.start()

    def on_download_finished(self):
        url, filename = self.missing.pop(0)
        
        if 'ff' in url.lower():
            self.extract_ffmpeg(filename)
        else:
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)
            req = requests.get('https://raw.githubusercontent.com/yt-dlp/yt-dlp/refs/heads/master/supportedsites.md')
            
            with open(os.path.join(BIN, 'supported-sites.txt'), 'w', encoding='utf-8') as f:
                pattern = r'\*\*([^*]+)\*\*:.*'
                matches = re.findall(pattern, req.text)
                for site in matches:
                    f.write(site.strip().lower() + '\n')

        if self.missing:
            self.download_init()
        else:
            self.finished.emit()

    def update_progress(self, progress, data):
        self.pb.setValue(progress)
        self.lb_progress.setText(data)


    def extract_ffmpeg(self, archive_path):
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(BIN)
        elif archive_path.endswith('.tar.xz'):
            with tarfile.open(archive_path, 'r:xz') as tar_ref:
                tar_ref.extractall(BIN)
        else:
            raise ValueError(f"Unsupported archive format: {archive_path}")

        # Search for ffmpeg and ffprobe executables
        for root, dirs, files in os.walk(os.path.join(BIN)):
            for file in files:
                if file.lower() in ['ffprobe', 'ffmpeg', 'ffprobe.exe', 'ffmpeg.exe'] and os.path.split(root)[-1] == 'bin':
                    src = os.path.join(root, file)
                    dst = os.path.join(BIN, file)
                    if src != dst:
                        shutil.copy(src, dst)
                        os.chmod(dst, stat.S_IEXEC)

    # Remove all directories inside BIN and the archive itself
        for item in os.listdir(BIN):
            item_path = os.path.join(BIN, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif item == os.path.basename(archive_path):
                os.remove(item_path)

    

class _D_Worker(QThread):
    progress = Signal(int, str)

    def __init__(self, url, filename=None):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        if not self.filename:
            self.filename = os.path.basename(self.url)
        r = requests.get(self.url, stream=True)
        file_size = int(r.headers.get("content-length", 0))
        scaling_factor = 100 / file_size if file_size > 0 else 0
        data = StringIO()
        chunk_size = 1024
        read_bytes = 0

        with NamedTemporaryFile(mode="wb", delete=False) as temp, tqdm(
            desc=os.path.basename(self.filename),
            total=file_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
            file=data,
            bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}/{remaining}, {rate_fmt}{postfix}]",
            leave=True,
        ) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                temp.write(chunk)
                bar.update(chunk_size)
                read_bytes += chunk_size
                self.progress.emit(
                    read_bytes * scaling_factor, data.getvalue().split("\r")[-1].strip()
                )
        data.close()
        shutil.move(temp.name, self.filename)
