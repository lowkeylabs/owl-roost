# src/owlstation/hydra/owl_hydra_run.py

from pathlib import Path

import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf

from owlstation.core.owl_runner import run_single_case


@hydra.main(
    config_path=None,  # Use hydra.searchpath instead
    config_name="config",
    version_base=None,
)
def main(cfg: DictConfig):
    """
    Pure Hydra runner for OWL scenarios.

    - Uses ./conf from the *current working directory*
    - Supports single runs and multiruns (-m)
    - Produces one output workbook per scenario
    """

    # -----------------------------------------------------------------
    # Echo resolved config (very useful for Hydra debugging)
    # -----------------------------------------------------------------
    logger.info("Resolved Hydra configuration:\n{}", OmegaConf.to_yaml(cfg))

    # -----------------------------------------------------------------
    # Validate required inputs
    # -----------------------------------------------------------------
    if not hasattr(cfg, "case") or not hasattr(cfg.case, "file"):
        raise RuntimeError("Hydra config must define case.file (path to TOML case file).")

    case_file = Path(cfg.case.file)

    if not case_file.exists():
        raise FileNotFoundError(f"Case file not found: {case_file}")

    # -----------------------------------------------------------------
    # Build semantic overrides (domain-level)
    # -----------------------------------------------------------------
    overrides = {
        "longevity": {
            "Jack": int(cfg.longevity.jack),
            "Jill": int(cfg.longevity.jill),
        }
    }

    logger.info("Scenario overrides: {}", overrides)

    # -----------------------------------------------------------------
    # Hydra-managed run directory
    # -----------------------------------------------------------------
    # When using Hydra:
    #   - cwd is automatically changed to a unique run directory
    #   - Path.cwd() is safe and intentional here
    run_dir = Path.cwd()
    run_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------------------
    # Output filename (scenario-specific)
    # -----------------------------------------------------------------
    output_file = run_dir / (
        f"{case_file.stem}"
        f"_LE_J{overrides['longevity']['Jack']}"
        f"_I{overrides['longevity']['Jill']}.xlsx"
    )

    # -----------------------------------------------------------------
    # Run OWL via shared runner
    # -----------------------------------------------------------------
    result = run_single_case(
        case_file=str(case_file),
        overrides=overrides,
        output_file=str(output_file),
    )

    logger.info("Case status: {}", result.status)

    if result.status != "solved":
        logger.warning("Case did not solve; no output written.")
        return

    logger.info("Results saved to: {}", output_file)


if __name__ == "__main__":
    main()
