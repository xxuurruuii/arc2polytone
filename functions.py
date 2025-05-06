# Author: rainrzk
# Date: 2025-05-06
# License: MIT
# Version: 1.0.3

"""
This script contains functions for main.py.
"""

import math
import re
import tempfile


ARC_COLOR_MAP = {}
ARC_END_KEYS = set()
ARC_START_KEYS = set()
MAP_FORMULA = {
    "x": lambda v: 0.5 + 1.2 * (v - 0.5),
    "y": lambda v: 2.1 * (v - 0.6),
}
TRACE_PAIRS = {}


def get_arc_color(start, x1, y1):
    for raw, (r, g, b) in ARC_COLOR_MAP.items():
        parts, *_ = parse_arc_line(raw)
        if float(parts[1]) == start and float(parts[3]) == x1 and float(parts[6]) == y1:
            return (r, g, b)
    return None


def set_arc_color(raw, color):
    ARC_COLOR_MAP[raw] = color


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()


def parse_arc_line(line):
    m1 = re.match(r"arc\(\s*([^\)]*)\)\[arctap\(\s*(\d+)(?:,([\d.]+))?\s*\)\];", line)
    if m1:
        parts = [x.strip() for x in m1.group(1).split(",")]
        return parts, int(m1.group(2)), float(m1.group(3) or 1), True
    m2 = re.match(r"arc\(\s*([^\)]*)\);", line)
    if m2:
        parts = [x.strip() for x in m2.group(1).split(",")]
        if parts[-1].lower() == "false":
            return parts, int(parts[0]), 1.0, False
    return None, None, None, False


def parse_timing_line(line, out_aff):
    m = re.match(r"\s*timing\(\s*([\d.]+)\s*,\s*([\d.]+)", line)
    if m and m.group(1) != "0":
        out_aff.write(f"timing({m.group(1)},{m.group(2)},4.00);\n")
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)


def build_multimap(path):
    global ARC_START_KEYS, ARC_END_KEYS, TRACE_PAIRS
    ARC_START_KEYS.clear()
    ARC_END_KEYS.clear()
    TRACE_PAIRS.clear()
    lines = [ln.rstrip("\n") for ln in read_lines(path)]
    false_arcs = []
    for raw in lines:
        if not raw.strip().startswith("arc("):
            continue
        arc_parts, *_ = parse_arc_line(raw.strip())
        if not arc_parts:
            continue
        if arc_parts[9].lower() == "false":
            false_arcs.append((raw.strip(), arc_parts))
    for raw, p in false_arcs:
        key_start = (p[0], p[2], p[5])
        key_end = (p[1], p[3], p[6])
        ARC_START_KEYS.add(key_start)
        ARC_END_KEYS.add(key_end)
        trace_start = None
        trace_end = None
        for ln in lines:
            ln_strip = ln.strip()
            if ln_strip == raw:
                continue
            trace_parts, *_ = parse_arc_line(ln_strip)
            if not trace_parts:
                m = re.match(r"arc\(\s*([^\)]*)\);", ln_strip)
                if not m:
                    continue
                trace_parts = [x.strip() for x in m.group(1).split(",")]
            if trace_parts[9].lower() != "true":
                continue
            if (
                trace_parts[0] == p[0]
                and trace_parts[2] == p[2]
                and trace_parts[5] == p[5]
            ):
                trace_start = ln_strip
                break
        for ln in lines:
            ln_strip = ln.strip()
            if ln_strip == raw:
                continue
            trace_parts, *_ = parse_arc_line(ln_strip)
            if not trace_parts:
                m = re.match(r"arc\(\s*([^\)]*)\);", ln_strip)
                if not m:
                    continue
                trace_parts = [x.strip() for x in m.group(1).split(",")]
            if trace_parts[9].lower() != "true":
                continue
            if (
                trace_parts[0] == p[1]
                and trace_parts[2] == p[3]
                and trace_parts[5] == p[6]
            ):
                trace_end = ln_strip
                break
        if trace_start and trace_end:
            TRACE_PAIRS[raw] = (trace_start, trace_end)


def is_there_an_arc_at_start(line: str) -> bool:
    inner = line[line.find("(") + 1 : line.find(")")]
    p = [x.strip() for x in inner.split(",")]
    return (p[0], p[2], p[5]) in ARC_END_KEYS


def is_there_an_arc_at_end(line: str) -> bool:
    inner = line[line.find("(") + 1 : line.find(")")]
    p = [x.strip() for x in inner.split(",")]
    return (p[0], p[2], p[5]) in ARC_START_KEYS


def is_there_a_trace_at_start(line):
    ln = line.strip()
    pair = TRACE_PAIRS.get(ln)
    return pair[0] if pair else False


def is_there_a_trace_at_end(line):
    ln = line.strip()
    pair = TRACE_PAIRS.get(ln)
    return pair[1] if pair else False


def build_fraction_dict(start, end, bpm):
    beat = 60000.0 / bpm
    tol = 2.0
    fracs = {
        "whole": [0, 1],
        "half": [0.5],
        "third": [1 / 3, 2 / 3],
        "quarter": [0.25, 0.75],
        "sixth": [1 / 6, 5 / 6],
    }
    return {
        t: next(
            (
                name
                for name, vs in fracs.items()
                if any(
                    abs((t - start) % beat - v * beat) <= tol
                    or abs((beat - t + start) % beat - v * beat) <= tol
                    for v in vs
                )
            ),
            "other",
        )
        for t in range(int(start), int(end) + 1)
    }


def get_color(key):
    return {
        "whole": (255, 128, 128),
        "half": (128, 128, 255),
        "third": (192, 128, 192),
        "quarter": (255, 255, 128),
        "sixth": (255, 224, 230),
    }.get(key, (0, 255, 0))


def ease_xy(ease, x):
    π = math.pi
    funcs = {
        "b": lambda v: (-(math.cos(v * π) - 1) / 2,) * 2,
        "s": lambda v: (v, v),
        "si": lambda v: (math.sin(π / 2 * v),) * 2,
        "sisi": lambda v: (math.sin(π / 2 * v),) * 2,
        "so": lambda v: (1 - math.cos(π / 2 * v),) * 2,
        "soso": lambda v: (1 - math.cos(π / 2 * v),) * 2,
        "siso": lambda v: (math.sin(π / 2 * v), 1 - math.cos(π / 2 * v)),
        "sosi": lambda v: (1 - math.cos(π / 2 * v), math.sin(π / 2 * v)),
    }
    return funcs.get(ease, lambda v: (v, v))(x)


def map(path):
    lines = read_lines(path)
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".aff")
    temp_path = temp_file.name
    with temp_file:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("arc("):
                m = re.match(r"(arc\()([^)]+)(\).*)", line)
                if m:
                    args, rest = m.group(2), m.group(3)
                    p = [x.strip() for x in args.split(",")]
                    p[2] = f"{MAP_FORMULA['x'](float(p[2])):.2f}"
                    p[3] = f"{MAP_FORMULA['x'](float(p[3])):.2f}"
                    p[5] = f"{MAP_FORMULA['y'](float(p[5])):.2f}"
                    p[6] = f"{MAP_FORMULA['y'](float(p[6])):.2f}"
                    temp_file.write(f"arc({','.join(p)}{rest}\n")
                    continue
            temp_file.write(line)
    return temp_path


def preprocess(path):
    temp_path = map(path)
    build_multimap(temp_path)
    return temp_path
