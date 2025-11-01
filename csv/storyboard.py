#!/usr/bin/env python3

import csv, json, pathlib, zipfile, subprocess, math
import typer
from jinja2 import Template
from rich.console import Console
from rich.progress import track

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_210 = 210


app = typer.Typer(add_completion=False)
console = Console()

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
TPL_README = ROOT / "templates" / "readme_template.j2"
TPL_STORY = ROOT / "templates" / "storyboard_text_template.j2"
PROJECTS.mkdir(exist_ok=True)

# ---------- Helpers ----------

def proj_dir(bname: str) -> pathlib.Path:
    p = PROJECTS / bname.lower().replace(" ", "_")
    p.mkdir(exist_ok=True)
    return p

def sec_to_str(sec: float) -> str:
    sec = max(0, int(round(sec)))
    return f"{sec//60:02d}:{sec%60:02d}"

def load_sections(path: pathlib.Path, total_duration: float):
    if path and path.exists():
        data = json.loads(path.read_text())
        return [{"name":d["name"],"start":float(d["start"]),"end":float(d["end"])} for d in data]
    # default single section
    return [{"name":"Whole","start":0.0,"end":float(total_duration)}]

def load_tempo(path: pathlib.Path, bpm: float|None, total_duration: float):
    segs = []
    if path and path.exists():
        arr = json.loads(path.read_text())
        arr = sorted(arr, key=lambda x: x["t"])
        for i,seg in enumerate(arr):
            t0 = float(seg["t"]); b = float(seg["bpm"])
            t1 = float(arr[i+1]["t"]) if i+1 < len(arr) else float(total_duration)
            segs.append({"start":t0,"end":t1,"bpm":b})
    elif bpm:
        segs = [{"start":0.0,"end":float(total_duration),"bpm":float(bpm)}]
    else:
        segs = [{"start":0.0,"end":float(total_duration),"bpm":None}]
    return segs

def beats_between(segs, a, b):
    if not any(s["bpm"] for s in segs):
        return None
    a = float(a); b = float(b)
    beats = 0.0
    for s in segs:
        s0, s1, sbpm = s["start"], s["end"], s["bpm"]
        if sbpm is None: continue
        lo = max(a, s0); hi = min(b, s1)
        if hi > lo:
            beats += (hi - lo) * sbpm/60.0
    return beats

def beat_at(segs, t):
    if not any(s["bpm"] for s in segs): return None
    t = float(t)
    beats = 0.0
    for s in segs:
        s0, s1, sbpm = s["start"], s["end"], s["bpm"]
        if sbpm is None: continue
        if t <= s0: break
        span = min(t, s1) - s0
        if span > 0:
            beats += span * sbpm/60.0
        if t <= s1: break
    return beats

def default_ratios(section_name: str, scene_type: str) -> float:
    table = {
        "Intro":{"Cover":0.5,"Transition":0.3,"Filler":0.2},
        "Verse":{"Main":0.5,"Transition":0.25,"Filler":0.25},
        "Chorus":{"Main":0.6,"Transition":0.25,"Filler":0.15},
        "Bridge":{"Main":0.45,"Transition":0.35,"Filler":0.2},
        "Instrumental":{"Transition":0.5,"Filler":0.5},
        "Drop":{"Transition":0.6,"Filler":0.4},
        "Outro":{"Main":0.3,"Transition":0.3,"Filler":0.4},
        "Whole":{"Main":0.5,"Transition":0.25,"Filler":0.25}
    }
    sec = table.get(section_name, table["Whole"])
    return sec.get(scene_type, 0.2)

def line_weight(line: str, emphasis: bool=False) -> float:
    L = max(1, len(line or ""))
    punct = (line or "").count(",") + (line or "").count(".") + (line or "").count(";")
    emph = 2 if emphasis else 0
    return 1*L + 0.5*punct + emph

def mmss_range(a,b): return f"{sec_to_str(a)}-{sec_to_str(b)}"

# ---------- Data IO ----------

