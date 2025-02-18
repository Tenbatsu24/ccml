packages = [
    "pip",
    "black",
    "flake8",
    "isort",
    "python-dotenv",
    "pre-commit",
    "nbautoexport",
]

basic = [
    "numpy==1.26.4"
    "ipython",
    "jupyterlab",
    "matplotlib",
    "notebook",
    "pandas",
    "scikit-learn",
    "scikit-image",
    "einops",
    "opt_einsum",
]

scaffold = [
    "typer",
    "loguru",
    "tqdm",
]


def write_dependencies(
    dependencies, packages, pip_only_packages, repo_name, module_name, python_version
):
    if dependencies == "requirements.txt":
        with open(dependencies, "w") as f:
            lines = sorted(packages)

            lines += ["" "-e ."]

            f.write("\n".join(lines))
            f.write("\n")

    elif dependencies == "environment.yml":
        with open(dependencies, "w") as f:
            lines = [
                f"name: {repo_name}",
                "channels:",
                "  - conda-forge",
                "dependencies:",
            ]

            lines += [f"  - python={python_version}"]
            lines += [f"  - {p}" for p in packages if p not in pip_only_packages]

            lines += ["  - pip:"]
            lines += [f"    - {p}" for p in packages if p in pip_only_packages]
            lines += ["    - -e ."]

            f.write("\n".join(lines))
