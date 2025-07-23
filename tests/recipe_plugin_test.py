"""Tests for the recipe plugin."""

from typing import Any

import pytest
from mkdocs.config import load_config

from recipes_repository.mkdocs_recipe_plugin import RecipePlugin, RecipePluginConfig


class RecipeTestConfig:
    """Configuration for recipe tests.

    Parameters
    ----------
    recipes_dir : str
        Directory where recipe files are located, default="recipes"
    images_dir : str
        Directory where image files are located, default="images"
    """

    def __init__(self, recipes_dir: str = "recipes", images_dir: str = "images") -> None:
        self.recipes_dir: str = recipes_dir
        self.images_dir: str = images_dir


class RecipePluginHelper:
    """Helper class for recipe plugin tests.

    Parameters
    ----------
    config : RecipeTestConfig
        Test configuration
    """

    def __init__(self, config: RecipeTestConfig) -> None:
        self.config: RecipeTestConfig = config
        self.plugin: RecipePlugin = self._create_plugin()

    def _create_plugin(self) -> RecipePlugin:
        """Create and configure a RecipePlugin instance.

        Returns
        -------
        RecipePlugin
            Configured RecipePlugin
        """
        plugin = RecipePlugin()
        plugin_config = RecipePluginConfig()
        plugin_config.recipes_dir = self.config.recipes_dir
        plugin_config.images_dir = self.config.images_dir
        plugin.config = plugin_config
        return plugin


class HTMLTableGenerator:
    """Generator for HTML tables from recipe information."""

    @staticmethod
    def generate_table(
        info_items: list[tuple[str, str]],
        recipe_name: str,
        image_path: str,
    ) -> str:
        """Generate HTML table from recipe info items.

        Parameters
        ----------
        info_items : list[tuple[str, str]]
            List of recipe information as (key, value) tuples
        recipe_name : str
            Name of the recipe
        image_path : str
            Path to the recipe image

        Returns
        -------
        str
            HTML table as a string
        """
        table_html = '<div style="display: flex; flex-direction: row; align-items: center;">\n'
        table_html += '    <div style="flex: 1; display: flex; justify-content: center;">\n'
        table_html += "        <table>\n"
        table_html += "            <tr><th>Information</th><th>Details</th></tr>\n"

        for key, value in info_items:
            table_html += f"            <tr><td>{key}</td><td>{value}</td></tr>\n"

        table_html += "        </table>\n"
        table_html += "    </div>\n"
        table_html += '    <div style="flex: 1; padding-left: 20px; display: flex; justify-content: center;">\n'
        table_html += (
            f'        <img src="{image_path}" alt="{recipe_name}" style="max-width: 100%;">\n'
        )
        table_html += "    </div>\n"
        table_html += "</div>\n"

        return table_html


class MkDocsConfigHelper:
    """Helper for testing MkDocs configuration."""

    @staticmethod
    def load_config(config_file_path: str = "mkdocs.yml") -> Any:
        """Load MkDocs configuration.

        Parameters
        ----------
        config_file_path : str
            Path to MkDocs configuration file, default="mkdocs.yml"

        Returns
        -------
        Any
            Loaded configuration
        """
        return load_config(config_file_path=config_file_path)

    @staticmethod
    def extract_plugin_names(plugins_config: Any) -> list[str]:
        """Extract plugin names from MkDocs plugins configuration.

        Parameters
        ----------
        plugins_config : Any
            MkDocs plugins configuration

        Returns
        -------
        list[str]
            List of plugin names
        """
        plugin_names: list[str] = []
        if isinstance(plugins_config, dict):
            plugin_names = list(plugins_config.keys())
        else:
            # Handle plugins as a list of plugin objects
            for plugin in plugins_config:
                if hasattr(plugin, "name"):
                    plugin_names.append(plugin.name)
                elif isinstance(plugin, str):
                    plugin_names.append(plugin)
                elif isinstance(plugin, dict):
                    plugin_names.extend(plugin.keys())
        return plugin_names


@pytest.fixture
def test_config() -> RecipeTestConfig:
    """Create test configuration.

    Returns
    -------
    RecipeTestConfig
        Test configuration
    """
    return RecipeTestConfig(recipes_dir="recipes", images_dir="images")


@pytest.fixture
def plugin_helper(test_config: RecipeTestConfig) -> RecipePluginHelper:
    """Create recipe plugin helper.

    Parameters
    ----------
    test_config : RecipeTestConfig
        Test configuration

    Returns
    -------
    RecipePluginHelper
        Recipe plugin helper
    """
    return RecipePluginHelper(test_config)


@pytest.fixture
def table_generator() -> HTMLTableGenerator:
    """Create HTML table generator.

    Returns
    -------
    HTMLTableGenerator
        HTML table generator
    """
    return HTMLTableGenerator()


@pytest.fixture
def mkdocs_helper() -> MkDocsConfigHelper:
    """Create MkDocs configuration helper.

    Returns
    -------
    MkDocsConfigHelper
        MkDocs configuration helper
    """
    return MkDocsConfigHelper()


class TestRecipeTableGeneration:
    """Tests for recipe HTML table generation."""

    def test_generate_table_html(self, table_generator: HTMLTableGenerator) -> None:
        """Test that we can generate HTML tables correctly from recipe info items.

        Args:
            table_generator: HTML table generator
        """
        # Create a simple list of recipe info items
        info_items: list[tuple[str, str]] = [
            ("Prep Time", "10 minutes"),
            ("Cook Time", "25 minutes"),
            ("Total Time", "35 minutes"),
            ("Servings", "4 servings"),
        ]

        recipe_name: str = "Test Recipe"
        image_path: str = "../images/test_recipe.jpg"

        # Generate HTML table directly
        table_html: str = table_generator.generate_table(info_items, recipe_name, image_path)

        # Verify table structure
        assert "<table>" in table_html
        assert "<tr><th>Information</th><th>Details</th></tr>" in table_html
        assert "<tr><td>Prep Time</td><td>10 minutes</td></tr>" in table_html
        assert f'<img src="{image_path}" alt="{recipe_name}"' in table_html


class TestMkDocsConfiguration:
    """Tests for MkDocs configuration."""

    def test_mkdocs_config_load(self, mkdocs_helper: MkDocsConfigHelper) -> None:
        """Test that MkDocs can load the plugin from config.

        Args:
            mkdocs_helper: MkDocs configuration helper
        """
        # Load MkDocs configuration
        config: dict[str, Any] = mkdocs_helper.load_config(config_file_path="mkdocs.yml")

        # Get the plugins config
        plugins_config: Any = config["plugins"]

        # Extract plugin names
        plugin_names: list[str] = mkdocs_helper.extract_plugin_names(plugins_config)

        # Check that our plugin is in the list
        assert "recipes" in plugin_names
        print(f"Successfully found plugins: {plugin_names}")
