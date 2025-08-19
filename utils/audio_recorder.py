#!/usr/bin/env python3

import subprocess
import tempfile
import os
from datetime import datetime
from pathlib import Path
import socket


class AudioRecorder:

    def __init__(self):
        self.ffmpeg_path = 'ffmpeg'  # assume ffmpeg is in path
        self.dir = Path(tempfile.mkdtemp())

    def record(self):
        now = datetime.now()
        title = now.strftime('%Y-%m-%d %H:%M:%S')
        artist = os.getenv('USER', 'unknown')
        creation_time = now.strftime('%Y-%m-%dT%H:%M:%S%Z')
        hostname = socket.gethostname()

        audio_file = self.dir / f"{now.strftime('%Y-%m-%d_%H:%M:%S')}.ogg"

        cmd = [
            self.ffmpeg_path,
            '-f', 'alsa', # assume on linux
            '-i', 'default',
            '-metadata', f'title={title}',
            '-metadata', f'artist={artist}',
            '-metadata', f'creation_time={creation_time}',
            '-metadata', f'comment={hostname}',
            '-hide_banner',
            str(audio_file)
        ]

        try:
            print("starting audio recording... (press q to stop)")
            subprocess.run(cmd, check=True)
            return str(audio_file)
        except subprocess.CalledProcessError as e:
            print(f"error recording audio: {e}")
            return None
        except KeyboardInterrupt:
            print("\nrecording stopped by user")
            if audio_file.exists():
                return str(audio_file)
            return None
