from dataclasses import dataclass
from mimetypes import guess_extension


@dataclass(frozen=True)
class CompanyLogo:
    """Original image bytes and the media type reported by DEGIRO."""

    content: bytes
    content_type: str

    @property
    def extension(self) -> str:
        """File extension for the media type, or .bin when it is unknown."""
        return guess_extension(self.content_type, strict=False) or ".bin"
