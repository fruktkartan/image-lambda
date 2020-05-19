#!/usr/bin/env python3
"""Entry point for AWS Lambda function."""

import os
import boto3
import logging
import urllib
from io import BytesIO
from tempfile import TemporaryDirectory
from argparse import ArgumentParser, FileType
from PIL import Image, ImageOps
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def resize(file, dir, key):
    """Validate and create thumbs for file."""
    WIDTHS = [400, 600, 800, 1200]

    generated_images = []
    try:
        img = Image.open(file)
        if img.mode != "RGB":
            # Convert paletted images (e.g. png)
            img = img.convert("RGB")

        img = ImageOps.exif_transpose(img)

        for width in WIDTHS:
            resized = img.copy()
            resized.thumbnail((width, width))
            fn = f"{key}_{width}.jpg"
            fp = os.path.join(dir, f"{key}_{width}.jpg")
            resized.save(fp, "JPEG")
            generated_images.append((fn, fp))
    except:
        pass
    return(generated_images)


def handler(event, context):
    """Entry point for AWS Lambda function.

    This function is called every time a new file is uploaded
    to the `S3_bucket_in` bucket.
    """
    s3_resource = boto3.resource('s3')
    in_bucket = os.environ.get("S3_bucket_in")
    out_bucket = os.environ.get("S3_bucket_out")
    key = event["Records"][0]["s3"]["object"]["key"]
    key_unquote = urllib.parse.unquote_plus(key)
    logger.info(f"Parsing {key_unquote}")
    file = s3_resource.Object(bucket_name=in_bucket, key=key_unquote)
    buffer = BytesIO(file.get()["Body"].read())
    with TemporaryDirectory() as tmpdir:
        files = resize(buffer, tmpdir, key)
        for (fn, fp) in files:
            s3_resource.meta.client.upload_file(
                Filename=fp,
                Bucket=out_bucket,
                Key=fn,
                ExtraArgs={'ACL': "public-read"},
            )
    return({})


def cli(args):
    """Entry point from command line."""
    key = args.key or os.path.basename(args.input_file.name)
    files = resize(args.input_file.name, args.output, key)
    print(files)


if __name__ == "__main__":
    parser = ArgumentParser(description="Resize an image")
    parser.add_argument("-i", "--input", type=FileType('r'),
                        dest="input_file", required=True,
                        help="Input file")
    parser.add_argument("-o", "--output", required=True,
                        help="Where should we put downloaded documents?")
    parser.add_argument("-k", "--key",
                        help="Key, used as filename for generated files.")
    args = parser.parse_args()
    cli(args)
