import shutil
from importlib.resources import files
from pathlib import Path

import click


@click.command("init")
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing configuration if it exists.",
)
def cmd_init(force: bool):
    """Initialize an OWL-Station project configuration."""
    cwd = Path.cwd()
    conf_dir = cwd / "conf"
    target = conf_dir / "config.yaml"

    if target.exists() and not force:
        raise click.ClickException("conf/config.yaml already exists. Use --force to overwrite.")

    conf_dir.mkdir(parents=True, exist_ok=True)

    src = files("owlstation.conf") / "config.yaml"
    shutil.copy(src, target)

    click.echo("✔ Created conf/config.yaml")
    click.echo("Edit this file to customize your project.")
