import os
from google.cloud import storage
from utils.helpers import log

SERVICE_ACCOUNT_FILE = ".cridentials/service_account.json"

if not os.path.exists(SERVICE_ACCOUNT_FILE):
    log(f"Must provide `{SERVICE_ACCOUNT_FILE}` to download the file.", "error")
    exit(0)


def download_to_local(bucket_name, filename):
    """
    Arguments:
        bucket_name:[str] - Bucket name.
        filename:[str] - filename or filepath in the bucket.
    Returns:
        None
    Description:
        `download` file from given `bucket` and `store` it to `local` directory.
    """
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    bucket = client.get_bucket(bucket_name)
    # Local Folder to store downloads
    folder = ".downloads/{}".format(filename)
    # List all objects that satisfy the filter.
    # Download the file to a destination
    delimiter = "/"
    blobs = bucket.list_blobs(prefix=filename, delimiter=delimiter)

    log("File download Started…. Wait for the job to complete.")
    # Create this folder locally if not exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Iterating through for loop one by one using API call
    for blob in blobs:
        log("Blobs: {}".format(blob.name))
        destination_uri = "{}/{}".format(folder, blob.name)
        blob.download_to_filename(destination_uri)
        log("Exported {} to {}".format(blob.name, destination_uri))

    client.close()
