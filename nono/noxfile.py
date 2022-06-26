# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in episodes and notebooks."""

import os

import nox

"""
nox.options.sessions = [
    'lint',
    'mypy',
    'pytype',
    'tests',
    'docs',
    'lint_notebooks',
    'check_notebooks'
]
"""
nox.options.sessions = [
    'lint',
    'mypy',
    'pytype',
    'tests',
    'docs',
    'lint_notebooks',
    'check_notebooks'
]

intro_prefixes = ['01', '02', '03a', '03b', '03c', '03d']
utils_prefixes = ['04']
solvers_prefixes = ['05']
current_prefix = ['05']
type_check_prefixes = utils_prefixes + solvers_prefixes
prefixes = intro_prefixes + type_check_prefixes
# prefixes = current_prefix

nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSION = "3.8"

BUILD_DIR = "build"


@nox.session(python=PYTHON_VERSION)
def lint(session):
    """Check code - configuration in .flake8."""
    session.log('================ lint ================')
    session.install("flake8",
                    "flake8-bandit",
                    "flake8-black",
                    "flake8-bugbear",
                    "flake8-docstrings",
                    "flake8-import-order",
                    "darglint")
    episodes = [f'episode{p}' for p in prefixes]
    session.run(
        'flake8',
        '--exclude=.git,__pycache__,.nox,.pytest_cache,target',
        # '--select=W,E112,E113,F,C9,N8',
        # '--ignore=E501,I202,F401,F841',
        '--show-source',
        # '--verbose',
        *episodes, 'noxfile.py', 'docs/conf.py')


@nox.session(python=PYTHON_VERSION)
def mypy(session):
    """Check types - configuration in mypy.ini."""
    session.log('================ mypy ================')
    session.install('mypy')
    session.run('pip', 'install', '--quiet', '-r', 'requirements.txt')
    session.install('--quiet', '-e', '.')
    episodes = [f'episode{p}' for p in prefixes
                if p >= "03"]
    session.run(
        'mypy',
        *episodes)


@nox.session(python=PYTHON_VERSION)
def pytype(session):
    """Check types with inference - inference based."""
    session.log('================ pytype ================')
    session.install('pytype')
    session.run('pip', 'install', '--quiet', '-r', 'requirements.txt')
    session.install('--quiet', '-e', '.')
    episodes = [f'episode{p}' for p in prefixes
                if p >= "03"]
    session.run(
        'pytype',
        *episodes)


@nox.session(python=PYTHON_VERSION)
def tests(session):
    """Unit test - configuration in pytest.ini."""
    session.log('================ tests ================')
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.run('pip', 'install', '--quiet', '-r', 'requirements.txt')
    session.install('--quiet', '-r', 'requirements.txt')
    session.run('pytest', '--cov-report', 'term')


@nox.session(python="3.8")
def docs(session):
    """Build the documentation.

    configuration in docs/conf.py.
    template in index.rst.
    """
    session.log('================ docs ================')
    session.install("sphinx")
    session.install('--quiet', '-r', 'requirements.txt')
    session.install('--quiet', '-e', '.')
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python=PYTHON_VERSION)
def lint_notebooks(session):
    """Check notebooks code."""
    # flakehell requieres toml
    # session.install('flake8', 'flakehell')
    # session.run(
    #        'flakehell',
    #        'lint',
    #        './notebooks/')
    session.log('================ lint_notebooks ================')
    session.install('nblint')
    session.install('--quiet', '-r', 'requirements.txt')

    import os
    for root, _dirs, files in os.walk('./notebooks/'):
        if 'output' not in root:
            for name in files:
                # for prefix in ['01', '02', '03a']:
                for prefix in prefixes:
                    if name.startswith(prefix) and name.endswith('.ipynb'):
                        if 'checkpoint' not in name:
                            filename = os.path.join(root, name)
                            session.run(
                                'nblint',
                                '--linter',
                                'pyflakes',
                                filename)


# TODO heck why it does not wor in venv (does not find constraint module)
# @nox.session(python=PYTHON_VERSION)
@nox.session(python=False)  # disable venv
def check_notebooks(session):
    """Check notebooks for runtime errors."""
    # session.install('nbconvert')
    # session.install('--quiet', '-r', 'requirements.txt')
    session.log('================ check_notebooks ================')
    session.run('pip', 'install', '--quiet', 'nbconvert')
    session.run('pip', 'install', '--quiet', '-r', 'requirements.txt')
    # import os
    for root, _dirs, files in os.walk('..'):
        if 'output' not in root:
            for name in files:
                # for prefix in ['01', '02', '03a']:
                for prefix in prefixes:
                    if name.startswith(prefix) and name.endswith('.ipynb'):
                        if 'checkpoint' not in name:
                            filename = os.path.join(root, name)
                            session.run(
                                'jupyter',
                                'nbconvert',
                                '--output-dir',
                                BUILD_DIR,
                                '--to',
                                'notebook',
                                '--execute',
                                '--output',
                                'check',
                                filename)
