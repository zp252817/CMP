#!/usr/bin/env python3
"""Convert an .xmind file to a structured Markdown outline."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert XMind file to Markdown.")
    parser.add_argument("--input", required=True, help="Path to .xmind file")
    parser.add_argument("--output", required=True, help="Path to output .md file")
    return parser.parse_args()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def topic_children(topic: dict[str, Any]) -> list[dict[str, Any]]:
    children = topic.get("children") or {}
    result: list[dict[str, Any]] = []
    result.extend(children.get("attached") or [])
    result.extend(children.get("detached") or [])
    return result


def pick_sheet(payload: list[dict[str, Any]], metadata: dict[str, Any]) -> dict[str, Any]:
    if not payload:
        raise RuntimeError("content.json is empty")
    active_id = metadata.get("activeSheetId")
    if active_id:
        for item in payload:
            if item.get("id") == active_id:
                return item
    return payload[0]


def topic_title(topic: dict[str, Any], fallback: str = "未命名主题") -> str:
    title = normalize_text(str(topic.get("title", "")))
    return title or fallback


def topic_note(topic: dict[str, Any]) -> str:
    note = topic.get("notes")
    if not isinstance(note, dict):
        return ""
    plain = note.get("plain")
    if not isinstance(plain, dict):
        return ""
    return normalize_text(str(plain.get("content", "")))


def render_bullets(topic: dict[str, Any], depth: int = 0) -> list[str]:
    lines: list[str] = []
    for child in topic_children(topic):
        indent = "  " * depth
        lines.append(f"{indent}- {topic_title(child)}")
        note = topic_note(child)
        if note:
            lines.append(f"{indent}  - 备注: {note}")
        lines.extend(render_bullets(child, depth + 1))
    return lines


def build_markdown(sheet: dict[str, Any]) -> str:
    root = sheet.get("rootTopic") or {}
    root_title = topic_title(root, fallback=topic_title(sheet, fallback="XMind 导出"))
    lines: list[str] = [f"# {root_title}", "", f"来源工作表: {topic_title(sheet)}", ""]

    top_topics = topic_children(root)
    if not top_topics:
        lines.append("- 无子主题")
        return "\n".join(lines).strip() + "\n"

    for item in top_topics:
        lines.append(f"## {topic_title(item)}")
        note = topic_note(item)
        if note:
            lines.append("")
            lines.append(f"> 备注: {note}")
        children = render_bullets(item, depth=0)
        if children:
            lines.append("")
            lines.extend(children)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def read_xmind(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        if "content.json" not in names:
            raise RuntimeError("Unsupported xmind: content.json not found")
        payload = json.loads(zf.read("content.json").decode("utf-8"))
        metadata: dict[str, Any] = {}
        if "metadata.json" in names:
            metadata = json.loads(zf.read("metadata.json").decode("utf-8"))
    if not isinstance(payload, list):
        raise RuntimeError("Invalid content.json format")
    return payload, metadata


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    if input_path.suffix.lower() != ".xmind":
        raise RuntimeError("Input file is not .xmind")

    payload, metadata = read_xmind(input_path)
    sheet = pick_sheet(payload, metadata)
    markdown = build_markdown(sheet)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

