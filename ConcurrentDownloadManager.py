import os
import requests
import concurrent.futures
from AtomicCounter import AtomicCounter
import pandas as pd


class ConcurrentDownloadManager:
    def __init__(self, num_threads=None):
        self.num_threads = num_threads
        self.totalFilesCount = 0
        self.downloadedFilesCount = AtomicCounter(0)

    def downloadFile(self, filename, url):
        try:
            result = requests.get(url)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as file:
                file.write(result.content)
            self.downloadedFilesCount.increment()
            print(f'Downloaded files: {self.downloadedFilesCount.value}/{self.totalFilesCount}')
        except Exception as e:
            print(f'Exception in downloadFile({filename}, {url}):', e)

    def downloadFiles(self, files_to_download):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            self.totalFilesCount = len(files_to_download)
            self.downloadedFilesCount = AtomicCounter(0)
            for file in files_to_download:
                (filename, url) = file
                executor.submit(self.downloadFile, filename=filename, url=url)