import os
import subprocess

from .. import SNAPSHOT_DIR, SNAPSHOT_KEEP_RENDERS, SNAPSHOT_CLEANUP_TIME, SNAPSHOT_PREFIX, SNAPSHOT_IMAGEMAGICK_PATH


# housekeeper script
def clean_old_files():
    if SNAPSHOT_KEEP_RENDERS:
        return
    outputDir = os.path.abspath(SNAPSHOT_DIR)
    for root, dir, files in os.walk(outputDir):
        for file in files:
            filePath = os.path.join(root, file)
            if file.startswith(SNAPSHOT_PREFIX) and os.path.getmtime(filePath) >= SNAPSHOT_CLEANUP_TIME:
                print(f"deleting {os.path.getmtime(filePath)} seconds old image {filePath}")
                os.remove(filePath)


async def crop_images(image_path):
    return subprocess.call([SNAPSHOT_IMAGEMAGICK_PATH, image_path, '-trim', image_path])


def trim_whitespace(image_path):
    """
    todo: deal with this later
    """
    from wand.image import Image
    from wand.color import Color

    with Image(filename = image_path) as img:
        img.trim(color = Color('rgba(0,0,0,0)'), fuzz = 0)
    img.save(filename = os.path.abspath(image_path))
    # img.close()
