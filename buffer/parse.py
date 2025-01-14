import datetime
import re
from pathlib import Path

from typing import Optional


def parse_threads(image_base: Path, data: str):
    "Parse threads and messages encoded as newline separated strings. - indicates a threaded message"
    threads = []
    thread = {"messages":[], "images": []}
    lines = data.splitlines()
    for line in lines:
        if line.strip().startswith("-"):
            message = line.strip(" -")
            message, images = extract_images(image_base, message)
            thread["messages"].append(message)
            thread["images"].append(images)
        else:
            if thread["messages"]:
                threads.append(thread)

            date_string, message = line.split(" ", 1)
            message, images = extract_images(image_base, message)

            dt = datetime.datetime.fromisoformat(date_string)
            thread = {"messages": [message], "timestamp": dt, "images": [images]}
    threads.append(thread)
    return threads


def extract_images(image_base: Optional[Path], message: str):
    image_regex = r"!\[\[([^\]]+)\]\]"
    images = [Path(x) for x in re.findall(image_regex, message)]

    relative_images = [i for i in images if not i.is_absolute()]

    if relative_images and image_base is None:
        raise Exception(f'Image paths are relative {relative_images} but no base path set')

    if image_base:
        images = [image_base / i for i in images]


    output = re.sub(image_regex, "", message)
    return output, images

if __name__ == "__main__":
    import pprint
    pprint.pprint(parse_threads("/images", """\
2025-01-13T21:14:45Z This is a tweet on its own.
2025-01-13T21:14:45Z This is a tweet with a picture ![[picture.png]]
2025-01-13T21:14:45Z This is a tweet with two pictures
 - With a thread ![[one.png]]
 - And three tweets ![[/absolute/image_path.png]] ![[three.png]]
"""))
    print("----")
    pprint.pprint(parse_threads(None, """\
2025-01-13T21:14:45Z This is a tweet with an absolute image ![[/abs/image.png]].
"""))
