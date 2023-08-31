import subprocess

import Config


def git_pull(repo_path=Config.REPO_PATH):
    process = subprocess.Popen(['git', 'pull'], cwd=repo_path)
    process.wait()
    if process.returncode == 0:
        print("repo update successfully.")
    else:
        print("Error pull repo.")


def git_add(repo_path=Config.REPO_PATH):
    process = subprocess.Popen(['git', 'add', '.'], cwd=repo_path)
    process.wait()
    if process.returncode == 0:
        print('done')
    else:
        print('error')


def git_commit(msg, repo_path=Config.REPO_PATH):
    process = subprocess.Popen(['git', 'commit', '-m', msg], cwd=repo_path)
    process.wait()
    if process.returncode == 0:
        print('done')
    else:
        print('error')


def git_push(repo_path=Config.REPO_PATH):
    process = subprocess.Popen(['git', 'push', 'origin', '-o', 'main'], cwd=repo_path)
    process.wait()
    if process.returncode == 0:
        print('done')
    else:
        print('error')


# git_add()
# git_commit('init file')
git_push()
