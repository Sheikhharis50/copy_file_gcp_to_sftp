import pysftp, os
from utils.helpers import log

SFTP_SERVER = ""
SFTP_USERNAME = ""
SFTP_PORT = 22
SFTP_KEY_FILE = ".cridentials/sftp.pem"

if not os.path.exists(SFTP_KEY_FILE):
    log(f"Must provide `{SFTP_KEY_FILE}` to upload the file.", "error")
    exit(0)
if not SFTP_USERNAME or not SFTP_SERVER:
    log(
        f"Must provide `server/host and username` for sftp to made connection.",
        "error",
    )
    exit(0)


def change_directory(sftp: pysftp.Connection, remote_path: str):
    """
    Arguments:
        sftp:[pysftp.Connection] - sftp connection instance.
        remote_path:[str] - filename or filepath from the remote machine..
    Returns:
        True - if any folders were created.
        False - if not created any folder.
    Description:
        `change` to given directory, recursively making new folders if needed.
    """
    if remote_path == "/":
        # absolute path so change directory to root
        sftp.chdir("/")
        return
    if remote_path == "":
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_path)  # check if sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_path.rstrip("/"))
        change_directory(sftp, dirname)  # make parent directories
        sftp.mkdir(basename)  # sub-directory missing, so created it
        sftp.chdir(basename)
        return True


def sep_dir_with_file(path):
    dirname, basename = os.path.split(path.rstrip("/"))
    if "." in basename:
        return dirname
    return path


def upload_to_sftp(filename: str, remote_path: str):
    """
    Arguments:
        filename:[str] - filename or filepath from the local machine.
        remote_path:[str] - filename or filepath from the remote machine..
    Returns:
        None
    Description:
        `upload` given `local` file to `remote machine`.
    """
    sftp = None
    try:
        filepath = f".downloads/{filename}"
        if not os.path.exists(filepath):
            raise Exception(f"filename `{filepath}` does not exist.")

        sftp = pysftp.Connection(
            host=SFTP_SERVER,
            username=SFTP_USERNAME,
            private_key=SFTP_KEY_FILE,
            port=SFTP_PORT,
        )

        change_directory(sftp, sep_dir_with_file(remote_path))
        log(f"Changed to `{remote_path}` remote directory.")

        log(f"File `{filepath}` Uploading Started…. Wait for the job to complete.")
        sftp.put(filepath, remote_path)
        log(f"File `{filepath}` Uploaded to `{remote_path}` Successfully.")

        sftp.close()
    except Exception as e:
        log(str(e), "error")
