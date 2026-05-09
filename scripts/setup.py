"""
setup.py — Run this FIRST
Creates all project folders and confirms your environment is ready.
"""

import os
import sys

FOLDERS = [
    "data/raw_videos",
    "data/frames",
    "schemas",
    "annotations",
    "qa_reports",
    "guidelines",
    "outputs/charts",
    "notebooks",
    "scripts",
]

def create_folders():
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)
    print("All folders created")

def check_python():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Python 3.8+ required. You have:", sys.version)
    else:
        print(f"Python {version.major}.{version.minor} detected")

def check_packages():
    required = ["pandas", "numpy", "cv2", "matplotlib",
                "jsonschema", "sklearn", "seaborn", "tqdm"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f" Missing packages: {missing}")
        print("   Run: pip install -r requirements.txt")
    else:
        print(" All packages installed")

def create_data_readme():
    msg = (
        "# data/raw_videos\n\n"
        "Place your UCF101 .avi video files here.\n\n"
        "Download from: https://www.crcv.ucf.edu/data/UCF101.php\n\n"
        "Recommended categories (3 folders only):\n"
        "- WalkingWithDog\n"
        "- TaiChi\n"
        "- Fencing\n\n"
        "Copy ~25 .avi files from each category into this folder.\n"
        "Rename them like: HandshakeGreeting_001.avi for clarity.\n"
    )
    with open("data/raw_videos/README.md", "w") as f:
        f.write(msg)
    print("data/raw_videos/README.md written")

if __name__ == "__main__":
    print("\n AsiaInteract — Project Setup\n")
    check_python()
    create_folders()
    create_data_readme()
    check_packages()
    print("\n Setup complete!")
    print("  Next step: place UCF101 videos in data/raw_videos/")
    print("    Then run: python scripts/frame_extractor.py\n")
