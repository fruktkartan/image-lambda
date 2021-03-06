"""Tests for image resizer."""
from resize import resize
from tempfile import TemporaryDirectory
from os.path import isfile
from PIL import Image


def test_resize_jpg():
    """Create thumbs from jpg image."""
    with TemporaryDirectory() as tmpdir:
        files = resize("test/files/Körsbärsträd.jpg", tmpdir, "test")

        assert len(files) == 4

        for (fname, fpath) in files:
            assert isfile(fpath)

            with Image.open(fpath) as img:
                # Check that all image have the widths they nominally should
                assert fname == f"test_{img.width}.jpg"

                # Check that images have roughly the same aspect ratio as the
                # original
                aspect = img.width / img.height
                assert aspect > 1.32
                assert aspect < 1.33

                # Check that there is no exif data, or possibly only the
                # orientation
                exif = img.getexif()
                assert len(exif) == 0 or len(exif) == 1
                if len(exif) == 1:
                    assert 0x0112 in exif
