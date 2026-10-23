#!/usr/bin/env python3
"""Mouth opening per frame of a take, measured on the face (MediaPipe Face Landmarker), for resync.py (MOUTH=...).

The take's own audio is a poor proxy when it carries music or other voices (a take cut from a rendered video):
the picture is what the viewer checks, so we match the voice against the lips themselves.

  python3 mouth_open.py take30.mp4 face_landmarker.task mouth.npy
      writes one float per frame: inner-lip gap / face height (NaN where no face was found, then interpolated)
  model: https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
"""
import sys
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

video, model, out = sys.argv[1:4]
lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO, num_faces=1))
cap = cv2.VideoCapture(video)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
vals, k = [], 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    r = lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), int(k * 1000 / fps))
    if r.face_landmarks:
        p = r.face_landmarks[0]
        gap = abs(p[14].y - p[13].y)            # inner lower lip - inner upper lip
        face = abs(p[152].y - p[10].y)          # chin - forehead
        vals.append(gap / face if face else np.nan)
    else:
        vals.append(np.nan)
    k += 1
lm.close()
v = np.array(vals, float)
idx = np.arange(len(v)); good = ~np.isnan(v)
if good.any():
    v = np.interp(idx, idx[good], v[good])
np.save(out, v)
print(f"{out}: {len(v)} frames, face found on {good.mean():.0%}, gap p10/p50/p90 = {np.percentile(v, [10, 50, 90]).round(4)}")
