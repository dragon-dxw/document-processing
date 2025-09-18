import boto3
import subprocess
from subprocess import STDOUT, PIPE
import os
from typing import Any


class MyModel:
    def __init__(self, name: Any, value: Any):
        self.name = name
        self.value = value

    def save(self) -> None:
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.put_object(Bucket="mybucket", Key=self.name, Body=self.value)


def clean_pdf(pdf_filename: str, verify_removal: bool = True) -> None:
    # assert that the pdf exists
    if not os.path.exists(pdf_filename):
        raise RuntimeError(f"No pdf found at {pdf_filename}")

    # Add a blank metadata update to the PDF and linearize it to remove it entirely
    # both write back to pdf_filename
    subprocess.run(["exiftool", "-all:all=", pdf_filename], timeout=10, check=True)
    subprocess.run(
        ["qpdf", "--linearize", "--replace-input", pdf_filename], timeout=10, check=True
    )

    if verify_removal:
        # attempting to restore metadata will fail if we've linearized -- good!
        output = subprocess.run(
            ["exiftool", "-pdf-update:all=", pdf_filename],
            stdout=PIPE,
            stderr=STDOUT,
            timeout=10,
        )
        if b"no previous ExifTool update" not in output.stdout:
            raise RuntimeError("ExifTool data reversable")


if __name__ == "__main__":
    while True:
        print(":)")
