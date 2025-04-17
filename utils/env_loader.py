import os
from dotenv import load_dotenv

load_dotenv()

NUTANIX_PC_IP = os.getenv("NUTANIX_PC_IP")
NUTANIX_PC_PORT = os.getenv("PORT", "9440")
NUTANIX_PC_USERNAME = os.getenv("NUTANIX_PC_USERNAME")
NUTANIX_PC_PASSWORD = os.getenv("NUTANIX_PC_PASSWORD")

if not all([NUTANIX_PC_IP, NUTANIX_PC_PORT, NUTANIX_PC_USERNAME, NUTANIX_PC_PASSWORD]):
    raise RuntimeError("Missing one or more required environment variables: NUTANIX_PC_IP, USERNAME, PASSWORD, PORT")