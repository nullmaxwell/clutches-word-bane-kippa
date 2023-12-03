import glob
import paramiko
from os import getenv


class SFTP:
    SFTP_HOST = getenv("SFTP_HOST")
    SFTP_PORT = getenv("SFTP_PORT")
    SFTP_USER = getenv("SFTP_USER")
    SFTP_SECRET = getenv("SFTP_SECRET")
    SFTP_SOURCE_PATH = getenv("SFTP_SOURCE_PATH")
    SFTP_DESTNIATION_PATH = getenv("SFTP_DESTNIATION_PATH")
    RAW_FILE_DESTINATION = getenv("RAW_FILE_DESTINATION")
    PARTITIONED_FILE_DESTINATION = getenv("PARTITIONED_FILE_DESTINATION")

    def getDataFromRemote(
        host: str = getenv("SFTP_HOST"),
        port: int = getenv("SFTP_PORT"),
        user: str = getenv("SFTP_USER"),
        secret: str = getenv("SFTP_SECRET"),
        remote_dir: str = getenv("SFTP_SOURCE_PATH"),
        local_dir: str = getenv("RAW_FILE_DESTINATION"),
    ):
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=secret)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in the remote directory
        remote_files = sftp.listdir(remote_dir)

        # Download each file to the local directory
        for filename in remote_files:
            remote_file_path = f"{remote_dir}/{filename}"
            local_file_path = f"{local_dir}/{filename}"
            sftp.get(remote_file_path, local_file_path)

        sftp.close()
        transport.close()

    def pushDataToRemote(
        host: str = getenv("SFTP_HOST"),
        port: int = getenv("SFTP_PORT"),
        user: str = getenv("SFTP_USER"),
        secret: str = getenv("SFTP_SECRET"),
        remote_dir: str = getenv("SFTP_DESTNIATION_PATH"),
        local_dir: str = getenv("PARTITIONED_FILE_DESTINATION"),
    ):
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=secret)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in the local directory
        files = glob.glob(f"{local_dir}/*.csv")

        # Upload each file to the remote directory
        for filename in files:
            remote_file_path = f"{remote_dir}/{filename}"
            sftp.put(filename, remote_file_path)

        sftp.close()
        transport.close()
