import glob
import logging
import pandas as pd
from os import getenv
from dotenv import load_dotenv

# --------------------------------------------------------------------------------------
load_dotenv()

LOG = logging.getLogger()

def initLogger() -> None:
    # Configure logging settings
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='app.log',
                        filemode='w')

    # Create a StreamHandler and set the level to DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the level to DEBUG or any desired level

    # Create a formatter and set it for the StreamHandler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    LOG.addHandler(console_handler)

# Creating global variables
RAW_FILE_DESTINATION = getenv("RAW_FILE_DESTINATION")
PARTITIONED_FILE_DESTINATION = getenv("PARTITIONED_FILE_DESTINATION")

# --------------------------------------------------------------------------------------

def main():
    # Initialize logger
    initLogger()

    # Download files from SFTP?
    pass

    # Read from raw file destination -----
    files = glob.glob(f"{RAW_FILE_DESTINATION}/*.csv")
    LOG.info(f"{len(files)} raw file(s) identified.")

    # Process Files
    grouped_df = pd.concat(
        [pd.read_csv(_) for _ in files], axis=0, ignore_index=True
    ).groupby("Drug Name")

    # Write file groups
    for name, data in grouped_df:
        LOG.info(f"Writing {name} of shape {data.shape}.")
        filepath = f"{PARTITIONED_FILE_DESTINATION}/{name.lower().replace(" ", "_")}.csv"
        data.to_csv(filepath)
        LOG.info(f"Group {name} of shape {data.shape} successfully written to {filepath}.")
        pass

    # Write to SFTP?
    pass

    # Return
    return


if __name__ == "__main__":
    main()
