# Python environment setup — generalized how-to

**Scope:** Any Python **application or library** you clone locally (FastAPI services, CLIs, monorepos, research code). **Not** tied to a single product name—swap paths and extras for your repo.

**Reuse pattern:** prerequisites → enter project tree → choose **one** env technology → bootstrap installers → install the project → configure secrets → run → verify.

---

## 0. Prerequisites (check once)

| Check | Typical need |
|--------|----------------|
| `python3 --version` | Match the project’s **`requires-python`** (often **3.11+**). |
| Shell | **bash** or **zsh** on Unix; **PowerShell** on Windows. |
| Git | If you use `git clone` / branches. |
| C compiler / Rust | Only if dependencies build from source (wheels usually avoid this). |

Read the project’s **`README`**, **`pyproject.toml`**, or **`CONTRIBUTING`** for pinned versions and optional extras.

---

## 1. Enter the project tree

```bash
cd /path/to/your-project
```

Confirm you see **`pyproject.toml`** and/or **`requirements.txt`**, **`setup.cfg`**, or **`setup.py`**.

---

## 2. Pick exactly one environment style

| Style | Strengths | Tradeoffs |
|-------|-------------|-----------|
| **`python -m venv`** | Standard library; matches most Docker/CI **pip** flows; no extra tools. | You manage Python upgrades yourself. |
| **`uv venv`** | Very fast; good cache. | Install [uv](https://docs.astral.sh/uv/); use **`--seed`** if you want **pip** inside the venv. |
| **Miniforge + `mamba`** | Fast solver; **conda-forge** binaries (native libs, compilers). | Larger install than micromamba alone. |
| **`micromamba`** | Single static binary; same env model as conda; great for **CI** and minimal hosts. | Separate root prefix (`MAMBA_ROOT_PREFIX`); learn `micromamba` CLI. |
| **`conda`** (classic) | Universal if you already use Anaconda/Miniconda. | Slower dependency resolution than **mamba**. |

**Rule:** Do not mix multiple active env types in one shell session without knowing which **`python`** wins (IDE + shell + conda can disagree). Pick one, activate it, then install.

---

## 3. venv (stdlib)

**macOS / Linux:**

```bash
python3.12 -m venv .venv    # or python3.11, etc.
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
```

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
```

Deactivate later: **`deactivate`**.

---

## 4. uv + `.venv` (optional)

```bash
uv venv .venv --python 3.12 --seed
source .venv/bin/activate    # Windows: .venv\Scripts\activate
python -m pip install -U pip setuptools wheel
# Alternative installs: uv pip install -r requirements.txt
```

Without **`--seed`**, many **`uv venv`** layouts omit **pip**; use **`uv pip`** or add **`--seed`**.

---

## 5. Miniforge + mamba (conda-forge)

1. Install **[Miniforge](https://github.com/conda-forge/miniforge/releases)**; restart the terminal.

2. Prefer strict channel priority (once):

   ```bash
   conda config --set channel_priority strict
   ```

3. Create and activate (example env name **`myproj`**):

   ```bash
   mamba create -n myproj python=3.12 pip git -y
   mamba activate myproj
   ```

4. **Native libraries** (examples—check your project docs):

   - **Matrix / `matrix-nio[e2e]`:** the **C library `libolm`** is often **not** on **conda-forge** for **macOS**; use **`brew install libolm`** (or your distro’s **`libolm-dev`** on Linux), then install Python extras with **pip**.
   - Heavy scientific / AV stacks: install **ffmpeg**, **cairo**, etc. from conda-forge when pip wheels fail.

5. Still use **pip** for the *application* unless the project documents conda-only packages:

   ```bash
   cd /path/to/your-project
   python -m pip install -U pip setuptools wheel
   python -m pip install -e ".[dev]"    # extras vary by project
   ```

Deactivate: **`conda deactivate`** (works after `mamba activate` on typical Miniforge setups).

---

## 6. Micromamba

Official install options: **[Micromamba installation](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)** (shell script, Homebrew, manual binary).

Typical first-time shell integration:

```bash
micromamba shell init -s zsh -r ~/micromamba
```

Restart the shell, then (use **`-s bash`** etc. if not zsh):

```bash
micromamba config append channels conda-forge
micromamba config set channel_priority strict
micromamba create -n myproj python=3.12 pip git -y
micromamba activate myproj
```

Then same **`cd` + `python -m pip install …`** as §5.

**CI / scripts** without activation:

```bash
micromamba run -n myproj pytest
micromamba run -n myproj python -m build
```

Self-update: **`micromamba self-update`**.

---

## 7. conda (classic, no mamba)

```bash
conda create -n myproj python=3.12 pip git -y
conda activate myproj
cd /path/to/your-project
python -m pip install -U pip setuptools wheel
```

---

## 8. After the env is active (all paths)

1. **Upgrade installers** (reduces weird resolver errors):

   ```bash
   python -m pip install -U pip setuptools wheel
   ```

2. **Install the project** (read upstream docs—examples):

   ```bash
   python -m pip install -e ".[dev]"
   # or:  python -m pip install -r requirements.txt
   # or:  poetry install
   # or:  uv pip install -e .
   ```

3. **Frontend** (if the repo has **`package.json`**):

   ```bash
   cd frontend-or-web   # name varies
   npm ci               # or npm install
   ```

4. **Secrets:** copy **`.env.example` → `.env`** (or use the project’s secret manager); never commit real keys.

---

## 9. Quick verification

```bash
which python
python --version
python -c "import sys; print(sys.executable)"
```

If **`which python`** is not inside **`.venv`** / **`conda` env`**, you are not in the env you think you are.

If **`pip`** keeps resolving packages under **`~/.local/lib/...`** while a conda/venv interpreter is active, set **`export PYTHONNOUSERSITE=1`** for that session so user site-packages are ignored.

**Matrix / `python-olm`:** building **`python-olm`** from PyPI sdist with **CMake 4+** often fails with *“Compatibility with CMake < 3.5 has been removed”*. Use **`export CMAKE_POLICY_VERSION_MINIMUM=3.5`** when installing **`python-olm`** or **`matrix-nio[e2e]`** (see [matrix-nio#541](https://github.com/matrix-nio/matrix-nio/issues/541)); on macOS you still need the **`libolm`** C library (**`brew install libolm`**) in most setups.

---

## 10. Optional: Node / monorepo cleanup (concept)

When you need a clean tree (disk or CI), projects often delete **regenerable** dirs: **`node_modules`**, **`.next`**, **`dist`**, **`.venv`**. Do that with project-specific scripts or a personal helper—always **`git status`** before bulk **`rm -rf`**.

---

## 11. Where to go deeper

| Topic | Starting point |
|--------|----------------|
| **uv** | [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) |
| **conda-forge** | [https://conda-forge.org/](https://conda-forge.org/) |
| **mamba / micromamba** | [https://mamba.readthedocs.io/](https://mamba.readthedocs.io/) |
| **Packaging** | [https://packaging.python.org/](https://packaging.python.org/) |

---

*This file lives in **`~/Guides`**. Product-specific walkthroughs (e.g. a single app’s tour script) should link here for “how do I env?” and stay short on the product side.*
