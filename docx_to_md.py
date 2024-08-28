import os
import subprocess
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_docx_to_md(docx_path, output_dir):
    """
    Convert a DOCX file to Markdown using pandoc.

    Args:
        docx_path (str): The path to the DOCX file.
        output_dir (str): The directory where the Markdown file and media will be saved.
    
    Raises:
        RuntimeError: If the pandoc conversion process fails.
    """
    try:
        # Extract the base filename without the extension
        base_filename = os.path.splitext(os.path.basename(docx_path))[0]
        # Define the output Markdown file path
        md_path = os.path.join(output_dir, f"{base_filename}.md")
        # Define the media extraction directory
        media_dir = os.path.join(output_dir, f"{base_filename}_files")
        # Build the pandoc command
        command = ["pandoc", "--extract-media", media_dir, "-s", docx_path, "-o", md_path]
        
        # Run the command and check for errors
        subprocess.run(command, check=True)
        print(f"Successfully converted {docx_path} to {md_path} and extracted media to {media_dir}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error converting {docx_path}: {e}")

def scan_and_convert(directory, destination, max_workers=4):
    """
    Recursively scan directories and convert DOCX files to Markdown.

    Args:
        directory (str): The root directory to start scanning.
        destination (str): The directory where the Markdown files and media will be saved.
        max_workers (int, optional): The maximum number of worker threads for parallel conversion. Defaults to 4.

    Raises:
        ValueError: If the provided directory or destination is invalid.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The provided directory path is invalid: {directory}")
    if not os.path.isdir(destination):
        raise ValueError(f"The provided destination path is invalid: {destination}")

    docx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".docx", ".doc")):
                docx_path = os.path.join(root, file)
                # Calculate relative path for proper media extraction
                relative_path = os.path.relpath(root, directory)
                output_dir = os.path.join(destination, relative_path)
                # Ensure the output directory exists
                os.makedirs(output_dir, exist_ok=True)
                docx_files.append((docx_path, output_dir))

    # Multithreaded conversion
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(convert_docx_to_md, docx, out_dir) for docx, out_dir in docx_files]
        for future in as_completed(futures):
            try:
                future.result()  # Retrieve results to ensure exceptions are raised
            except Exception as e:
                print(f"Error during conversion: {e}")

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert DOCX files to Markdown.")
    parser.add_argument(
        "-src", "--source",
        required=True,
        type=str,
        help="The path to the DOCX file or directory containing DOCX files."
    )
    parser.add_argument(
        "-dest", "--destination",
        required=True,
        type=str,
        help="The directory where the Markdown files and media will be saved."
    )
    parser.add_argument(
        "-workers", "--max-workers",
        type=int,
        default=4,
        help="Maximum number of worker threads for parallel conversion. Defaults to 4."
    )
    return parser.parse_args()

def main():
    """
    Main function to orchestrate DOCX to Markdown conversion based on the provided arguments.
    """
    args = parse_arguments()

    try:
        if os.path.isfile(args.source):
            if not os.path.isdir(args.destination):
                raise ValueError(f"The specified destination is not a directory: {args.destination}")
            convert_docx_to_md(args.source, args.destination)
        elif os.path.isdir(args.source):
            scan_and_convert(args.source, args.destination, max_workers=args.max_workers)
        else:
            raise ValueError(f"The specified source path is not valid: {args.source}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
