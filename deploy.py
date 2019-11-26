import sys
import subprocess as sp
import logging
import shutil

run = lambda x: sp.run(x, shell=True, capture_output=True)

abort = lambda: exit(-1)

if __name__ == '__main__':
    branch = run("git branch")
    branch = [ line[2:].strip() for line in branch.stdout.decode('utf-8').split('\n') if line.startswith("*") ][0]

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )
    logger = logging.getLogger()

    if branch != 'master':
        logger.error(f"Need to be on branch master (currently on {branch})")
        abort()

    changes = run("git status -s").stdout.decode('utf-8').split('\n')
    not_docs = [ line for line in changes if not line[3:].startswith('docs') and len(line) > 0 ]

    if not_docs:
        logger.error(f"Changes other than docs/:\n" + '\n'.join(not_docs))
        abort()

    logging.info(run("make all").stdout.decode('utf-8'))
    logging.info("Removing docs...")
    shutil.rmtree("docs")
    logging.info(run("bundle exec jekyll build").stdout.decode('utf-8'))
    logging.info(run("git add -A").stdout.decode('utf-8'))
