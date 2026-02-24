from textnode import TextType, TextNode, text_node_to_html_node
from enum import Enum
from htmlnode import ParentNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
        else:
            split_string = node.text.split(delimiter)
            if len(split_string) % 2 == 0:
                raise Exception("invalid markdown")
            else:
                for index, string in enumerate(split_string):
                    if string:
                        if index % 2 == 0:
                            new_node = TextNode(string, TextType.TEXT)
                            results.append(new_node)
                        else:
                            new_node = TextNode(string, text_type)
                            results.append(new_node)
    return results

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                results.append(node)
            else:
                original_text = node.text
                for image in images:
                    image_text = image[0]
                    image_url = image[1]
                    image_markdown = f"![{image_text}]({image_url})"
                    sections = original_text.split(image_markdown, 1)
                    if len(sections) != 2:
                        raise Exception("wrong markdown")
                    if sections[0] != "":
                        new_node = TextNode(sections[0], TextType.TEXT)
                        results.append(new_node)
                    image_node = TextNode(image_text, TextType.IMAGE, image_url)
                    results.append(image_node)
                    original_text = sections[1]
                if original_text != "":
                    remaining_text = TextNode(original_text, TextType.TEXT)
                    results.append(remaining_text)
    return results



def split_nodes_link(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                results.append(node)
            else:
                original_text = node.text
                for link in links:
                    link_text = link[0]
                    link_url = link[1]
                    link_markdown = f"[{link_text}]({link_url})"
                    sections = original_text.split(link_markdown, 1)
                    if len(sections) != 2:
                        raise Exception("wrong markdown")
                    if sections[0] != "":
                        new_node = TextNode(sections[0], TextType.TEXT)
                        results.append(new_node)
                    link_node = TextNode(link_text, TextType.LINK, link_url)
                    results.append(link_node)
                    original_text = sections[1]
                if original_text != "":
                    remaining_text = TextNode(original_text, TextType.TEXT)
                    results.append(remaining_text)
    return results

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    results = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        if block == "":
            continue
        stripped_block = block.strip("\n")
        results.append(stripped_block)
    return results

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    list_of_nodes = text_to_textnodes(text)
    result = []
    for node in list_of_nodes:
        html_node = text_node_to_html_node(node)
        result.append(html_node)
    return result

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unorderedlist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return orderedlist_to_html_node(block)

def paragraph_to_html_node(block):
    split_block = block.split("\n")
    rejoined_block = " ".join(split_block)
    children = text_to_children(rejoined_block)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level +=1
        else:
            break
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    result = []
    for line in lines:
        stripped_line = line.lstrip("> ")
        result.append(stripped_line)
    text = " ".join(result)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    return ParentNode("pre", [code_node])

def unorderedlist_to_html_node(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        stripped_line = line[2:]
        loop_children = text_to_children(stripped_line)
        li_node = ParentNode("li", loop_children)
        children.append(li_node)
    return ParentNode("ul", children)

def orderedlist_to_html_node(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        split_line = line.split(". ", 1)
        stripped_line = split_line[1]
        loop_children = text_to_children(stripped_line)
        li_node = ParentNode("li", loop_children)
        children.append(li_node)
    return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)