def load_csv(path: pathlib.Path):
    rows = []
    if not path.exists(): return rows
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # normalize keys
            r = {k.strip(): v for k,v in r.items()}
            try:
                r["scene_id"] = int(r.get("scene_id","0") or "0")
            except (OSError, IOError, FileNotFoundError):
            rows.append(r)
    return rows

def load_json(path: pathlib.Path):
    if not path.exists(): return []
    try:
        data = json.loads(path.read_text() or "[]")
        return data
    except Exception:
        return []

def merge_rows(json_rows, csv_rows):
    by_id_csv = {int(r.get("scene_id",0)): r for r in csv_rows}
    merged = []
    if json_rows:
        for s in json_rows:
            sid = int(s.get("scene_id",0))
            c = by_id_csv.get(sid, {})
            def pick(k, default=""):
                v = s.get(k, None)
                if v not in (None,""): return v
                v = c.get(k, None)
                if v not in (None,""): return v
                return default
            merged.append({
                "scene_id": sid,
                "scene_type": pick("scene_type","Filler"),
                "lyric_line": pick("lyric_line",""),
                "mood": pick("mood",""),
                "lighting_style": pick("lighting_style",""),
                "camera_style": pick("camera_style",""),
                "color_palette": pick("color_palette",""),
                "symbolism": pick("symbolism",""),
                "prompt_description": pick("prompt_description",""),
                "transition_method": pick("transition_method",""),
                "section_name": pick("section_name","Whole"),
                "emphasis": bool(pick("emphasis", False)),
                "timestamp": pick("timestamp",""),
            })
    else:
        for c in csv_rows:
            merged.append({
                "scene_id": int(c.get("scene_id",0)),
                "scene_type": c.get("scene_type","Filler"),
                "lyric_line": c.get("lyric_line",""),
                "mood": c.get("mood",""),
                "lighting_style": c.get("lighting_style",""),
                "camera_style": c.get("camera_style",""),
                "color_palette": c.get("color_palette",""),
                "symbolism": c.get("symbolism",""),
                "prompt_description": c.get("prompt_description",""),
                "transition_method": c.get("transition_method",""),
                "section_name": c.get("section_name","Whole"),
                "emphasis": bool(c.get("emphasis","") in ("1","true","True","yes","Yes")),
                "timestamp": c.get("timestamp",""),
            })
    merged.sort(key=lambda x: (int(x["scene_id"]), x.get("timestamp","")))
    return merged

def allocate(scenes, total_duration, bpm=None, tempo_map=None, sections=None):
    # Build segments and sections
    segs = load_tempo(tempo_map, bpm, total_duration)
    secs = load_sections(sections, total_duration)

    # group scenes by section
    by_section = {s["name"]: [] for s in secs}
    for sc in scenes:
        name = sc.get("section_name","Whole")
        if name not in by_section: by_section[name] = []
        by_section[name].append(sc)

    # assign durations inside each section by ratios * line weight
    for sec in secs:
        sname = sec["name"]; sstart=sec["start"]; send=sec["end"]
        dur = max(0.0, send - sstart)
        pool = by_section.get(sname, [])
        if not pool: continue
        weights = []
        for sc in pool:
            r = default_ratios(sname, sc.get("scene_type","Filler"))
            w = line_weight(sc.get("lyric_line",""), sc.get("emphasis", False))
            weights.append(max(1e-6, r*w))
        total_w = sum(weights) or 1.0
        allocs = [dur*(w/total_w) for w in weights]
        cursor = sstart
        for sc, d in zip(pool, allocs):
            sc["start_sec"] = round(cursor,3)
            sc["end_sec"] = round(cursor+d,3)
            sc["duration_sec"] = round(d,3)
            sb = beat_at(segs, sc["start_sec"])
            eb = beat_at(segs, sc["end_sec"])
            sc["start_beat"] = None if sb is None else round(sb,3)
            sc["end_beat"] = None if eb is None else round(eb,3)
            sc["timestamp"] = f"{sec_to_str(sc['start_sec'])}-{sec_to_str(sc['end_sec'])}"
            cursor += d

    return scenes

