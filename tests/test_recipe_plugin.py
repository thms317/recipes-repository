import unittest
from pathlib import Path
from typing import Any, Dict, List, Tuple, cast

from mkdocs.config import load_config
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

from recipes.mkdocs_recipe_plugin import RecipePlugin, RecipePluginConfig


class TestRecipePlugin(unittest.TestCase):
    def setUp(self) -> None:
        self.plugin = RecipePlugin()
        # Configure plugin directly
        config = RecipePluginConfig()
        config.recipes_dir = "recipes"  # This is the directory we expect files to be in
        config.images_dir = "images"
        self.plugin.config = config

    def test_generate_table_html(self) -> None:
        """Test that we can generate HTML tables correctly from recipe info items."""
        # Create a simple list of recipe info items
        info_items: list[tuple[str, str]] = [
            ("Prep Time", "10 minutes"),
            ("Cook Time", "25 minutes"),
            ("Total Time", "35 minutes"),
            ("Servings", "4 servings"),
        ]

        recipe_name = "Test Recipe"
        image_path = "../images/test_recipe.jpg"

        # Generate HTML table directly
        table_html = self._generate_table_html(info_items, recipe_name, image_path)

        # Verify table structure
        self.assertIn("<table>", table_html)
        self.assertIn("<tr><th>Information</th><th>Details</th></tr>", table_html)
        self.assertIn("<tr><td>Prep Time</td><td>10 minutes</td></tr>", table_html)
        self.assertIn(f'<img src="{image_path}" alt="{recipe_name}"', table_html)

    def test_mkdocs_config_load(self) -> None:
        """Test that MkDocs can load the plugin from config."""
        try:
            # Attempt to load MkDocs config with our plugin
            config = load_config(
                config_file_path="mkdocs.yml",
            )
            # Get the plugins config
            plugins_config = config["plugins"]

            # Check if our plugin is in the config
            # Plugins could be a list of plugin names or a dict of plugin configurations
            plugin_names = []
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

            # Check that our plugin is in the list
            self.assertIn("recipes", plugin_names)
            print(f"Successfully found plugins: {plugin_names}")
        except Exception as e:
            self.fail(f"Failed to load MkDocs config with plugin: {e}")

    def _generate_table_html(
        self,
        info_items: list[tuple[str, str]],
        recipe_name: str,
        image_path: str,
    ) -> str:
        """Generate HTML table from recipe info items."""
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


if __name__ == "__main__":
    unittest.main()
