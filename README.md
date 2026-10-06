# Wellknox content calendar, October 2026

Client review page for the October 2026 posting plan: carousels, reels and open testimonial slots.

- `index.html` is the finished page. Open it in a browser. Every post has Preview, Approve and Make changes.
  Approve and Make changes open WhatsApp (+91 79818 27087) with the post filled in.
- `previews/` holds small preview copies of the reels and carousel slides used by the Preview player.
- `thumbs/` holds the thumbnails embedded in the page.
- `build/build_calendar.py` rebuilds `index.html`. Edit the `P` dictionary at the top to change the plan.
- `build/encode_previews.sh` makes one preview file from a source video. `build/jobs.txt` lists the source path for each preview and is meant to be run from the `wellknox` folder, which is not part of this repo.

Rebuild: `python3 build/build_calendar.py`
