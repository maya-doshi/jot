# jot

post to [memos](https://github.com/usememos/memos) and [bluesky](https://bsky.app) quickly from the cli

ported from my [shell script](https://github.com/maya-doshi/scripts/blob/main/memo_bsky.sh) cause it was getting annoying to modify

## features
- memos
  - text
  - visibility
  - audio recordings
- bsky support
  - text
  - two accounts

## usage

1. install dependencies:
   - ffmpeg (linux)
   - requests
   - some text editor, can be avoided. defaults to vim

2. fill variables in [config.py](./config.py)
  - notes
    - bsky urls are the pds urls not bsky.app
    - yes i know the way im doing secret management is bad look at the [todo](./TODO.md)

3. `./main.py`
