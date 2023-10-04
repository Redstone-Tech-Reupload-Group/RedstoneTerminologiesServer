import subprocess

try:
    import Config_private as Config
except ImportError:
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
        return 'push done'
    else:
        return 'push fail'


def git_checkout(repo_path=Config.REPO_PATH):
    process = subprocess.Popen(['git', 'checkout', '.'], cwd=repo_path)
    process.wait()
    if process.returncode == 0:
        return '已撤销本地改动'
    else:
        return 'fail'
