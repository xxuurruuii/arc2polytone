# Author: rainrzk
# Date: 2025-05-06
# License: MIT
# Version: 1.0.3

"""
This script mainly supports arctap2square:
- Arctap's width controls square's size
- Red arctap represents flick
- Trace's length controls square's rotation
- Trace at arc's start and end can set hold's rotation
- Input aff file (-0.5 <= x <= 1.5, 0.0 <= y <= 1.0) is recommended
"""

import cmath
import functions
import math
import re
import os


AUDIO_OFFSET = 0
BASE_BPM = 170
DEFAULT_NOTE_SIZE = 0.75
HOLD_DENSITY = 12
INPUT_AFF = "2.aff"
OUTPUT_AFF = "3.aff"
TURN_ON_ARC2HOLD = True
TURN_ON_COLOR_INSIDE = True
TURN_ON_FLICK = True


def process(input_path, output_path):
    def process_arctap(p, t, bpm, frac, out_aff, out_lua, tg, raw, scale):
        if functions.is_there_an_arc_at_start(raw) or functions.is_there_an_arc_at_end(
            raw
        ):
            return tg
        start, end = float(p[0]), float(p[1])
        x, y = float(p[2]), float(p[5])
        key = frac.get(t, "other")
        r, g, b = functions.get_color(key)
        base = end - start - 1
        size = DEFAULT_NOTE_SIZE * scale
        for i in range(4):
            ang = base + i * 90
            dx = size * cmath.sin(math.radians(ang)) / 4
            dy = 0.96 * size * cmath.cos(math.radians(ang)) / 2
            nx, ny = (x + dx).real, (y + dy).real
            out_aff.write(
                f"timinggroup(noinput){{\n"
                f"  timing(0,{bpm:.2f},4.00);\n"
                f"  scenecontrol({t},hidegroup,0.00,1);\n"
                f"  arc({t},{t+1},{nx:.2f},{nx:.2f},s,{ny:.2f},{ny:.2f},0,none,true)[arctap({t})];\n"
                f"}};\n"
            )
            out_lua.write(
                f"local tg{tg}=Scene.getNoteGroup({tg})\n"
                f"tg{tg}.rotationIndividualZ=Channel.keyframe().addKey(0,{ang})\n"
                f"tg{tg}.scaleIndividualX=Channel.keyframe().addKey(0,{0.9*size:.2f})\n"
                f"tg{tg}.scaleIndividualY=Channel.keyframe().addKey(0,{0.6*size:.2f})\n"
                f"tg{tg}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                f"tg{tg}.colorR={r}\n"
                f"tg{tg}.colorG={g}\n"
                f"tg{tg}.colorB={b}\n\n"
            )
            tg += 1
        if TURN_ON_COLOR_INSIDE:
            dx = 0.39 * size * cmath.sin(math.radians(base))
            dy = 0.74 * size * cmath.cos(math.radians(base))
            mx, my = (x + dx).real, (y + dy).real
            out_aff.write(
                f"timinggroup(noinput){{\n"
                f"  timing(0,{bpm:.2f},4.00);\n"
                f"  scenecontrol({t},hidegroup,0.00,1);\n"
                f"  arc({t},{t+1},{mx:.2f},{mx:.2f},s,{my:.2f},{my:.2f},0,none,true)[arctap({t})];\n"
                f"}};\n"
            )
            out_lua.write(
                f"local tg{tg}=Scene.getNoteGroup({tg})\n"
                f"tg{tg}.rotationIndividualZ=Channel.keyframe().addKey(0,{base})\n"
                f"tg{tg}.scaleIndividualX=Channel.keyframe().addKey(0,{0.9*size:.2f})\n"
                f"tg{tg}.scaleIndividualY=Channel.keyframe().addKey(0,{6.56*size:.2f})\n"
                f"tg{tg}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                f"tg{tg}.colorR={r}\n"
                f"tg{tg}.colorG={g}\n"
                f"tg{tg}.colorB={b}\n"
                f"tg{tg}.colorA=64\n\n"
            )
            tg += 1
        if TURN_ON_FLICK and p[7] == "1":
            for i in range(3):
                for sign in (1, -1):
                    a = base + 20 * sign
                    dx = (0.39 + i * 0.14) * size * cmath.sin(
                        math.radians(base)
                    ) + 0.1 * sign * size * cmath.cos(math.radians(base))
                    dy = (0.74 + i * 0.26) * size * cmath.cos(
                        math.radians(base)
                    ) - 0.19 * sign * size * cmath.sin(math.radians(base))
                    mx, my = (x + dx).real, (y + dy).real
                    out_aff.write(
                        f"timinggroup(noinput){{\n"
                        f"  timing(0,{bpm:.2f},4.00);\n"
                        f"  scenecontrol({t},hidegroup,0.00,1);\n"
                        f"  arc({t},{t+1},{mx:.2f},{mx:.2f},s,{my:.2f},{my:.2f},0,none,true)[arctap({t})];\n"
                        f"}};\n"
                    )
                    out_lua.write(
                        f"local tg{tg}=Scene.getNoteGroup({tg})\n"
                        f"tg{tg}.rotationIndividualZ=Channel.keyframe().addKey(0,{a})\n"
                        f"tg{tg}.scaleIndividualX=Channel.keyframe().addKey(0,{0.45*size:.2f})\n"
                        f"tg{tg}.scaleIndividualY=Channel.keyframe().addKey(0,{0.6*size:.2f})\n"
                        f"tg{tg}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                        f"tg{tg}.colorR={r}\n"
                        f"tg{tg}.colorG={g}\n"
                        f"tg{tg}.colorB={b}\n\n"
                    )
                    tg += 1
        out_aff.write(
            f"timinggroup(){{\n"
            f"  timing(0,{bpm:.2f},4.00);\n"
            f"  scenecontrol(0,hidegroup,0.00,1);\n"
            f"  {raw}\n"
            f"}};\n"
        )
        tg += 1
        return tg

    def process_arc(p, bpm, frac, out_aff, out_lua, tg, raw):
        start, end = float(p[0]), float(p[1])
        x1, x2 = float(p[2]), float(p[3])
        y1, y2 = float(p[5]), float(p[6])
        ease = p[4]
        if TURN_ON_ARC2HOLD:
            base = 0
            beat = 60000.0 / bpm
            size = DEFAULT_NOTE_SIZE
            has_trace_at_start = functions.is_there_a_trace_at_start(raw)
            has_trace_at_end = functions.is_there_a_trace_at_end(raw)
            override = functions.get_arc_color(start, x1, y1)
            if override:
                sr, sg, sb = override
            else:
                sr, sg, sb = functions.get_color(frac.get(int(start), "other"))
            if not has_trace_at_start and not has_trace_at_end:
                step = beat / HOLD_DENSITY
                dirs = [0, 90, 180, 270]
                gids = list(range(tg, tg + 4))
                for idx, offset in enumerate(dirs):
                    gid = gids[idx]
                    out_aff.write(
                        f"timinggroup(noinput){{\n" f"  timing(0,{bpm:.2f},4.00);\n"
                    )
                    current = start
                    while current <= end:
                        pval = (current - start) / (end - start) if end > start else 1.0
                        ex, ey = functions.ease_xy(ease, pval)
                        xi = x1 + (x2 - x1) * ex
                        yi = y1 + (y2 - y1) * ey
                        ang = base + offset
                        dx = size * math.sin(math.radians(ang)) / 4
                        dy = size * math.cos(math.radians(ang)) / 2
                        nx, ny = xi + dx, yi + dy
                        out_aff.write(
                            f"  arc({int(current)},{int(current+1)},{nx:.2f},{nx:.2f},s,{ny:.2f},{ny:.2f},0,none,true)[arctap({int(current)})];\n"
                        )
                        current += step
                    out_aff.write("};\n")
                    out_lua.write(
                        f"local tg{gid}=Scene.getNoteGroup({gid})\n"
                        f"tg{gid}.rotationIndividualZ=Channel.keyframe().addKey(0,{ang})\n"
                        f"tg{gid}.scaleIndividualX=Channel.keyframe().addKey(0,{0.9*size:.2f})\n"
                        f"tg{gid}.scaleIndividualY=Channel.keyframe().addKey(0,{0.6*size:.2f})\n"
                        f"tg{gid}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                        f"tg{gid}.colorR={sr}\n"
                        f"tg{gid}.colorG={sg}\n"
                        f"tg{gid}.colorB={sb}\n\n"
                    )
                tg += 4

                if TURN_ON_COLOR_INSIDE:
                    out_aff.write(
                        f"timinggroup(noinput){{\n" f"  timing(0,{bpm:.2f},4.00);\n"
                    )
                    current = start
                    while current <= end:
                        pval = (current - start) / (end - start) if end > start else 1.0
                        ex, ey = functions.ease_xy(ease, pval)
                        xi = x1 + (x2 - x1) * ex
                        yi = y1 + (y2 - y1) * ey
                        ang = base
                        dx = 0.39 * size * math.sin(math.radians(ang))
                        dy = 0.74 * size * math.cos(math.radians(ang))
                        xf, yf = xi + dx, yi + dy
                        out_aff.write(
                            f"  arc({int(current)},{int(current+1)},{xf:.2f},{xf:.2f},s,{yf:.2f},{yf:.2f},0,none,true)[arctap({int(current)})];\n"
                        )
                        current += step
                    out_aff.write("};\n")
                    out_lua.write(
                        f"local tg{tg}=Scene.getNoteGroup({tg})\n"
                        f"tg{tg}.rotationIndividualZ=Channel.keyframe().addKey(0,{ang})\n"
                        f"tg{tg}.scaleIndividualX=Channel.keyframe().addKey(0,{0.9*size:.2f})\n"
                        f"tg{tg}.scaleIndividualY=Channel.keyframe().addKey(0,{6.56*size:.2f})\n"
                        f"tg{tg}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                        f"tg{tg}.colorR={sr}\n"
                        f"tg{tg}.colorG={sg}\n"
                        f"tg{tg}.colorB={sb}\n"
                        f"tg{tg}.colorA=64\n\n"
                    )
                    tg += 1

            elif has_trace_at_start and has_trace_at_end:
                s = has_trace_at_start
                inner_s = s[s.find("(") + 1 : s.find(")")]
                ps = [p.strip() for p in inner_s.split(",")]
                e = has_trace_at_end
                inner_e = e[e.find("(") + 1 : e.find(")")]
                pe = [p.strip() for p in inner_e.split(",")]
                start_angle = float(ps[1]) - float(ps[0]) - 1
                end_angle = float(pe[1]) - float(pe[0]) - 1
                step = beat / HOLD_DENSITY
                total = int((end - start) / step) + 1
                delta = (end_angle - start_angle) / max(total - 1, 1)
                current = start
                for i in range(total):
                    ang = start_angle + i * delta
                    for j in range(4):
                        pval = (current - start) / (end - start) if end > start else 1.0
                        ex, ey = functions.ease_xy(ease, pval)
                        xi = x1 + (x2 - x1) * ex
                        yi = y1 + (y2 - y1) * ey
                        new_ang = ang + j * 90
                        dx = size * math.sin(math.radians(new_ang)) / 4
                        dy = size * math.cos(math.radians(new_ang)) / 2
                        nx, ny = xi + dx, yi + dy
                        out_aff.write(
                            f"timinggroup(noinput){{\n"
                            f"  timing(0,{bpm:.2f},4.00);\n"
                            f"  scenecontrol({int(current)},hidegroup,0.00,1);\n"
                            f"  arc({int(current)},{int(current+1)},{nx:.2f},{nx:.2f},s,{ny:.2f},{ny:.2f},0,none,true)[arctap({int(current)})];\n"
                            f"}};\n"
                        )
                        out_lua.write(
                            f"local tg{tg}=Scene.getNoteGroup({tg})\n"
                            f"tg{tg}.rotationIndividualZ=Channel.keyframe().addKey(0,{new_ang})\n"
                            f"tg{tg}.scaleIndividualX=Channel.keyframe().addKey(0,{0.9*size:.2f})\n"
                            f"tg{tg}.scaleIndividualY=Channel.keyframe().addKey(0,{0.6*size:.2f})\n"
                            f"tg{tg}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                            f"tg{tg}.colorR={sr}\n"
                            f"tg{tg}.colorG={sg}\n"
                            f"tg{tg}.colorB={sb}\n\n"
                        )
                        tg += 1
                    if TURN_ON_COLOR_INSIDE:
                        dx = 0.39 * size * math.sin(math.radians(ang))
                        dy = 0.74 * size * math.cos(math.radians(ang))
                        xf, yf = xi + dx, yi + dy
                        out_aff.write(
                            f"timinggroup(noinput){{\n"
                            f"  timing(0,{bpm:.2f},4.00);\n"
                            f"  arc({int(current)},{int(current+1)},{xf:.2f},{xf:.2f},s,{yf:.2f},{yf:.2f},0,none,true)[arctap({int(current)})];\n"
                            f"  scenecontrol({int(current)},hidegroup,0.00,1);\n"
                            f"}};\n"
                        )
                        out_lua.write(
                            f"local tg{tg}=Scene.getNoteGroup({tg})\n"
                            f"tg{tg}.rotationIndividualZ=Channel.keyframe().addKey(0,{ang})\n"
                            f"tg{tg}.scaleIndividualX=Channel.keyframe().addKey(0,{0.9*size:.2f})\n"
                            f"tg{tg}.scaleIndividualY=Channel.keyframe().addKey(0,{6.56*size:.2f})\n"
                            f"tg{tg}.scaleIndividualZ=Channel.keyframe().addKey(0,0)\n"
                            f"tg{tg}.colorR={sr}\n"
                            f"tg{tg}.colorG={sg}\n"
                            f"tg{tg}.colorB={sb}\n"
                            f"tg{tg}.colorA=64\n\n"
                        )
                        tg += 1
                    current += step
            out_aff.write(f"timinggroup(){{\n" f"  timing(0,{bpm:.2f},4.00);\n")
            if not functions.is_there_an_arc_at_start(raw):
                out_aff.write(
                    f"  arc({int(start)},{int(start+1)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},0,none,true)[arctap({int(start)})];\n"
                )
            out_aff.write(
                f"  arc({int(start)},{int(end)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},0,none,false);\n"
                f"}};\n"
            )
            out_lua.write(
                f"local tg{tg} = Scene.getNoteGroup({tg})\n" f"tg{tg}.colorA = 0\n\n"
            )
            tg += 1
            out_aff.write(
                f"timinggroup(){{\n"
                f"  timing(0,0.01,4.00);\n"
                f"  scenecontrol(0,hidegroup,0.00,1);\n"
                f"  timing(1,0.00,4.00);\n"
                f"  arc({int(start)},{int(end)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},0,none,false);\n"
                f"  arc({int(start)},{int(end)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},1,none,false);\n"
                f"}};\n"
            )
            out_lua.write(
                f"local tg{tg} = Scene.getNoteGroup({tg})\n" f"tg{tg}.colorA = 0\n\n"
            )
            tg += 1
            functions.set_arc_color(raw, (sr, sg, sb))
            return tg
        else:
            out_aff.write(
                f"timinggroup(noheightindicator){{\n" f"  timing(0,{bpm:.2f},4.00);\n"
            )
            if not functions.is_there_an_arc_at_start(raw):
                out_aff.write(
                    f"  arc({int(start)},{int(start+1)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},0,none,true)[arctap({int(start)})];\n"
                )
            out_aff.write(
                f"  arc({int(start)},{int(end)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},0,none,false);\n"
                f"}};\n"
            )
            tg += 1
            out_aff.write(
                f"timinggroup(noheightindicator){{\n"
                f"  timing(0,0.01,4.00);\n"
                f"  scenecontrol(0,hidegroup,0.00,1);\n"
                f"  timing(1,0.00,4.00);\n"
                f"  arc({int(start)},{int(end)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},0,none,false);\n"
                f"  arc({int(start)},{int(end)},{x1:.2f},{x2:.2f},{ease},{y1:.2f},{y2:.2f},1,none,false);\n"
                f"}};\n"
            )
            tg += 1
            return tg

    lines = functions.read_lines(input_path)
    max_t = max(
        (
            float(m.group(1))
            for L in lines
            if (m := re.search(r"arc\(\s*[\d.]+,\s*([\d.]+)", L))
        ),
        default=0,
    )
    bpm = None
    tg = 1

    with open(output_path, "w") as a, open("Scenecontrol/polytone.lua", "w") as l:
        a.write(
            f"AudioOffset:{AUDIO_OFFSET}\n"
            f"-\n"
            f"timing(0,{BASE_BPM:.2f},4.00);\n"
            f"camera(0,0.00,-900.00,500.00,0.00,27.50,0.00,l,0);\n"
        )
        for L in lines:
            t0, b0 = functions.parse_timing_line(L, a)
            if b0 and b0 > 0:
                bpm = b0
                frac = functions.build_fraction_dict(t0, max_t, bpm)
                continue
            if not L.strip().startswith("arc("):
                continue
            p, t, s, type = functions.parse_arc_line(L)
            if not p:
                continue
            if type:
                tg = process_arctap(p, t, bpm, frac, a, l, tg, L.strip(), s)
            else:
                tg = process_arc(p, bpm, frac, a, l, tg, L.strip())


if __name__ == "__main__":
    temp_aff = functions.preprocess(INPUT_AFF)
    process(temp_aff, OUTPUT_AFF)
    os.unlink(temp_aff)
