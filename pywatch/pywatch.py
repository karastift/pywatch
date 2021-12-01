#!/usr/bin/env python3

import os
from time import sleep
from sys import argv

# TODO: Use Popen or smth, to be able to kill the process when changes artdetected
# this requires the watch process to run in a seperate thread

class Pywatch:

    def __init__(
        self,
        file_path: str,
        interval: int = 1,
    ) -> None:
        
        if not os.path.exists(file_path):
            print('[!] File does not exist...')
            exit()
    
        self.file_path = file_path
        self.timestamp = self.refresh_timestamp()
        self.interval = interval
        self.active = False

        self.execute_program()

    def has_changed(self):
        old_stamp = self.timestamp
        new_stamp = self.refresh_timestamp()

        return old_stamp != new_stamp

    def refresh_timestamp(self) -> int:
        self.timestamp = os.stat(self.file_path).st_mtime
        
        return self.timestamp

    def execute_program(self):
        print('[!] Restarting program...')
        print('_________________________\n')

        os.system(f'/usr/bin/env python3 {self.file_path}')

    def start(self):
        self.active = True
        print(f'[+] Watching for changes on {self.file_path}...')
        
        try:
            while self.active:

                sleep(self.interval)

                if self.has_changed():
                    print('\n[+] Changes detected...')
                    self.execute_program()

        except KeyboardInterrupt:
            print('\n[!] Quitting...')
            self.active = False
            exit()


if __name__ == '__main__':
    pw = Pywatch(
            argv[1],
        )

    pw.start()
