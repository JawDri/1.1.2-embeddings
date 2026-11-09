# Lesson 1.1.2 — demo code: Embeddings, How AI Understands Meaning

| File | What it shows | Needs |
|---|---|---|
| `vector_map_2d.py` | The 2D map from slide 04 and its cosine similarities. | nothing (no packages) |
| `semantic_search_demo.py` | A real embedding model on your own computer: the refund example and the SKU trap. `--query "..."` for your own search. | nothing (free; downloads a ~70 MB model once) |

The model is saved once, outside this folder: `%LOCALAPPDATA%\ai-automation-from-scratch\fastembed`
(Mac / Linux: `~/.cache/ai-automation-from-scratch/fastembed`).

## Set up on Windows (once per computer)
PowerShell and Python 3.10 or newer ([python.org](https://www.python.org/downloads/), tick
"Add python.exe to PATH"). Open PowerShell **in this folder** (in Explorer: Shift + right-click →
"Open PowerShell window here", or `cd` to it) and run:
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```
It creates this lesson's Python environment from `requirements.txt` in
`%LOCALAPPDATA%\ai-automation-from-scratch\venvs\M1_1.1.2` (outside this folder, so the folder stays
small and Windows' path-length limit is never hit). Run it again any time: it repairs a broken setup.

## Run on Windows
```powershell
.\run.ps1 vector_map_2d.py
.\run.ps1 semantic_search_demo.py
```
If PowerShell refuses to run `.\run.ps1`:

- "running scripts is disabled": allow local scripts once for your user with
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or run
  `powershell -ExecutionPolicy Bypass -File .\run.ps1 <script.py>` instead.
- "not digitally signed": Windows marked these files as downloaded (from a zip, for example).
  Unblock them once, from this folder: `Get-ChildItem -Recurse | Unblock-File`.

## Mac / Linux
`setup.ps1` and `run.ps1` are for Windows. With Python 3.10 or newer (check: `python3 --version`), open
a terminal in this folder and set up once:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Then run the demos (same options as on Windows):
```bash
python vector_map_2d.py
python semantic_search_demo.py
```
In a new terminal, run `source .venv/bin/activate` first. On Ubuntu/Debian, if `python3 -m venv` fails:
`sudo apt install python3-venv`.

## Helper files (the demos need them; no need to edit them)
- `course_env.py`: the shared helper every demo imports (sets where the model is saved, makes the
  output print correctly).
- `setup.ps1` and `run.ps1`: set up this lesson once, then run a demo (Windows).
