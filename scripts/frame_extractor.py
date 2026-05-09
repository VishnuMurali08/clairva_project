"""
frame_extractor.py — DAY 1
Extracts frames from UCF101 videos at 1 fps.
Place .avi files in data/raw_videos/ before running.
"""

import cv2
import os
import json
from tqdm import tqdm


def extract_frames(video_path, output_dir, fps=1):
    """Extract frames from a single video file."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    save_dir = os.path.join(output_dir, video_name)
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open: {video_path}")
        return None

    video_fps   = cap.get(cv2.CAP_PROP_FPS) or 25
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration     = round(total_frames / video_fps, 2)
    interval     = max(1, int(video_fps / fps))

    saved = 0
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % interval == 0:
            timestamp = round(frame_idx / video_fps, 2)
            fname = f"frame_{saved:04d}_t{timestamp}s.jpg"
            cv2.imwrite(os.path.join(save_dir, fname), frame)
            saved += 1
        frame_idx += 1

    cap.release()
    return {
        "video_id":   video_name,
        "duration_s": duration,
        "fps_source": round(video_fps, 1),
        "frames_extracted": saved,
        "frame_dir":  save_dir,
    }


def process_all(video_dir="data/raw_videos", output_dir="data/frames"):
    """Process every video in video_dir, including subfolders like Fencing/, TaiChi/ etc."""
    exts = (".avi", ".mp4", ".mov", ".mkv")

    # Walk all subfolders recursively
    video_paths = []
    for root, dirs, files in os.walk(video_dir):
        for f in files:
            if f.lower().endswith(exts) and not f.startswith("."):
                video_paths.append(os.path.join(root, f))

    if not video_paths:
        print(f"\n No videos found in '{video_dir}' or its subfolders")
        print("   Make sure your Fencing/, TaiChi/, WalkingWithDog/ folders contain .avi files.\n")
        return

    # Group by category for nicer output
    categories = {}
    for vp in video_paths:
        cat = os.path.basename(os.path.dirname(vp))
        categories.setdefault(cat, []).append(vp)

    print(f"\n Found {len(video_paths)} videos across {len(categories)} categories:")
    for cat, vids in categories.items():
        print(f"   {cat}: {len(vids)} videos")
    print(f"\n   Extracting at 1 fps...\n")

    results = []

    for vpath in tqdm(video_paths, desc="Extracting"):
        # Include category name in output folder to avoid name collisions
        category = os.path.basename(os.path.dirname(vpath))
        cat_output_dir = os.path.join(output_dir, category)
        info = extract_frames(vpath, cat_output_dir)
        if info:
            info["category"] = category
            results.append(info)

    # Save manifest
    manifest_path = os.path.join(output_dir, "extraction_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)

    total_frames = sum(r["frames_extracted"] for r in results)
    print(f"\n Done — {len(results)} videos, {total_frames} frames total")
    print(f"   Manifest saved: {manifest_path}")
    print("   Next: python scripts/annotation_template.py\n")


if __name__ == "__main__":
    process_all()