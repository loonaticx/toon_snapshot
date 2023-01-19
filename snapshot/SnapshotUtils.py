import os

from .. import SNAPSHOT_DIR, SNAPSHOT_KEEP_RENDERS, SNAPSHOT_CLEANUP_TIME, SNAPSHOT_PREFIX


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


def trim_whitespace(image_path):
    from wand.image import Image
    from wand.color import Color

    with Image(filename = image_path) as img:
        img.trim(color = Color('rgba(0,0,0,0)'), fuzz = 0)
    img.save(filename = os.path.abspath(image_path))
    img.close()
