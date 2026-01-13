# StoryBoarder CLI — Adaptive Timing Edition

This setup gives you:
- Mamba environment
- CLI with generate/render/build
- Adaptive timing: duration, BPM, tempo map, and custom sections
- Templates for README and cinematic text rendering

## Quickstart
```bash
cd storyboarder_adaptive
mamba env create -f env/environment.yml
mamba activate storyboard
chmod +x scripts/storyboard_cli.py

# create a project
scripts/storyboard_cli.py generate "Stormchild"

# add CSV/JSON scenes to projects/stormchild/
# then render with timing
scripts/storyboard_cli.py render "Stormchild" --duration 210 --bpm 92   --sections examples/sections.json --tempo-map examples/tempo.json

# package
scripts/storyboard_cli.py build "Stormchild" --duration 210
```
