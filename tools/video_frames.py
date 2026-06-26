"""video_frames — read a video with ORDO: ffmpeg keyframes → native image vision → compaction.

There is no standard npx video-understanding MCP, so ORDO does video the REAL way (no placeholder, no extra
service): extract keyframes with ffmpeg, read them as IMAGES via the agent's native vision (Claude Code's Read
tool reads images), and ponytail-compact the per-frame notes. Run: `python tools/video_frames.py <video> [n=8] [out_dir]`.
Prints the frame paths for the agent to Read. Degrades with a clear message if ffmpeg is missing.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

_FF = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
_PROBE = shutil.which("ffprobe") or shutil.which("ffprobe.exe")


def extract(video, n: int = 8, out_dir=None):
    """Extract ~n evenly-spaced keyframes from `video` as JPGs. Returns the frame paths (for the agent to Read)."""
    if not _FF:
        raise RuntimeError("ffmpeg not found — install it, then ORDO reads the extracted frames as images (native vision).")
    video = Path(video)
    out = Path(out_dir) if out_dir else video.parent / (video.stem + "_frames")
    out.mkdir(parents=True, exist_ok=True)
    dur = 0.0
    if _PROBE:
        try:
            dur = float(subprocess.run([_PROBE, "-v", "error", "-show_entries", "format=duration",
                                        "-of", "default=nw=1:nk=1", str(video)], capture_output=True, text=True).stdout.strip() or 0)
        except Exception:
            dur = 0.0
    paths = []
    if dur > 0:  # even time sampling (the good path)
        step = dur / (n + 1)
        for i in range(1, n + 1):
            p = out / f"frame_{i:02d}.jpg"
            subprocess.run([_FF, "-y", "-ss", str(round(step * i, 2)), "-i", str(video),
                            "-frames:v", "1", "-q:v", "3", str(p)], capture_output=True)
            if p.exists():
                paths.append(str(p))
    else:  # fallback: thumbnail filter
        subprocess.run([_FF, "-y", "-i", str(video), "-vf", "thumbnail,fps=1", "-frames:v", str(n),
                        str(out / "frame_%02d.jpg")], capture_output=True)
        paths = sorted(str(x) for x in out.glob("frame_*.jpg"))
    return paths


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    if not args:
        print("usage: python tools/video_frames.py <video> [n=8] [out_dir]\n"
              "  extracts ~n keyframes; the agent then Reads each as an image (native vision) and ponytail-compacts\n"
              "  the per-frame notes. This is ORDO's video sight — ffmpeg keyframes + native image vision, NO MCP.\n"
              f"  ffmpeg present: {bool(_FF)} | ffprobe present: {bool(_PROBE)}")
        sys.exit(0)
    video = args[0]
    n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 8
    od = args[2] if len(args) > 2 else None
    try:
        frames = extract(video, n, od)
        print("\n".join(frames))
        print(f"# {len(frames)} keyframes — Read each as an image (native vision), then compact the per-frame notes (ponytail).")
    except Exception as e:
        print("video_frames:", e)
