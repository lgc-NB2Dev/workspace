import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
REFERENCE_DIR = ROOT_DIR / "private" / "references" / "nonebot2"
WEBSITE_DIR = REFERENCE_DIR / "website"
SOURCE_DOCS_DIR = WEBSITE_DIR / "docs"
OUTPUT_FILE = ROOT_DIR / "docs" / "nonebot2-docs-index.md"


@dataclass
class DocContext:
    version: str
    commit: str
    docs_dir: Path
    sidebar_file: Path
    docs_rel_dir: Path


@dataclass
class DocInfo:
    title: str
    path: Path
    rel_path: str
    description: str | None = None


def run(command: list[str], cwd: Path = ROOT_DIR) -> str:
    result = subprocess.run(  # noqa: S603
        command,
        check=True,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def installed_nonebot_version() -> str:
    output = run(["uv", "pip", "show", "nonebot2"])
    for line in output.splitlines():
        if line.startswith("Version:"):
            return line.split(":", 1)[1].strip()
    msg = "Could not find NoneBot2 version in `uv pip show nonebot2` output."
    raise RuntimeError(msg)


def git_output(args: list[str]) -> str:
    return run(["git", "-C", str(REFERENCE_DIR), *args])


def validate_reference() -> str:
    if not REFERENCE_DIR.exists():
        msg = (
            f"Missing {REFERENCE_DIR.relative_to(ROOT_DIR)}. "
            "Clone https://github.com/nonebot/nonebot2 with --depth=1 first."
        )
        raise RuntimeError(msg)

    return git_output(["rev-parse", "--short", "HEAD"])


def build_context() -> DocContext:
    version = installed_nonebot_version()
    commit = validate_reference()

    docs_dir = WEBSITE_DIR / "versioned_docs" / f"version-{version}"
    if not docs_dir.exists():
        msg = f"Missing versioned docs for installed NoneBot2 {version}: {docs_dir.relative_to(ROOT_DIR)}"
        raise RuntimeError(msg)

    sidebar_file = (
        WEBSITE_DIR / "versioned_sidebars" / f"version-{version}-sidebars.json"
    )
    if not sidebar_file.exists():
        msg = f"Missing sidebar file: {sidebar_file.relative_to(ROOT_DIR)}"
        raise RuntimeError(msg)

    return DocContext(
        version=version,
        commit=commit,
        docs_dir=docs_dir,
        sidebar_file=sidebar_file,
        docs_rel_dir=docs_dir.relative_to(ROOT_DIR),
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    raw = text[4:end]
    body = text[end + 4 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, body


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def category_data(directory: Path) -> dict[str, Any]:
    path = directory / "_category_.json"
    if not path.exists():
        return {}

    data = read_json(path)
    return data if isinstance(data, dict) else {}


def doc_info(path: Path, docs_dir: Path) -> DocInfo:
    frontmatter, body = parse_frontmatter(path.read_text("utf-8"))
    title = frontmatter.get("title") or first_heading(body) or path.stem
    description = frontmatter.get("description")
    rel_path = path.relative_to(docs_dir).as_posix()
    return DocInfo(title=title, description=description, path=path, rel_path=rel_path)


def doc_path_from_id(doc_id: str, docs_dir: Path) -> Path | None:
    candidates = [
        docs_dir / f"{doc_id}.md",
        docs_dir / f"{doc_id}.mdx",
        docs_dir / doc_id / "README.md",
        docs_dir / doc_id / "README.mdx",
    ]
    return next((path for path in candidates if path.exists()), None)


def doc_sort_key(path: Path) -> tuple[int, str]:
    frontmatter, _ = parse_frontmatter(path.read_text("utf-8"))
    raw_pos = frontmatter.get("sidebar_position")
    try:
        position = int(raw_pos) if raw_pos is not None else 1000
    except ValueError:
        position = 1000
    return position, path.stem


def directory_sort_key(path: Path) -> tuple[int, str]:
    data = category_data(path)
    raw_pos = data.get("position")
    try:
        position = int(raw_pos) if raw_pos is not None else 1000
    except (TypeError, ValueError):
        position = 1000
    return position, path.name


def collect_docs(directory: Path) -> list[Path]:
    docs = [
        path
        for pattern in ("*.md", "*.mdx")
        for path in directory.glob(pattern)
        if path.name != "_category_.json"
    ]
    readme = [path for path in docs if path.stem == "README"]
    others = [path for path in docs if path.stem != "README"]
    return sorted(readme, key=doc_sort_key) + sorted(others, key=doc_sort_key)


def render_doc_line(info: DocInfo, indent: int = 0) -> str:
    prefix = "  " * indent
    suffix = f" - {info.description}" if info.description else ""
    return f"{prefix}- `{info.rel_path}`: {info.title}{suffix}"


def render_directory(directory: Path, docs_dir: Path, indent: int = 0) -> list[str]:
    if not directory.exists():
        return []

    lines = [
        render_doc_line(doc_info(path, docs_dir), indent)
        for path in collect_docs(directory)
    ]
    subdirs = sorted(
        [path for path in directory.iterdir() if path.is_dir()],
        key=directory_sort_key,
    )

    for subdir in subdirs:
        data = category_data(subdir)
        label = data.get("label") or subdir.name
        rel_path = subdir.relative_to(docs_dir).as_posix()
        lines.append(f"{'  ' * indent}- {label} (`{rel_path}/`)")
        lines.extend(render_directory(subdir, docs_dir, indent + 1))

    return lines


def render_sidebar_item(item: Any, docs_dir: Path, indent: int = 0) -> list[str]:
    if isinstance(item, str):
        path = doc_path_from_id(item, docs_dir)
        return [render_doc_line(doc_info(path, docs_dir), indent)] if path else []

    if not isinstance(item, dict):
        return []

    item_type = item.get("type")
    if item_type == "autogenerated":
        return render_directory(docs_dir / item["dirName"], docs_dir, indent)

    if item_type == "category":
        lines = [f"{'  ' * indent}- {item['label']}"]
        for child in item.get("items", []):
            lines.extend(render_sidebar_item(child, docs_dir, indent + 1))
        return lines

    if item_type == "link":
        target = item.get("href") or item.get("to")
        return [f"{'  ' * indent}- {item.get('label', target)}: {target}"]

    if item_type == "doc":
        path = doc_path_from_id(item["id"], docs_dir)
        return [render_doc_line(doc_info(path, docs_dir), indent)] if path else []

    return []


def render_nav_summary() -> list[str]:
    return [
        "## Navbar",
        "",
        "- 指南: `tutorial` docs menu.",
        "- 深入: `appendices` docs menu.",
        "- 进阶: `advanced` docs menu.",
        "- API: `api/index`.",
        "- 更多: links to 最佳实践, 开发者, 社区, 开源之夏, 商店, 更新日志, 论坛.",
        "",
    ]


def sidebar_title(name: str) -> str:
    title = name.replace("-", " ").replace("_", " ").title()
    return title.upper() if len(name) <= 4 else title


def render_sidebar_section(
    item: Any,
    sidebar_name: str,
    docs_dir: Path,
) -> list[str]:
    if isinstance(item, dict) and item.get("type") == "category":
        title = item["label"]
        content: list[str] = []
        for child in item.get("items", []):
            content.extend(render_sidebar_item(child, docs_dir))
    else:
        title = sidebar_title(sidebar_name)
        content = render_sidebar_item(item, docs_dir)

    lines = [f"### {title}", ""]
    lines.extend(content)
    lines.append("")
    return lines


def render_sidebars(sidebars: dict[str, list[Any]], docs_dir: Path) -> list[str]:
    lines = ["## Sidebar", ""]
    for sidebar_name, items in sidebars.items():
        for item in items:
            lines.extend(render_sidebar_section(item, sidebar_name, docs_dir))
    return lines


def main() -> None:
    context = build_context()
    sidebars = read_json(context.sidebar_file)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# NoneBot2 Docs Index",
        "",
        f"Generated from local clone `{REFERENCE_DIR.relative_to(ROOT_DIR).as_posix()}`.",
        "",
        f"- Installed NoneBot2 version: `{context.version}`.",
        f"- Reference commit: `{context.commit}`.",
        f"- Docs root used: `{context.docs_dir.relative_to(REFERENCE_DIR).as_posix()}`.",
        f"- Source docs root: `{SOURCE_DOCS_DIR.relative_to(REFERENCE_DIR).as_posix()}`.",
        f"- Sidebar source: `{context.sidebar_file.relative_to(REFERENCE_DIR).as_posix()}`.",
        "- Regenerate after the local reference repo or installed NoneBot2 version changes: `poe docs-index`.",
        "",
    ]
    lines.extend(render_nav_summary())
    lines.extend(render_sidebars(sidebars, context.docs_dir))

    OUTPUT_FILE.write_text("\n".join(lines).rstrip() + "\n", "utf-8")
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
