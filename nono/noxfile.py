import nox

nox.options.sessions = ['lint', 'tests', 'lint_notebooks', 'check_notebooks']
nox.options.reuse_existing_virtualenvs = True


@nox.session(python='3.8')
def tests(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    session.install('--quiet', '-r', 'requirements.txt')
    session.run('pytest', '--cov-report', 'term')


@nox.session(python='3.8')
def lint(session):
    session.install('flake8')
    session.run(
            'flake8',
            '--exclude=.git,__pycache__,.nox,.pytest_cache,target',
            '--select=W,E112,E113,F,C9,N8',
            '--ignore=E501,I202,F401,F841',
            '--show-source',
            # '.', 'noxfile.py')
            'episode01', 'episode02', 'episode03a', 'noxfile.py')


@nox.session
def lint_notebooks(session):
    # flakehell requieres toml
    # session.install('flake8', 'flakehell')
    # session.run(
    #        'flakehell',
    #        'lint',
    #        './notebooks/')
    session.install('nblint')
    session.install('--quiet', '-r', 'requirements.txt')

    import os
    for root, dirs, files in os.walk('./notebooks/'):
        if 'output' not in root:
            for name in files:
                for prefix in ['01', '02', '03a']:
                    if name.startswith(prefix) and name.endswith('.ipynb'):
                        if 'checkpoint' not in name:
                            filename = os.path.join(root, name)
                            session.run(
                                    'nblint',
                                    '--linter',
                                    'pyflakes',
                                    filename)


@nox.session
def check_notebooks(session):
    session.install('nbconvert')
    session.install('--quiet', '-r', 'requirements.txt')
    import os
    for root, dirs, files in os.walk('..'):
        if 'output' not in root:
            for name in files:
                for prefix in ['01', '02', '03a']:
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
