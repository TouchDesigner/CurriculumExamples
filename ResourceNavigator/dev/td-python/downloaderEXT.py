import requests
import os
from urllib.parse import parse_qs
import shutil
import threading
from queue import Queue
from pathlib import Path

class downlaoderAgent:
    '''
    '''

    def __init__(self, owner_op:OP) -> None:
        self.Owner = owner_op
        self.jobs = Queue()
        self.Downloads_remaining = tdu.Dependency(0)
        print("download agent init")

    def Fetch_files(self, manifest:list) -> None:
        '''Accepts a list of links to download
        '''
        cache_dir = self.Owner.par.Cachelocation.eval()
        project_dir = project.folder
        target_dir = f"{project_dir}/{cache_dir}"

        # check to make sure our target dir exists
        if os.path.isdir(target_dir):
            pass

        # create it if it does not yet exists
        else:
            valid_path = Path(target_dir)
            valid_path.mkdir(parents=True)

        # create a queue
        self._fill_queue(manifest, target_dir)

        # turn on execute DAT
        op("execute_status").par.active = True
    
    def _fill_queue(self, manifest:list, target_dir:str) -> None:
        '''Fills threading Queue
        '''

        # threaded downloader
        for each_item in manifest:
            base_name = parse_qs(each_item)['path'][0].replace('/', '.')
            local_file_path = f"{target_dir}/{base_name}"

            # skip files that already exist
            if os.path.isfile(local_file_path):
                print(f"File previously cached skipping | {local_file_path}")
                pass
            else:
                # create a job for each download
                self.jobs.put([each_item, local_file_path])

        # start up 10 downloader threads
        for each_thread in range(10):
            worker = threading.Thread(target=self._download_img, args=(self.jobs,))
            worker.start()
        
        # set the remaining downloads
        self.Downloads_remaining.val = len(manifest)

    def _download_img(self, q:Queue) -> None:
        '''Worker func
        '''
        while not q.empty():
            value = q.get()

            file_url = value[0]
            local_path = value[1]
            
            response = requests.get(file_url, stream=True)
            if response.status_code != 200:
                pass

            else:
                with open(local_path, "wb") as current_img:
                    shutil.copyfileobj(response.raw, current_img)
            
            q.task_done()

    def _current_queue_size(self) -> int:
        '''Current Queue size
        '''
        return self.jobs.qsize()

    def Download_status(self) -> tuple:
        '''
        '''
        self.Downloads_remaining.val = self._current_queue_size()

        if self._current_queue_size() == 0:
            op("execute_status").par.active = False
        return self._current_queue_size()