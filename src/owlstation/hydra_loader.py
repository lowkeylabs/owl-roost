import os
from pathlib import Path

import click
from hydra import compose, initialize_config_dir
from hydra.core.hydra_config import HydraConfig
from hydra.errors import HydraException


def load_hydra_config(overrides=None):
    try:
        overrides = overrides or []

        cwd = Path.cwd()
        xdg_config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

        search_dirs = []

        if (cwd / "conf").exists():
            search_dirs.append(cwd / "conf")

        if (xdg_config_home / "owlstation" / "conf").exists():
            search_dirs.append(xdg_config_home / "owlstation" / "conf")

        # Package-installed configs (absolute path)
        import owlstation

        pkg_conf = Path(owlstation.__file__).parent / "conf"
        search_dirs.append(pkg_conf)

        # Highest priority first
        config_dir = search_dirs[0]

        with initialize_config_dir(
            version_base=None,
            config_dir=str(config_dir),
            job_name="owlstation",
        ):
            cfg = compose(
                config_name="config",
                overrides=overrides,
                return_hydra_config=True,
            )

        HydraConfig.instance().set_config(cfg)
        return cfg

    except HydraException as e:
        raise click.ClickException(str(e)) from None
