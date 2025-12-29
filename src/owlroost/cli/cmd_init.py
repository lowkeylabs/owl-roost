import click
from loguru import logger

from owlroost.core.config_init import init_project_config


@click.command("init")
@click.option("--force", is_flag=True, help="Overwrite existing config.")
def cmd_init(force: bool):
    """
    Initialize an OWL-Station project configuration.
    """
    init_project_config(force=force)
    logger.success("OWL-Station configuration initialized in ./conf")
