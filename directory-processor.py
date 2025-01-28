import os
import sys
import argparse
import re
import tiktoken
import json
import logging
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict, Tuple
import nbconvert


def setup_logging(log_file: str, enable_logging: bool = True):
    if enable_logging:
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filemode="w",
        )
    else:
        logging.basicConfig(level=logging.ERROR, handlers=[logging.NullHandler()])


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def should_include_file(file_path: str, file_size: int, params: Dict) -> bool:
    ext = os.path.splitext(file_path)[1].lower()

    if ext in params["exclude_extensions"]:
        logging.debug(f"Excluded file due to extension: {file_path}")
        return False

    if ext == ".json" and file_size > params["json_size_threshold"]:
        logging.debug(f"Excluded JSON file due to size: {file_path}")
        return False

    if file_size > params["max_file_size"]:
        logging.debug(f"Excluded file due to size: {file_path}")
        return False

    return True


def should_ignore_path(path: str, ignore_patterns: List[str]) -> bool:
    """
    Check if a path should be ignored based on the ignore patterns.
    Patterns are treated as directory or file names to match exactly.
    """
    path_parts = Path(path).parts
    return any(pattern in path_parts for pattern in ignore_patterns)


def convert_notebook_to_markdown(notebook_path: str) -> str:
    logging.info(f"Converting notebook to markdown: {notebook_path}")
    markdown_exporter = nbconvert.MarkdownExporter()
    body, _ = markdown_exporter.from_filename(notebook_path)

    md_path = notebook_path.rsplit(".", 1)[0] + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(body)

    logging.info(f"Notebook converted: {md_path}")
    return md_path


