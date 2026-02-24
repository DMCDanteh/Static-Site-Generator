import os
from pathlib import Path
from inline_markdown import markdown_to_html_node
from htmlnode import LeafNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped_line = line.lstrip("#").strip(" ")
            return stripped_line
    raise Exception("no header detected")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    markdown_node = markdown_to_html_node(markdown_content)
    markdown_string = markdown_node.to_html()
    markdown_title = extract_title(markdown_content)
    result = template_content.replace("{{ Title }}", markdown_title).replace("{{ Content }}", markdown_string)
    result = result.replace('href="/', f'href="{basepath}')
    result = result.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(path=dir_path_content):
        full_path_filename = os.path.join(dir_path_content, filename)
        dest_full_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(full_path_filename):
            correct_dest = Path(dest_full_path).with_suffix(".html")
            generate_page(full_path_filename, template_path, correct_dest, basepath)
        else:
            generate_pages_recursive(full_path_filename, template_path, dest_full_path, basepath)