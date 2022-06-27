# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in notebooks."""

import os

import nox

nox.options.sessions = [
    'lint_notebooks',
    'check_notebooks'
]

prefixes = ['01', '02', '03a', '03b', '03c', '03d', '04', '05']

nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSION = "3.8"

BUILD_DIR = "build"


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