def process_directory(
    path: str,
    current_depth: int,
    params: Dict,
    output_file,
    excluded_files: List[Tuple[str, int]],
) -> None:
    if current_depth > params["max_depth"]:
        logging.debug(f"Max depth reached: {path}")
        return

    # Check if the current directory should be ignored
    if should_ignore_path(path, params["ignore_patterns"]):
        logging.debug(f"Ignored directory due to pattern: {path}")
        output_file.write(
            f"{'  ' * current_depth}[Directory ignored: {os.path.basename(path)}]\n"
        )
        return

    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        logging.error(f"Permission denied accessing directory: {path}")
        output_file.write(
            f"{'  ' * current_depth}[Permission denied accessing directory]\n"
        )
        return
    except Exception as e:
        logging.error(f"Error accessing directory {path}: {str(e)}")
        output_file.write(f"{'  ' * current_depth}[Error accessing directory]\n")
        return

    for item in items:
        item_path = os.path.join(path, item)

        # Check if the item should be ignored
        if should_ignore_path(item_path, params["ignore_patterns"]):
            logging.debug(f"Ignored item due to pattern: {item_path}")
            output_file.write(f"{'  ' * current_depth}├── {item} [Ignored]\n")
            continue

        if os.path.isdir(item_path):
            output_file.write(f"{'  ' * current_depth}└── {item}/\n")
            process_directory(
                item_path, current_depth + 1, params, output_file, excluded_files
            )
        else:
            try:
                file_size = os.path.getsize(item_path)
            except OSError:
                logging.error(f"Cannot access file: {item_path}")
                output_file.write(f"{'  ' * current_depth}├── {item} [Access Error]\n")
                continue

            if item.endswith(".ipynb"):
                try:
                    md_path = convert_notebook_to_markdown(item_path)
                    item_path = md_path
                    item = os.path.basename(md_path)
                    file_size = os.path.getsize(md_path)
                except Exception as e:
                    logging.error(f"Error converting notebook {item_path}: {str(e)}")
                    output_file.write(
                        f"{'  ' * current_depth}├── {item} [Notebook Conversion Error]\n"
                    )
                    continue

            if should_include_file(item_path, file_size, params):
                output_file.write(f"{'  ' * current_depth}├── {item}\n")

                try:
                    with open(item_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if count_tokens(content) <= params["token_limit"]:
                        output_file.write(f"{'  ' * (current_depth + 1)}Content:\n")
                        output_file.write(f"{content}\n\n")
                    else:
                        output_file.write(
                            f"{'  ' * (current_depth + 1)}[Content excluded due to token limit]\n\n"
                        )
                        logging.info(
                            f"Content excluded due to token limit: {item_path}"
                        )
                except Exception as e:
                    logging.error(f"Error processing file {item_path}: {str(e)}")
                    output_file.write(
                        f"{'  ' * (current_depth + 1)}[Error processing file]\n\n"
                    )
            else:
                output_file.write(f"{'  ' * current_depth}├── {item} [Excluded]\n")
                excluded_files.append((item_path, file_size))


def main():
    parser = argparse.ArgumentParser(
        description="Process a local directory and create a structured output"
    )
    parser.add_argument(
        "--enable-logging",
        action="store_true",
        default=False,
        help="Enable logging to file",
    )
    parser.add_argument("directory_path", help="Path to the directory to process")
    parser.add_argument(
        "--token-limit",
        type=int,
        default=10_000,
        help="Token limit for non-code text files",
    )
    parser.add_argument(
        "--json-size-threshold",
        type=int,
        default=1024 * 1024,
        help="Size threshold for JSON files (in bytes)",
    )
    parser.add_argument(
        "--exclude-extensions",
        nargs="+",
        default=[".csv", ".pt", ".pkl", ".bin", ".h5", ".parquet", ".gitignore"],
        help="File extensions to exclude",
    )
    parser.add_argument(
        "--ignore-patterns",
        nargs="+",
        default=[
            ".env",
            ".git",
            ".history",
            ".idea",
            ".jest",
            ".pytest_cache",
            ".venv",
            ".vscode",
            "__pycache__",
            "assets",
            "bin",
            "bower_components",
            "build",
            "coverage",
            "dist",
            "document",
            "generated",
            "graphics",
            "images",
            "media",
            "migrations",
            "misc_docs",
            "node_modules",
            "obj",
            "out",
            "packages",
            "public",
            "static",
            "staticfiles",
            "tabs",
            "target",
            "test-results",
            "tests",
            "vendor",
            "venv",
        ],
        help="Directories or file patterns to ignore",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum depth for directory tree processing",
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=10 * 1024 * 1024,
        help="Maximum file size to include (in bytes)",
    )
    parser.add_argument("--output", default="codebase.txt", help="Output file name")
    parser.add_argument(
        "--split-threshold",
        type=int,
        default=1000000,
        help="Token threshold for splitting output files",
    )
    parser.add_argument(
        "--log-file", default="directory_processing.log", help="Log file name"
    )

    args = parser.parse_args()

    setup_logging(args.log_file, args.enable_logging)
    logging.info("Starting directory processing")

    if not os.path.exists(args.directory_path):
        logging.error(f"Directory does not exist: {args.directory_path}")
        print(f"Error: Directory does not exist: {args.directory_path}")
        sys.exit(1)

    if not os.path.isdir(args.directory_path):
        logging.error(f"Path is not a directory: {args.directory_path}")
        print(f"Error: Path is not a directory: {args.directory_path}")
        sys.exit(1)

    params = vars(args)
    excluded_files = []
    output_files = []

    output_file = open(args.output, "w", encoding="utf-8")
    output_files.append(output_file.name)

    logging.info("Processing directory structure")
    process_directory(args.directory_path, 0, params, output_file, excluded_files)

    logging.info("Listing excluded files")
    for file_path, size in excluded_files:
        logging.info(f"Excluded: {file_path} - {size} bytes")

    output_file.close()

    logging.info("Estimating total token count")
    total_tokens = 0
    for file_name in output_files:
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()
            file_tokens = count_tokens(content)
            total_tokens += file_tokens
            logging.info(f"{file_name}: {file_tokens} tokens")

    logging.info(f"Total tokens: {total_tokens}")

    if total_tokens > args.split_threshold:
        logging.info("Output exceeds split threshold. Splitting into multiple files.")
        split_files = []
        current_tokens = 0
        current_content = ""
        part = 1

        for file_name in output_files:
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
                content_tokens = count_tokens(content)

                if current_tokens + content_tokens > args.split_threshold:
                    split_file_name = f"{args.output}.split{part}"
                    with open(split_file_name, "w", encoding="utf-8") as split_f:
                        split_f.write(current_content)
                    split_files.append(split_file_name)
                    logging.info(f"Created split file: {split_file_name}")
                    part += 1
                    current_content = content
                    current_tokens = content_tokens
                else:
                    current_content += content
                    current_tokens += content_tokens

        if current_content:
            split_file_name = f"{args.output}.split{part}"
            with open(split_file_name, "w", encoding="utf-8") as split_f:
                split_f.write(current_content)
            split_files.append(split_file_name)
            logging.info(f"Created final split file: {split_file_name}")

        logging.info(f"Output split into {len(split_files)} files")

    logging.info("Processing complete")


if __name__ == "__main__":
    main()
