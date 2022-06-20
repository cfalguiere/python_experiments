import nox

nox.options.sessions = ["lint", "tests", "lint_notebooks", "check_notebooks"]
# 'mypy', 'pytype',
# prefixes = ['01', '02', '03a', '03b', '03c', '03d', '04']
prefixes = ['03b', '03c', '03d', "04"]

nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSION = "3.8"


@nox.session(python=PYTHON_VERSION)
def lint(session):
    """static checking - configuration in .flake8"""
    session.install("flake8",
                    "flake8-bandit",
                    "flake8-black",
                    "flake8-bugbear",
                    "flake8-import-order")
    episodes = [f'episode{p}' for p in prefixes]
    session.run(
            'flake8',
            '--exclude=.git,__pycache__,.nox,.pytest_cache,target',
            # '--select=W,E112,E113,F,C9,N8',
            # '--ignore=E501,I202,F401,F841',
            '--show-source',
            # '--verbose',
            *episodes, 'noxfile.py')


@nox.session(python=PYTHON_VERSION)
def mypy(session):
    """ static type checking - configuration in mypy.ini"""
    session.install('mypy')
    episodes = [f'episode{p}' for p in prefixes
                if p >= "04"]
    session.run(
            'mypy',
            *episodes)


@nox.session(python=PYTHON_VERSION)
def pytype(session):
    """ static type checking - inference based"""
    session.install('pytype')
    episodes = [f'episode{p}' for p in prefixes
                if p >= "04"]
    session.run(
            'pytype',
            *episodes)


@nox.session(python=PYTHON_VERSION)
def tests(session):
    """unit testing - configuration in pytest.ini"""
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.run('pytest', '--cov-report', 'term')


@nox.session(python=PYTHON_VERSION)
def lint_notebooks(session):
    """static checking of notebooks"""

    # flakehell requieres toml
    # session.install('flake8', 'flakehell')
    # session.run(
    #        'flakehell',
    #        'lint',
    #        './notebooks/')
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


@nox.session(python=PYTHON_VERSION)
def check_notebooks(session):
    """runtime checking of notebooks"""
    session.install('nbconvert')
    session.install('--quiet', '-r', 'requirements.txt')
    import os
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
                                    '--to',
                                    'notebook',
                                    '--execute',
                                    '--output',
                                    'check',
                                    filename)
