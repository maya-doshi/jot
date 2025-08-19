#!/usr/bin/env python3

class Config:
    def __init__(self):
        # memos configuration
        self.URL = ''
        self.TOKEN = ''

        # bsky configuration
        self.PDSHOST = ''
        self.BSKY_HANDLE = ''
        self.BSKY_PASS = ''

        # pubsky configuration
        self.PUBSKY_PDSHOST = ''
        self.PUBSKY_HANDLE = ''
        self.PUBSKY_PASS = ''

    def validate(self):
        if not self.URL or not self.TOKEN:
            print("Error: URL and TOKEN are required for memos")
            return False
        return True

    def bsky_config_complete(self):
        return bool(self.PDSHOST and self.BSKY_HANDLE and self.BSKY_PASS)

    def pubsky_config_complete(self):
        return bool(self.PUBSKY_PDSHOST and self.PUBSKY_HANDLE and self.PUBSKY_PASS)
