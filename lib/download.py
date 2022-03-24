import requests, sys
from tqdm import tqdm
from pathlib import Path
#import commandline as cmd

# Start Logger
#log = cmd.logger("Downloads")

def downloader(url: str, path: str, resumeBytePosition: int = None):
    """Download ``url`` to disk with possible resumption.

    Parameters
    ----------
    url: str
        URL of the file to download
    path: str
        Path to download file to
    resume_byte_pos: int
        Position of byte from where to resume the download

    """
    # Get size of file
    r = requests.head(url)
    fileSize = int(r.headers.get('content-length', 0))
    initialPosition = resumeBytePosition if resumeBytePosition else 0

    # Append information to resume download at specific byte position
    # to header
    resumeHeader = ({'Range': f'bytes={resumeBytePosition}-'}
                     if resumeBytePosition else None)

    # Establish connection
    r = requests.get(url, stream=True, headers=resumeHeader)

    # Set configuration
    blockSize = 1024
    mode = 'ab' if resumeBytePosition else 'wb'

    with open(path, mode) as f:
        with tqdm(total=fileSize, unit='B',
                  unit_scale=True, unit_divisor=1024,
                  desc=path.name, initial=initialPosition,
                  ascii=True, miniters=1) as progressBar:
            for chunk in r.iter_content(32 * blockSize):
                f.write(chunk)
                progressBar.update(len(chunk))
        sys.stdout.flush()
        print("Download Compleate")
            


def downloadFile(url: str, path: str = None) -> None:
    """Start the file download

    Depending on the size of the file online and offline, resume the
    download if the file offline is smaller than online.

    Parameters
    ----------
    url: str
        URL of the file to download
    path: str
        Path to download file to (Filename of `url` if not specified)

    """
    # Establish connection to header of file
    r = requests.head(url)


    # Convert str to pathlib object
    path = Path(path)

    # Get filesize of online and offline file
    fileSizeOnline = int(r.headers.get('content-length', 0))

    if path.exists():
        print("File (" + str(path) + ") allready exists")
        fileSizeOffline = path.stat().st_size
        # If file allready exists resume download
        if fileSizeOnline >= fileSizeOffline: 
            print("Resuming download")
            downloader(url, path, fileSizeOffline)
        else: print("Download complete")
    else:
        print("Starting Download")
        downloader(url, path)