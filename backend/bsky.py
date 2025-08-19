#!/usr/bin/env python3

import requests
from datetime import datetime, timezone


class BskyClient:
    def __init__(self, pds_host, handle, password):
        self.pds_host = pds_host.rstrip('/')
        self.handle = handle
        self.password = password
        self.token = None
        self.session = requests.Session()

    def authenticate(self):
        endpoint = f"{self.pds_host}/xrpc/com.atproto.server.createSession"

        data = {
            "identifier": self.handle,
            "password": self.password
        }

        try:
            response = self.session.post(endpoint, json=data)
            response.raise_for_status()

            result = response.json()
            self.token = result.get('accessJwt')

            if self.token:
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                })
                return True
            return False

        except requests.exceptions.RequestException as e:
            print(f"error authenticating with bsky: {e}")
            return False

    def post(self, content):
        if not self.token:
            if not self.authenticate():
                return None

        endpoint = f"{self.pds_host}/xrpc/com.atproto.repo.createRecord"

        created_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        data = {
            "repo": self.handle,
            "collection": "app.bsky.feed.post",
            "record": {
                "text": content,
                "createdAt": created_at
            }
        }

        try:
            response = self.session.post(endpoint, json=data)
            response.raise_for_status()

            result = response.json()
            return result.get('validationStatus', 'unknown')

        except requests.exceptions.RequestException as e:
            print(f"error posting to bsky: {e}")
            return None
