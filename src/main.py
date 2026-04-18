import os
import shutil
import sys

from gencontent import generate_pages_recursive


def copy_static_to_destination(static_dir, destination_dir):
	if os.path.exists(destination_dir):
		shutil.rmtree(destination_dir)

	if os.path.exists(static_dir):
		shutil.copytree(static_dir, destination_dir)
		return

	os.makedirs(destination_dir, exist_ok=True)


def main():
	basepath = "/"
	if len(sys.argv) > 1:
		basepath = sys.argv[1]

	copy_static_to_destination("static", "docs")
	generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
	main()
