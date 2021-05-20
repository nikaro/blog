#!/usr/bin/python3

import argparse
from pathlib import Path
import re


def main() -> None:
    args = setup_args()
    contents = Path(args.content).glob("*.md")
    for article in contents:
        content = article.read_text()
        content = format_metadata(content)
        article.write_text(content)


def setup_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("content", help="content directory")
    args = parser.parse_args()
    return args


def format_metadata(content: str) -> str:
    lines = content.splitlines()
    lines_del = []
    # insert opening delimiter
    if not lines[0] == "---":
        lines.insert(0, "---")
    for index, line in enumerate(lines):
        # title
        line = re.sub(r'^Title:(?: (.*))?$', r'title: "\1"', line)
        # slug
        line = re.sub(r'^Slug: (.*)$', r'slug: "\1"', line)
        # date
        line = re.sub(r'^Date: (\d{4}-\d{2}-\d{2})(?: (?:.*))?$', r'date: "\1"', line)
        # author
        if re.match(r'^Author: (.*)$', line):
            lines_del.append(index)
        # categories
        line = re.sub(r'^Category: (.*)$', r'categories: ["\1"]', line)
        # tags
        if match := re.match(r'^Tags:(?: (.*))?$', line):
            groups = match.groups()[0]
            tags = sorted(list(map(str.strip, groups.split(",")))) if groups else []
            tags = str(tags).replace("'", '"')
            line = f"tags: {tags}"
        # drafts
        if match := re.match(r'^Status: (.*)$', line):
            print(match.group(1))
            if match.group(1) == "published":
                lines_del.append(index)
            else:
                line = "draft: true"
        # replace line
        lines[index] = line
        # insert closing delimiter
        if not line:
            if lines[index - 1] != "---":
                lines.insert(index, "---")
            break
    # ensure there is a new lin at the end of file
    lines[-1] += "\n"
    # delete items
    list(map(lines.pop, lines_del))
    # re-join lines together
    content = "\n".join(lines)
    return content


if __name__ == "__main__":
    main()
