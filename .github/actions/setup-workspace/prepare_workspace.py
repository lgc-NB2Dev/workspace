# /// script
# requires-python = ">=3.10"
# dependencies = ["tomlkit>=0.13"]
# ///
# ruff: noqa: INP001
"""Trim a checked-out workspace to the plugin being tested in CI."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, cast

import tomlkit


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def requirement_name(requirement: str) -> str:
    match = re.match(r"[A-Za-z0-9_.-]+", requirement)
    if match is None:
        raise ValueError(f"Invalid dependency specification: {requirement}")
    return re.sub(r"[_.]", "-", match.group()).casefold()


def select_dependencies(
    dependencies: list[str],
    plugin_name: str,
    plugin_dependencies: list[str],
    plugin_extras: str,
) -> list[str]:
    try:
        workspace_dependency_index = dependencies.index("cookit[all]")
    except ValueError as error:
        raise ValueError("Expected cookit[all] workspace dependency marker") from error

    declared_names = {
        requirement_name(dependency)
        for dependency in [plugin_name, *plugin_dependencies]
    }
    selected = [
        dependency
        for dependency in dependencies[workspace_dependency_index:]
        if requirement_name(dependency) in declared_names
    ]
    if requirement_name(plugin_name) not in map(requirement_name, selected):
        selected.append(plugin_name)
    if plugin_extras:
        plugin_requirement = f"{plugin_name}[{plugin_extras}]"
        selected = [
            plugin_requirement
            if requirement_name(dependency) == requirement_name(plugin_name)
            else dependency
            for dependency in selected
        ]
    return unique([*dependencies[:workspace_dependency_index], *selected])


def make_array(values: list[str]) -> Any:
    array = tomlkit.array().multiline(multiline=True)
    for value in values:
        array.append(value)
    return array


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--submodule-path", type=Path, required=True)
    parser.add_argument("--plugin-extras", default="")
    parser.add_argument("--extra-dev-dependencies", default="")
    args = parser.parse_args()

    plugin_directory = args.workspace / args.submodule_path

    pyproject_path = args.workspace / "pyproject.toml"
    pyproject: Any = tomlkit.parse(pyproject_path.read_text(encoding="utf-8"))
    dependencies = list(cast("list[str]", pyproject["dependency-groups"]["dev"]))

    plugin_project: Any = tomlkit.parse(
        (plugin_directory / "pyproject.toml").read_text(encoding="utf-8")
    )
    plugin_name = cast("str", plugin_project["project"]["name"])
    extra_dependencies = [
        dependency.strip()
        for dependency in args.extra_dev_dependencies.splitlines()
        if dependency.strip()
    ]
    dependencies = unique(
        [
            *select_dependencies(
                dependencies,
                plugin_name,
                cast("list[str]", plugin_project["project"].get("dependencies", [])),
                ",".join(
                    extra.strip()
                    for extra in args.plugin_extras.split(",")
                    if extra.strip()
                ),
            ),
            *extra_dependencies,
        ]
    )

    pyproject["dependency-groups"]["dev"] = make_array(dependencies)
    pyproject["tool"]["uv"]["workspace"]["members"] = make_array(
        [args.submodule_path.as_posix()]
    )
    sources: Any = tomlkit.table()
    source: Any = tomlkit.inline_table()
    source["workspace"] = True
    sources[plugin_name] = source
    pyproject["tool"]["uv"]["sources"] = sources
    pyproject_path.write_text(tomlkit.dumps(pyproject), encoding="utf-8")


if __name__ == "__main__":
    main()