# ---------- Commands ----------

@app.command()
def generate(bname: str):
    """Scaffold empty files for a new storyboard project."""
    p = proj_dir(bname)
    base = bname.lower().replace(" ","_")
    csv_path = p / f"{base}_storyboard.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scene_id","timestamp","section_name","scene_type","lyric_line","mood",
            "lighting_style","camera_style","color_palette","symbolism",
            "prompt_description","transition_method","emphasis"
        ])
    (p / f"{base}_storyboard.json").write_text("[]")
    (p / f"{base}_storyboard.txt").write_text(f"{bname} — Cinematic Storyboard\n\n[Rendered output appears here after 'render']\n")
    console.logger.info(f"[green]✅ Created template in {p}")

@app.command()
def render(
    bname: str,
    duration: float = typer.Option(CONSTANT_210.0, help="Total duration in seconds"),
    bpm: float = typer.Option(None, help="Song BPM (optional)"),
    sections: pathlib.Path = typer.Option(None, help="Path to sections.json"),
    tempo_map: pathlib.Path = typer.Option(None, help="Path to tempo.json"),
):
    """Render formatted cinematic text using adaptive timing."""
    p = proj_dir(bname); base = bname.lower().replace(" ","_")
    csv_path = p / f"{base}_storyboard.csv"
    json_path = p / f"{base}_storyboard.json"
    rows_csv = load_csv(csv_path)
    rows_json = load_json(json_path)
    scenes = merge_rows(rows_json, rows_csv)
    if not scenes:
        console.logger.info("[red]No scenes found. Fill CSV or JSON first.[/]")
        raise typer.Exit(1)

    # allocate timings
    scenes = allocate(
        scenes,
        total_duration=float(duration),
        bpm=bpm,
        tempo_map=tempo_map,
        sections=sections
    )

    # render text
    tpl = Template(TPL_STORY.read_text())
    text = tpl.render(title=bname, scenes=scenes, runtime_sec=int(duration))
    out_txt = p / f"{base}_storyboard.txt"
    out_txt.write_text(text)

    # also update JSON with timing fields
    out_json = p / f"{base}_storyboard.json"
    out_json.write_text(json.dumps(scenes, indent=2))

    console.logger.info(f"[green]✅ Rendered {out_txt.name} with {len(scenes)} scenes")
    console.logger.info(f"[green]✅ Updated {out_json.name} with timing fields")

@app.command()
def build(bname: str, duration: float = CONSTANT_210.0):
    """Package project files into a zip with README."""
    p = proj_dir(bname); base = bname.lower().replace(" ","_")
    json_path = p / f"{base}_storyboard.json"
    csv_path  = p / f"{base}_storyboard.csv"
    if not json_path.exists() or not csv_path.exists():
        console.logger.info("[red]Missing CSV/JSON in project folder[/]")
        raise typer.Exit(1)

    try:
        scenes = json.loads(json_path.read_text() or "[]")
    except Exception:
        scenes = []
    readme = Template(TPL_README.read_text()).render(title=bname, scenes=len(scenes), runtime_sec=int(duration))
    (p / "readme.txt").write_text(readme)

    zip_path = p / f"{base}_storyboard.zip"
    console.logger.info(f"[cyan]Packaging {zip_path.name}...[/]")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for file in track(list(p.iterdir()), description="Adding files..."):
            if file.is_file() and file.name != zip_path.name:
                z.write(file, arcname=file.name)
    console.logger.info(f"[green]✅ Created {zip_path}")
    
@app.command()
def list_projects():
    """List all projects."""
    console.logger.info("[bold yellow]Projects:")
    for d in PROJECTS.iterdir():
        if d.is_dir():
            console.logger.info(f" • {d.name}")

@app.command()
def open_project(bname: str):
    """Open project folder in Finder."""
    subprocess.run(["open", str(proj_dir(bname))])

if __name__ == "__main__":
    app()
