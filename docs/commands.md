# List of `make` Commands

## `install`

This command verifies the presence of necessary tools and installs them if they are not already installed. The tools include:

- `Homebrew`
- `git`

- `uv`


The command also sets up the required Python version (specified in the `.python-version` file) using `uv`.

<details>
  <summary>Usage</summary>

```bash
make install
```

```bash
Verifying if Homebrew is installed...
Installing required tools...
git is already installed. Skipping.

uv is already installed. Skipping.
Setting up Python version 3.11.0
```

</details>

## `setup`

This command sets up the project development environment by configuring `uv`, initializing `git` (if required), and installing `pre-commit` hooks.

<details>
  <summary>Usage</summary>

```bash
make setup
```

```bash
Installing tools...
All tools installed successfully.
Setting up the project...

python3 --version
Python 3.11.0
Creating environment at '.venv'...
Installing with sync:
  Using index 'https://pypi.org/simple/' (https://pypi.org/simple/)...
  Copying pyproject.toml to disk...
  Resolving dependencies...
  Picked 66 packages to install:
    annotated-types==0.6.0
    anyio==4.2.0
    certifi==2023.11.17
    click==8.1.7
    ...
    python-dateutil==2.8.2
    pytz==2024.1
    regex==2023.12.25
    requests==2.31.0
    ...
    Installed 66 packages in 2.93s (pip: 1.75s)

Setting up git...
Setting up pre-commit...
pre-commit installed at .git/hooks/pre-commit
pre-commit installed at .git/hooks/commit-msg

Setup completed successfully!
```

</details>

## `types`


This command is not available with uv as it doesn't need a separate types plugin.

<details>
  <summary>Usage</summary>

```bash
make types
```

```bash

Command not available with uv.
```

</details>

## `clean`

This command cleans up your development environment by removing virtual environments, caches, and lock files.

<details>
  <summary>Usage</summary>

```bash
make clean
```

```bash
Uninstalling local packages...

rm -rf .venv uv.lock
Cleaning up project artifacts...
Cleanup completed.
```

</details>

## `test`

This command first updates dependencies using uv and builds the package. Then, it runs a full test suite using `pytest`, generating a coverage report, for all the source code.

<details>
  <summary>Usage</summary>

```bash
make test
```

```bash
Running tests...

uv run pytest tests --cov=src --cov-report term

---------- coverage: platform darwin, python 3.11.0-final-0 ----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
src/recipes/__init__.py      1      0   100%
--------------------------------------------------
TOTAL                             1      0   100%
```

</details>

## `tree`

This command generates a tree view of the project directory, excluding certain directories and files like `.venv`, `__pycache__`, and `.git`.

<details>
  <summary>Usage</summary>

```bash
make tree
```

```bash
.
├── .coverage
├── .github
│   ├── dependabot.yml
│   ├── pull_request_template.md
│   └── workflows
│       ├── ci.yml
│       ├── deploy-dab.yml
│       ├── semantic-pr.yml
│       └── semantic-release.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .vscode
│   ├── extensions.json
│   └── settings.json
├── Makefile
├── README.md
├── README_github.md
├── databricks.yml
├── dependabot.md
├── docs
│   ├── CHANGELOG.md
│   ├── api
│   │   ├── recipes
│   │   │   ├── index.html
│   │   │   └── main.html
│   │   └── tests
│   │       ├── default_test.html
│   │       └── index.html
│   ├── assets
│   │   ├── badge-coverage.svg
│   │   ├── badge-tests.svg
│   │   ├── make-clean.png
│   │   ├── make-deploy_dev.png
│   │   ├── make-destroy_dev.png
│   │   ├── make-install.png
│   │   ├── make-module-azure-devops.png
│   │   ├── make-module-dlt.png
│   │   ├── make-module-gitlab.png
│   │   ├── make-module-vscode.png
│   │   ├── make-module.png
│   │   ├── make-repo-github.png
│   │   ├── make-repo.png
│   │   ├── make-setup.png
│   │   ├── make-test.png
│   │   └── make-tree.png
│   ├── bundle_deployment.md
│   ├── cicd.md
│   ├── coding_standards.md
│   ├── commands.md
│   ├── getting_started.md
│   ├── index.md
│   ├── jobs
│   │   └── index.md
│   ├── modules.md
│   ├── notebooks
│   │   └── index.md
│   ├── release.md
│   └── tests
│       ├── coverage
│       │   ├── class_index.html
│       │   ├── coverage_html_cb_6fb7b396.js
│       │   ├── favicon_32_cb_58284776.png
│       │   ├── function_index.html
│       │   ├── index.html
│       │   ├── keybd_closed_cb_ce680311.png
│       │   ├── status.json
│       │   ├── style_cb_8e611ae1.css
│       │   ├── z_df71c8327dd0b782___init___py.html
│       │   └── z_df71c8327dd0b782_main_py.html
│       ├── coverage_report.md
│       ├── test_configuration.md
│       └── tests.md
├── mkdocs.yml
├── poetry.lock
├── poetry.toml
├── pyproject.toml
├── resources
│   ├── jobs
│   │   ├── ingest_dataset_using_dlt.yml
│   │   └── template_job.yml
│   └── notebooks
│       ├── dlt_ingest_dataset.py
│       └── hello_revodata.py
├── src
│   └──
│       ├── __init__.py
│       └── main.py
└── tests
    ├── __init__.py
    └── default_test.py

19 directories, 73 files
```

</details>

## `docs`

Our project uses `MkDocs` to generate comprehensive HTML documentation from markdown files in the `docs` directory. In addition, we use `pdoc3` to auto-generate HTML documentation (from doctrings) of modules and tests. XML coverage reports are generated by `pytest-cov` and are available for CI/CD purposes.

To generate documentation, run the following command:

<details>
  <summary>Usage</summary>

```bash
make docs
```

```bash
Generating HTML documentation...
docs/api/recipes/index.html
docs/api/recipes/main.html
docs/api/tests/index.html
docs/api/tests/default_test.html
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: ./site
INFO    -  Documentation built in 0.24 seconds
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.21 seconds
INFO    -  [14:20:30] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [14:20:30] Serving on http://127.0.0.1:8000/
```

</details>

<!--
HTML coverage reports are disabled by default. To enable them:
1. Edit the Makefile and uncomment the HTML coverage generation lines in the "docs" target
2. Run `make docs` to generate the HTML coverage report
3. See docs/tests/coverage_report.md for more information
-->
