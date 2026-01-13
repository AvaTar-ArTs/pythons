🎨 SHELL := /bin/bash

✨ setup:
	🔧 mamba env create -f env/environment.yml || mamba env update -f env/environment.yml
	💡 @echo 'Run: mamba activate storyboard'
	🔑 chmod +x scripts/storyboard_cli.py

🚀 generate:
	🔄 mamba activate storyboard && scripts/storyboard_cli.py generate $(name)

🎬 render:
	🎶 mamba activate storyboard && scripts/storyboard_cli.py render $(name) --duration $(dur) --bpm $(bpm) --sections $(sections) --tempo-map $(tempo)

🏗️ build:
	🛠️ mamba activate storyboard && scripts/storyboard_cli.py build $(name) --duration $(dur)
