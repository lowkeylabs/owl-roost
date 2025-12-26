import os
from pathlib import Path

import click
from hydra import compose, initialize_config_dir
from hydra.core.hydra_config import HydraConfig
from hydra.errors import HydraException


def load_hydra_config(overrides=None):
    """
    Load Hydra configuration with layered search paths.

    Primary config source:
      1. ./conf (if present)
      2. pkg://owlstation.conf

    Secondary (fallback) sources:
      - ~/.config/owlstation/conf
      - pkg://owlstation.conf
    """
    try:
        overrides = overrides or []

        cwd = Path.cwd()
        xdg_config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

        # -------- Primary config directory --------
        if (cwd / "conf").exists():
            primary_config_dir = cwd / "conf"
        else:
            import owlstation

            primary_config_dir = Path(owlstation.__file__).parent / "conf"

        # -------- Secondary search paths --------
        search_paths = []

        user_conf = xdg_config_home / "owlstation" / "conf"
        if user_conf.exists():
            search_paths.append(f"file://{user_conf}")

        # Package defaults ALWAYS available
        search_paths.append("pkg://owlstation.conf")

        hydra_overrides = [f"hydra.searchpath=[{','.join(search_paths)}]"]

        with initialize_config_dir(
            version_base=None,
            config_dir=str(primary_config_dir),
            job_name="owlstation",
        ):
            cfg = compose(
                config_name="config",
                overrides=hydra_overrides + overrides,
                return_hydra_config=True,
            )

        HydraConfig.instance().set_config(cfg)
        return cfg

    except HydraException as e:
        raise click.ClickException(str(e)) from None
