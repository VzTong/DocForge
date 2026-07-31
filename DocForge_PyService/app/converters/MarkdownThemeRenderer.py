"""
Utilities for loading and rendering Markdown themes.

Responsibility
--------------
This module is responsible for:

- Loading HTML templates (.j2)
- Loading one or more CSS stylesheets
- Rendering a complete HTML document

This module intentionally DOES NOT know anything about:

- Markdown parsing
- PDF generation
- WeasyPrint

Its only responsibility is converting:

    Template + CSS + HTML Body
            ↓
       Complete HTML Document
"""

from __future__ import annotations

from pathlib import Path

from app.converters.base import ConversionError

from jinja2 import Environment, FileSystemLoader

# Root directory containing all built-in Markdown themes.
#
# Structure:
#
# templates/
# └── markdown/
#     ├── modern/
#     ├── github/
#     └── cv/
#
THEME_ROOT = (
    Path(__file__).parent
    / "templates"
    / "markdown"
)

class MarkdownTheme:
    """
    Represents a Markdown rendering theme.

    Each theme directory contains:

    - template.j2      HTML template
    - *.css            One or more stylesheets

    Example:

        github/
            template.j2
            00-github.css
            10-override.css

    All CSS files are automatically merged in alphabetical order.
    """

    def __init__(self, name: str = "modern") -> None:
        """
        Initialize a rendering theme.

        Args:
            name:
                Theme name.
                Example:
                    modern
                    github
                    cv
        """
        self.name = name

        self._env = Environment(
            loader=FileSystemLoader(self.theme_dir)
        )

    # ------------------------------------------------------------------
    # Theme paths
    # ------------------------------------------------------------------

    @property
    def theme_dir(self) -> Path:
        """Return the directory of the selected theme."""
        return THEME_ROOT / self.name

    @property
    def template_path(self) -> Path:
        """Return the HTML template path."""
        return self.theme_dir / "template.j2"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate(self) -> None:
        """
        Ensure the theme exists.
        """
        if not self.theme_dir.exists():
            raise ConversionError(
                f"Theme '{self.name}' does not exist."
            )

        if not self.template_path.exists():
            raise ConversionError(
                f"Template file not found: {self.template_path}"
            )

    def _load_stylesheets(self) -> str:
        """
        Load every CSS file inside the theme directory.

        Files are merged alphabetically.

        Example:

            00-base.css
            10-layout.css
            20-print.css

        Returns:
            Combined CSS string.
        """
        if not self.theme_dir.is_dir():
            raise ConversionError(f"Theme directory does not exist: {self.theme_dir}")

        if not self.template_path.is_file():
            raise ConversionError(f"Template file does not exist: {self.template_path}")

        css_files = sorted(
            self.theme_dir.glob("*.css")
        )
        if not css_files:
            raise ConversionError(f"No CSS file found in theme '{self.name}'.")

        return "\n\n".join(
            css_file.read_text(encoding="utf-8")
            for css_file in css_files
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(
        self,
        *,
        title: str,
        body: str,
        **kwargs,
    ) -> str:
        """
        Render a complete HTML document.

        Args:
            title:
                HTML document title.

            body:
                HTML body generated from Markdown.

            **kwargs:
                Additional template variables passed to the Jinja2 template.
                This allows themes to use extra context (e.g. subtitle,
                contact) without modifying this method's signature.

        Returns:
            Complete HTML document.
        """

        self._validate()

        env = Environment(
            loader=FileSystemLoader(self.theme_dir)
        )

        template = env.get_template("template.j2")

        css = self._load_stylesheets()

        return template.render(
            title=title,
            css=css,
            body=body,
            **kwargs,
        )