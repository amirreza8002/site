import logging
from pathlib import Path

from django.conf import settings
from django.core.cache import cache

from PIL import Image
import pillow_avif  # noqa: F401

from sorl.thumbnail.conf import settings as sorl_settings
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


class DefaultKVStore(KVStoreBase):
    def __init__(self):
        super().__init__()
        self.connection = cache

    def _get_raw(self, key):
        return self.connection.get(key)

    def _set_raw(self, key, value):
        return self.connection.set(
            key, value, timeout=sorl_settings.THUMBNAIL_VALKEY_TIMEOUT * 1000
        )

    def _delete_raw(self, *keys):
        return self.connection.delete(*keys)

    def _find_keys_raw(self, prefix):
        pattern = prefix + "*"
        return list(
            map(lambda key: key.decode("utf-8"), self.connection.keys(pattern=pattern))
        )
