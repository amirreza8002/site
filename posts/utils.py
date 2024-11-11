import logging
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.cache import cache

from PIL import Image, ImageFile
import pillow_avif  # noqa: F401

from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.conf import defaults as default_settings, settings as sorl_settings
from sorl.thumbnail.engines.pil_engine import Engine
from sorl.thumbnail.helpers import tokey, serialize
from sorl.thumbnail.kvstores.base import KVStoreBase


logger = logging.getLogger(__name__)


def convert_pictures(filepath: str, format="AVIF", unlink=True, **kwargs):
    """
    Reformat uploaded pictures to any format
    """
    target_size: tuple[int, int] | None = kwargs.get("target_size", None)
    quality: int = kwargs.get("quality", 90)
    prefix: str = kwargs.get("prefix", "preview")
    final_path_function = kwargs.get(
        "final_path_function", lambda filepath, **kwargs: filepath.parent / "prev/"
    )

    blank_if_nonexistent = kwargs.get("blank_if_nonexistent", True)

    filepath: Path = Path(filepath)

    if not filepath.is_file() and blank_if_nonexistent:
        raise ValueError("Image does not exist")

    img: Image = Image.open(filepath)
    if img.format == format.upper():
        return filepath

    tmp_path = kwargs.get("tmp_path", filepath.parent)

    if kwargs.get("pil_verify", True):
        img.verify()
        img = Image.open(filepath)

    stem = filepath.stem
    # if size is specified, resize as well
    if target_size:
        assert isinstance(target_size, tuple)
        img.thumbnail(target_size)

    preview_path: Path = tmp_path / f"{prefix}{stem}_q{quality}.{format.lower()}"
    img.save(
        preview_path, format.upper(), quality=quality, method=kwargs.get("method", 5)
    )

    final_path: Path = final_path_function(filepath, **kwargs)
    final_path.mkdir(mode=0o775, parents=True, exist_ok=True)

    preview_path = preview_path.rename(final_path / preview_path.name)
    rel_path = preview_path.relative_to(settings.MEDIA_ROOT)
    logger.debug(f"Made preview at '{preview_path}'")

    if unlink:
        filepath.unlink()

    return rel_path


EXTENSIONS = {
    "JPEG": "jpg",
    "PNG": "png",
    "GIF": "gif",
    "WEBP": "webp",
    "AVIF": "avif",
}


class AvifBackend(ThumbnailBackend):
    def _get_thumbnail_filename(self, source, geometry_string, options):
        """
        Compute the destination filename.
        """
        key = tokey(source.key, geometry_string, serialize(options))
        path = f"{key[:2]}{key[2:4]}{key}"
        return f"{sorl_settings.THUMBNAIL_PREFIX}{path}.{EXTENSIONS[options["format"]]}"

    def _get_format(self, source):
        file_extension = self.file_extension(source)

        if file_extension == ".jpg" or file_extension == ".jpeg":
            return "JPEG"
        elif file_extension == ".avif":
            return "AVIF"
        elif file_extension == ".png":
            return "PNG"
        elif file_extension == ".gif":
            return "GIF"
        elif file_extension == ".webp":
            return "WEBP"
        else:
            from django.conf import settings

            return getattr(
                settings, "THUMBNAIL_FORMAT", default_settings.THUMBNAIL_FORMAT
            )


class AvifEngine(Engine):
    def _get_raw_data(
        self, image, format_, quality, image_info=None, progressive=False
    ):
        # Increase (but never decrease) PIL buffer size
        ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, image.size[0] * image.size[1])
        bf = BytesIO()

        params = {
            "format": format_,
            "quality": quality,
            "optimize": 1,
        }

        # keeps icc_profile
        if "icc_profile" in image_info:
            params["icc_profile"] = image_info["icc_profile"]

        raw_data = None

        if format_ == "JPEG" and progressive:
            params["progressive"] = True
        try:
            # Do not save unnecessary exif data for smaller thumbnail size
            params.pop("exif", {})
            image.save(bf, **params)
        except OSError:
            # Try without optimization.
            params.pop("optimize")
            image.save(bf, **params)
        else:
            raw_data = bf.getvalue()
        finally:
            bf.close()

        return raw_data


class DefaultKVStore(KVStoreBase):
    def __init__(self):
        super().__init__()
        self.connection = cache

    def _get_raw(self, key):
        return self.connection.get(key)

    def _set_raw(self, key, value):
        return self.connection.set(
            key, value, px=sorl_settings.THUMBNAIL_VALKEY_TIMEOUT * 1000
        )

    def _delete_raw(self, *keys):
        return self.connection.delete(*keys)

    def _find_keys_raw(self, prefix):
        pattern = prefix + "*"
        return list(
            map(lambda key: key.decode("utf-8"), self.connection.keys(pattern=pattern))
        )
