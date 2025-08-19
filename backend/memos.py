#!/usr/bin/env python3

import requests
import base64
import os
import mimetypes
from pathlib import Path


class MemosClient:
    def __init__(self, url, token):
        self.url = url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def create_memo(self, content, visibility="PRIVATE"):
        endpoint = f"{self.url}/api/v1/memos"

        data = {
            "content": content,
            "visibility": visibility
        }

        try:
            response = self.session.post(endpoint, json=data)
            response.raise_for_status()

            result = response.json()
            return result.get('name', '')
        except requests.exceptions.RequestException as e:
            print(f"error creating memo: {e}")
            return None

    def upload_file(self, file_path, memo_id=None):
        endpoint = f"{self.url}/api/v1/resources"

        if not os.path.exists(file_path):
            print(f"file not found: {file_path}")
            return None

        file_path = Path(file_path)

        filename = file_path.name
        mime_type = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
        file_size = file_path.stat().st_size

        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')

        data = {
            "filename": filename,
            "content": file_content,
            "type": mime_type,
            "size": str(file_size)
        }

        if memo_id:
            data["memo"] = memo_id

        try:
            response = self.session.post(endpoint, json=data)
            response.raise_for_status()

            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            print(f"error uploading file: {e}")
            return None
