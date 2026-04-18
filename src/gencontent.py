import os


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isdir(from_path):
            generate_pages_recursive(
                from_path,
                template_path,
                os.path.join(dest_dir_path, filename),
                basepath,
            )
            continue

        if not filename.endswith(".md"):
            continue

        if filename == "index.md":
            dest_path = os.path.join(dest_dir_path, "index.html")
        else:
            page_name = os.path.splitext(filename)[0]
            dest_path = os.path.join(dest_dir_path, page_name, "index.html")

        generate_page(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    # Lazy import keeps extract_title tests independent from markdown parser modules.
    from markdown_blocks import markdown_to_html_node

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as to_file:
        to_file.write(template)


def extract_title(md):
    lines = md.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found")
