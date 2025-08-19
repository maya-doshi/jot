#!/usr/bin/env python3

import argparse
import tempfile
import subprocess
import os
import sys
from pathlib import Path

from config import Config
from backend.memos import MemosClient
from backend.bsky import BskyClient
from utils.audio_recorder import AudioRecorder


def get_memo_content(memo_text=None):
    if memo_text:
        return memo_text

    editor = os.environ.get('EDITOR', 'vim')

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        subprocess.run([editor, temp_file_path], check=True)

        with open(temp_file_path, 'r') as f:
            content = f.read().strip()

        return content
    finally:
        os.unlink(temp_file_path)


def main():
    parser = argparse.ArgumentParser(description='Post to memos and bsky')
    parser.add_argument('-m', '--memo', help='Memo text')
    parser.add_argument('-a', '--audio', action='store_true', help='Record audio')
    parser.add_argument('-p', '--public', action='store_true', help='Make public')
    parser.add_argument('-b', '--bsky', action='store_true', help='Post to bsky')
    parser.add_argument('-x', '--pubsky', action='store_true', help='Post to pubsky')

    args = parser.parse_args()

    config = Config()
    if not config.validate():
        print("configuration is incomplete. please check config.py")
        sys.exit(1)

    memo_content = get_memo_content(args.memo)
    audio_file = None

    if args.audio:
        recorder = AudioRecorder()
        audio_file = recorder.record()
        print(f"audio recorded to: {audio_file}")

    if not memo_content and not audio_file:
        print("memo and audio can't both be empty")
        sys.exit(1)

    bsky_client = None
    pubsky_client = None

    if args.bsky and config.bsky_config_complete():
        bsky_client = BskyClient(config.PDSHOST, config.BSKY_HANDLE, config.BSKY_PASS)
        if not bsky_client.authenticate():
            print("failed to authenticate with bsky")
            bsky_client = None

    if args.pubsky and config.pubsky_config_complete():
        pubsky_client = BskyClient(config.PUBSKY_PDSHOST, config.PUBSKY_HANDLE, config.PUBSKY_PASS)
        if not pubsky_client.authenticate():
            print("failed to authenticate with pubsky")
            pubsky_client = None

    if bsky_client and memo_content:
        print("posting to bsky...")
        result = bsky_client.post(memo_content)
        print(f"bsky result: {result}")

    if pubsky_client and memo_content:
        print("posting to pubsky...")
        result = pubsky_client.post(memo_content)
        print(f"pubsky result: {result}")

    memos_client = MemosClient(config.URL, config.TOKEN)
    visibility = "PUBLIC" if args.public else "PRIVATE"

    if memo_content or audio_file:
        memo_id = memos_client.create_memo(memo_content, visibility)
        print(f"created memo: {memo_id}")

        if audio_file:
            print("uploading audio...")
            result = memos_client.upload_file(audio_file, memo_id)
            print(f"audio upload result: {result}")

            try:
                os.unlink(audio_file)
                parent_dir = Path(audio_file).parent
                if parent_dir.exists() and not any(parent_dir.iterdir()):
                    parent_dir.rmdir()
            except Exception as e:
                print(f"warning: could not clean up audio file: {e}")


if __name__ == "__main__":
    main()
