from __future__ import annotations

import math
import xml.etree.ElementTree as ET


def _as_float(value: str | None, default: float = 0.0) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def _extract_nodes(root: ET.Element):
    model = root.find(".//mxGraphModel")
    if model is None:
        return [], 1400.0, 1200.0

    page_width = _as_float(model.get("pageWidth"), 1400.0)
    page_height = _as_float(model.get("pageHeight"), 1200.0)

    nodes = []
    for cell in root.findall(".//mxCell"):
        if cell.get("vertex") != "1":
            continue
        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue

        nodes.append(
            {
                "id": cell.get("id", ""),
                "cell": cell,
                "geometry": geometry,
                "x": _as_float(geometry.get("x")),
                "y": _as_float(geometry.get("y")),
                "w": _as_float(geometry.get("width")),
                "h": _as_float(geometry.get("height")),
            }
        )

    return nodes, page_width, page_height


def _is_overlap(a: dict, b: dict) -> bool:
    return not (
        a["x"] + a["w"] <= b["x"]
        or b["x"] + b["w"] <= a["x"]
        or a["y"] + a["h"] <= b["y"]
        or b["y"] + b["h"] <= a["y"]
    )


def _box_distance(a: dict, b: dict) -> float:
    dx = max(a["x"] - (b["x"] + b["w"]), b["x"] - (a["x"] + a["w"]), 0)
    dy = max(a["y"] - (b["y"] + b["h"]), b["y"] - (a["y"] + a["h"]), 0)
    return math.sqrt(dx * dx + dy * dy)


def analyze_layout(xml_text: str, min_spacing: float = 20.0):
    root = ET.fromstring(xml_text)
    nodes, page_width, page_height = _extract_nodes(root)

    overlaps = []
    spacing_violations = []
    out_of_bounds = []

    for i in range(len(nodes)):
        a = nodes[i]
        if (
            a["x"] < 0
            or a["y"] < 0
            or a["x"] + a["w"] > page_width
            or a["y"] + a["h"] > page_height
        ):
            out_of_bounds.append(a["id"])

        for j in range(i + 1, len(nodes)):
            b = nodes[j]
            if _is_overlap(a, b):
                overlaps.append((a["id"], b["id"]))
                continue

            distance = _box_distance(a, b)
            if distance < min_spacing:
                spacing_violations.append((a["id"], b["id"], round(distance, 2)))

    return {
        "canvas": {"width": page_width, "height": page_height},
        "overlaps": overlaps,
        "out_of_bounds": out_of_bounds,
        "spacing_violations": spacing_violations,
    }


def _move_node(node: dict, new_x: float, new_y: float):
    node["x"] = new_x
    node["y"] = new_y
    node["geometry"].set("x", str(int(round(new_x))))
    node["geometry"].set("y", str(int(round(new_y))))


def auto_fix_layout(
    xml_text: str,
    min_spacing: float = 20.0,
    max_iterations: int = 2,
):
    root = ET.fromstring(xml_text)
    nodes, page_width, page_height = _extract_nodes(root)

    iterations = 0
    while iterations < max_iterations:
        iterations += 1
        changed = False

        for node in nodes:
            max_x = max(0.0, page_width - node["w"])
            max_y = max(0.0, page_height - node["h"])
            clamped_x = min(max(node["x"], 0.0), max_x)
            clamped_y = min(max(node["y"], 0.0), max_y)
            if clamped_x != node["x"] or clamped_y != node["y"]:
                _move_node(node, clamped_x, clamped_y)
                changed = True

        for i in range(len(nodes)):
            a = nodes[i]
            for j in range(i + 1, len(nodes)):
                b = nodes[j]
                if _is_overlap(a, b) or _box_distance(a, b) < min_spacing:
                    new_x = a["x"] + a["w"] + min_spacing
                    new_y = b["y"]
                    if new_x + b["w"] > page_width:
                        new_x = 0.0
                        new_y = min(page_height - b["h"], a["y"] + a["h"] + min_spacing)
                    _move_node(b, new_x, new_y)
                    changed = True

        report = analyze_layout(
            ET.tostring(root, encoding="unicode"), min_spacing=min_spacing
        )
        total_issues = (
            len(report["overlaps"])
            + len(report["out_of_bounds"])
            + len(report["spacing_violations"])
        )
        if total_issues == 0 or not changed:
            break

    final_xml = ET.tostring(root, encoding="unicode")
    final_report = analyze_layout(final_xml, min_spacing=min_spacing)
    return final_xml, {
        "iterations": iterations,
        "issues": final_report,
    }
