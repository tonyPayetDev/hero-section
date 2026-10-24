#!/usr/bin/env python3
"""Clean a background-removal matte with a person mask (MediaPipe selfie multiclass segmenter).

hyperframes remove-background sometimes keeps a piece of the room glued to the subject (a dark board behind
the head, a lamp…) and leaves small floating islands. A second, person-only segmenter knows a board is not a
person: the final alpha is the matte's alpha (fine edges, hair) inside a dilated person mask (no room).

  python3 clean_matte.py SRC.mp4 MATTE.webm MODEL.tflite OUT.webm [--frames N] [--grow 28]
      MODEL: https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite
      needs mediapipe + opencv-python-headless; on a headless box link Chromium's libEGL (see SKILL.md)
"""
import argparse, shutil, subprocess
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("matte"); ap.add_argument("model"); ap.add_argument("out")
ap.add_argument("--frames", type=int, default=0)
ap.add_argument("--grow", type=int, default=28, help="px the person mask is grown by, so hair and motion blur stay")
ap.add_argument("--below", type=int, default=0, help="rows below this y keep the matte as is (the person model misses dark, blurred legs); 0 = whole frame")
ap.add_argument("--island", type=int, default=6000, help="drop alpha islands smaller than this many pixels")
a = ap.parse_args()
FF = shutil.which("ffmpeg") or "ffmpeg"
FP = FF.replace("ffmpeg", "ffprobe")
W, H = map(int, subprocess.check_output([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", a.src]).decode().split(","))
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=a.model), running_mode=vision.RunningMode.VIDEO, output_category_mask=True))
n = ["-frames:v", str(a.frames)] if a.frames else []
rgb_p = subprocess.Popen([FF, "-v", "error", "-i", a.src, *n, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
al_p = subprocess.Popen([FF, "-v", "error", "-c:v", "libvpx-vp9", "-i", a.matte, *n, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "22", "-row-mt", "1", "-deadline", "good",
                        "-cpu-used", "4", "-auto-alt-ref", "0", a.out], stdin=subprocess.PIPE)
grow = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.grow + 1, 2 * a.grow + 1))
k, removed = 0, 0
while True:
    b1 = rgb_p.stdout.read(W * H * 3); b2 = al_p.stdout.read(W * H * 4)
    if len(b1) < W * H * 3 or len(b2) < W * H * 4:
        break
    rgb = np.frombuffer(b1, np.uint8).reshape(H, W, 3)
    rgba = np.frombuffer(b2, np.uint8).reshape(H, W, 4).copy()
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)), int(k * 1000 / 30))
    person = (r.category_mask.numpy_view() > 0).astype(np.uint8)          # 0 = background, 1..5 = hair/body/face/clothes/other
    person = cv2.dilate(cv2.resize(person, (W, H), interpolation=cv2.INTER_NEAREST), grow)
    soft = cv2.GaussianBlur(person.astype(np.float32), (31, 31), 0)
    if a.below:
        ramp = np.clip((np.arange(H, dtype=np.float32) - a.below) / 120.0, 0, 1)[:, None]     # fade to « keep » over 120 px
        soft = np.maximum(soft, ramp)
    alpha = rgba[..., 3].astype(np.float32)
    before = (alpha > 40).sum()
    alpha *= soft
    keep = (alpha > 40).astype(np.uint8)
    cnt, lab, stats, _ = cv2.connectedComponentsWithStats(keep, connectivity=8)
    alpha[np.isin(lab, [i for i in range(1, cnt) if stats[i, cv2.CC_STAT_AREA] < a.island])] = 0
    removed += int(before - (alpha > 40).sum())
    rgba[..., 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    rgba[..., :3] = rgb                         # colour from the source (the matte's own colour is a lossy copy)
    enc.stdin.write(rgba.tobytes()); k += 1
seg.close()
enc.stdin.close(); enc.wait()
print(f"{a.out}: {k} frames, {removed / max(1, k):.0f} px/frame given back to the room")
