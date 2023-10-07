import os
import paramiko
import fnmatch
from stat import S_ISDIR

def fetch_files_recursive_sftp(sftp, remote_path, local_path, pattern):
    for item in sftp.listdir_attr(remote_path):
        remote_item_path = os.path.join(remote_path, item.filename)
        local_item_path = os.path.join(local_path, os.path.basename(item.filename))

        if S_ISDIR(item.st_mode):
            fetch_files_recursive_sftp(sftp, remote_item_path, local_path, pattern)
        elif os.path.exists(local_item_path):
            print(f"File {item.filename} already exists in the target path. Skipping...")
            continue
        elif fnmatch.fnmatch(item.filename, pattern):
            try:
                print(f"Starting download {item.filename}")
                sftp.get(remote_item_path, local_item_path)
                print(f"Downloaded {item.filename}")
            except Exception as e:
                print(f"Error downloading {item.filename}: {e}")

def fetch_files_via_sftp(hostname, port, username, password, remote_path, local_path, pattern):
    transport = paramiko.Transport((hostname, int(port)))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        fetch_files_recursive_sftp(sftp, remote_path, local_path, pattern)
    finally:
        sftp.close()
        transport.close()

required_parameters = {
    'sftp_host': os.getenv('sftp_host'),
    'sftp_port': os.getenv('sftp_port'),
    'sftp_user': os.getenv('sftp_user'),
    'sftp_password': os.getenv('sftp_password'),
    'sftp_path': os.getenv('sftp_path'),
    'sftp_local_path': '/downloads',
    'sftp_file_pattern': os.getenv('sftp_file_pattern')
}

if(all(value is not None for value in required_parameters.values())):
    fetch_files_via_sftp(
        hostname=required_parameters['sftp_host'],
        port=required_parameters['sftp_port'],
        username=required_parameters['sftp_user'],
        password=required_parameters['sftp_password'],
        remote_path=required_parameters['sftp_path'],
        local_path=required_parameters['sftp_local_path'],
        pattern=required_parameters['sftp_file_pattern']
    )
else:
    print('Not all environment variables are set')
    print(required_parameters)
