#!/bin/bash
# usage: enc.sh "kind|src|name"   (run from the wellknox folder: ../ of this repo)
IFS='|' read -r kind src name <<< "$1"
P="$(cd "$(dirname "$0")/.." && pwd)/previews"
if [ "$kind" = reel ]; then
  ffmpeg -v error -y -i "$src" -vf "scale=540:960" -c:v libx264 -crf 27 -preset medium -pix_fmt yuv420p -c:a aac -b:a 64k -movflags +faststart "$P/$name.mp4" </dev/null
else
  ffmpeg -v error -y -i "$src" -vf "scale=720:-2" -c:v libx264 -crf 28 -preset medium -pix_fmt yuv420p -an -movflags +faststart "$P/$name.mp4" </dev/null
fi
