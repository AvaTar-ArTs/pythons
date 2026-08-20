<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Two Script Variants</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg:#f3f0e8;
      --paper:#fbf8f1;
      --ink:#161616;
      --muted:#5f5a52;
      --line:#d7d0c4;
      --accent:#b56a2d;
      --accent-2:#23443c;
      --shadow:0 20px 60px rgba(0,0,0,.08);
      --radius:22px;
    }

    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{
      margin:0;
      font-family:"Space Grotesk", sans-serif;
      color:var(--ink);
      background:
        radial-gradient(circle at 20% 10%, rgba(181,106,45,.08), transparent 25%),
        radial-gradient(circle at 80% 20%, rgba(35,68,60,.08), transparent 25%),
        linear-gradient(180deg, #f8f4ec 0%, var(--bg) 100%);
      min-height:100vh;
    }

    .grain::before{
      content:"";
      position:fixed;
      inset:0;
      pointer-events:none;
      opacity:.05;
      background-image:
        linear-gradient(rgba(0,0,0,.5) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,.5) 1px, transparent 1px);
      background-size: 3px 3px, 3px 3px;
      mix-blend-mode:multiply;
    }

    .wrap{
      width:min(1200px, calc(100% - 2rem));
      margin:0 auto;
    }

    header{
      padding:1rem 0 0;
    }

    nav{
      display:flex;
      justify-content:space-between;
      align-items:center;
      padding:.9rem 1rem;
      background:rgba(251,248,241,.7);
      border:1px solid rgba(22,22,22,.08);
      border-radius:999px;
      backdrop-filter: blur(14px);
      box-shadow: var(--shadow);
      animation: rise .8s ease both;
    }

    .brand{
      display:flex;
      align-items:center;
      gap:.8rem;
      font-weight:700;
      letter-spacing:.03em;
    }

    .brand-mark{
      width:34px;height:34px;border-radius:10px;
      background:
        linear-gradient(135deg, var(--accent), #d79c67),
        linear-gradient(315deg, var(--accent-2), #3d6b5f);
      position:relative;
      overflow:hidden;
      box-shadow: inset 0 1px 0 rgba(255,255,255,.5);
    }

    .brand-mark::after{
      content:"";
      position:absolute;
      inset:7px;
      border:2px solid rgba(255,255,255,.7);
      border-radius:8px;
      transform:rotate(12deg);
    }

    .nav-links{
      display:flex;
      gap:1rem;
      flex-wrap:wrap;
    }

    .nav-links a{
      color:var(--muted);
      text-decoration:none;
      font-size:.95rem;
      transition:.25s ease;
    }

    .nav-links a:hover{color:var(--ink)}

    main{
      padding:clamp(2rem, 5vw, 4rem) 0 4rem;
    }

    .hero{
      display:grid;
      grid-template-columns:1.15fr .85fr;
      gap:clamp(1.25rem, 3vw, 3rem);
      align-items:end;
      min-height:48vh;
      padding:clamp(2rem, 4vw, 3rem) 0 2rem;
    }

    .kicker{
      font-family:"IBM Plex Mono", monospace;
      font-size:.82rem;
      letter-spacing:.12em;
      text-transform:uppercase;
      color:var(--accent-2);
      margin-bottom:1rem;
      animation: rise .7s .05s ease both;
    }

    h1{
      margin:0;
      font-size:clamp(2.7rem, 8vw, 7rem);
      line-height:.92;
      letter-spacing:-.05em;
      max-width:10ch;
      animation: rise .8s .12s ease both;
    }

    .hero p{
      max-width:58ch;
      color:var(--muted);
      font-size:clamp(1rem, 1.4vw, 1.15rem);
      line-height:1.7;
      margin:1.25rem 0 0;
      animation: rise .8s .22s ease both;
    }

    .hero-aside{
      background:linear-gradient(180deg, rgba(251,248,241,.8), rgba(255,255,255,.55));
      border:1px solid rgba(22,22,22,.08);
      border-radius:var(--radius);
      padding:1.2rem;
      box-shadow:var(--shadow);
      backdrop-filter: blur(12px);
      position:relative;
      overflow:hidden;
      animation: rise .9s .3s ease both;
    }

    .hero-aside::before{
      content:"";
      position:absolute;
      width:180px;height:180px;
      border-radius:50%;
      right:-40px; top:-40px;
      background:radial-gradient(circle, rgba(181,106,45,.22), transparent 65%);
    }

    .mini-label{
      font-family:"IBM Plex Mono", monospace;
      font-size:.8rem;
      color:var(--muted);
      margin-bottom:1rem;
    }

    .feature-list{
      display:grid;
      gap:.85rem;
    }

    .feature-item{
      display:grid;
      grid-template-columns:auto 1fr;
      gap:.8rem;
      align-items:start;
      padding:.85rem 0;
      border-bottom:1px dashed rgba(22,22,22,.12);
    }

    .feature-item:last-child{border-bottom:none}

    .dot{
      width:11px;height:11px;border-radius:50%;
      margin-top:.35rem;
      background:linear-gradient(135deg, var(--accent), var(--accent-2));
      box-shadow:0 0 0 6px rgba(181,106,45,.08);
    }

    .section{
      padding:clamp(2rem, 5vw, 4rem) 0;
    }

    .section-head{
      display:grid;
      grid-template-columns:.9fr 1.1fr;
      gap:2rem;
      align-items:end;
      margin-bottom:2rem;
    }

    .section-head h2{
      margin:0;
      font-size:clamp(1.8rem, 4vw, 3.8rem);
      line-height:.95;
      letter-spacing:-.04em;
    }

    .section-head p{
      margin:0;
      color:var(--muted);
      line-height:1.7;
      max-width:60ch;
    }

    .scripts{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:1.25rem;
    }

    .script-panel{
      background:rgba(251,248,241,.78);
      border:1px solid rgba(22,22,22,.08);
      border-radius:var(--radius);
      overflow:hidden;
      box-shadow:var(--shadow);
      backdrop-filter: blur(10px);
      transform:translateY(20px);
      opacity:0;
    }

    .script-top{
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:1rem;
      padding:1rem 1rem .8rem;
      border-bottom:1px solid rgba(22,22,22,.08);
      background:
        linear-gradient(180deg, rgba(255,255,255,.55), rgba(255,255,255,0));
    }

    .script-title{
      font-weight:700;
      font-size:1rem;
    }

    .script-tag{
      font-family:"IBM Plex Mono", monospace;
      font-size:.75rem;
      padding:.38rem .55rem;
      border-radius:999px;
      background:rgba(35,68,60,.08);
      color:var(--accent-2);
      border:1px solid rgba(35,68,60,.12);
      white-space:nowrap;
    }

    pre{
      margin:0;
      padding:1rem;
      overflow:auto;
      max-height:70vh;
      background:
        linear-gradient(180deg, rgba(255,255,255,.18), rgba(255,255,255,0));
    }

    code{
      font-family:"IBM Plex Mono", monospace;
      font-size:.86rem;
      line-height:1.6;
      color:#1e1e1e;
      white-space:pre;
    }

    .actions{
      display:flex;
      gap:.75rem;
      flex-wrap:wrap;
      margin-top:1.5rem;
    }

    button{
      appearance:none;
      border:none;
      background:var(--ink);
      color:#fff;
      padding:.95rem 1.15rem;
      border-radius:999px;
      font-family:"Space Grotesk", sans-serif;
      font-weight:700;
      cursor:pointer;
      transition:transform .18s ease, background .18s ease, box-shadow .18s ease;
      box-shadow:0 10px 25px rgba(22,22,22,.14);
    }

    button.secondary{
      background:transparent;
      color:var(--ink);
      border:1px solid rgba(22,22,22,.14);
      box-shadow:none;
    }

    button:hover{
      transform:translateY(-2px) scale(1.01);
    }

    button:active{
      transform:translateY(0) scale(.99);
    }

    .reveal.in{
      animation: rise .7s ease both;
    }

    footer{
      padding:1rem 0 3rem;
      color:var(--muted);
      font-size:.95rem;
    }

    @keyframes rise{
      from{opacity:0; transform:translateY(22px)}
      to{opacity:1; transform:translateY(0)}
    }

    @media (max-width: 920px){
      .hero,
      .section-head,
      .scripts{
        grid-template-columns:1fr;
      }

      nav{
        border-radius:24px;
        align-items:flex-start;
        flex-direction:column;
        gap:.8rem;
      }

      h1{max-width:12ch}
    }
  </style>
</head>
<body class="grain">
  <div class="wrap">
    <header>
      <nav aria-label="Primary">
        <div class="brand">
          <div class="brand-mark" aria-hidden="true"></div>
          <span>Script Variants</span>
        </div>
        <div class="nav-links">
          <a href="#overview">Overview</a>
          <a href="#scripts">Scripts</a>
        </div>
      </nav>
    </header>

    <main>
      <section class="hero" id="overview">
        <div>
          <div class="kicker">Python / CSV naming update</div>
          <h1>Two complete script versions.</h1>
          <p>
            Below are both requested variants: one using the previous fix based on the scanned folder name with numeric uniqueness, and one using the updated MMDD suffix behavior when a matching file already exists.
          </p>
          <div class="actions">
            <button data-copy="script1">Copy previous-fix version</button>
            <button class="secondary" data-copy="script2">Copy MMDD version</button>
          </div>
        </div>

        <aside class="hero-aside">
          <div class="mini-label">Included differences</div>
          <div class="feature-list">
            <div class="feature-item">
              <div class="dot"></div>
              <div>
                <strong>Script 1</strong><br>
                Names output from scanned folder name and uses <code>_1</code>, <code>_2</code> if needed.
              </div>
            </div>
            <div class="feature-item">
              <div class="dot"></div>
              <div>
                <strong>Script 2</strong><br>
                Same folder-based naming, but uniqueness first uses <code>_MMDD</code>, then <code>_MMDD_1</code>, etc.
              </div>
            </div>
          </div>
        </aside>
      </section>

      <section class="section" id="scripts">
        <div class="section-head">
          <h2>Full rewritten scripts</h2>
          <p>
            Both are complete and ready to paste into separate files. Suggested names:
            <code>doc_csv_folder_name.py</code> and <code>doc_csv_folder_name_mmdd.py</code>.
          </p>
        </div>

        <div class="scripts">
          <article class="script-panel reveal">
            <div class="script-top">
              <div class="script-title">Script 1 — Previous fix</div>
              <div class="script-tag">folder-based name + _1 fallback</div>
            </div>
            <pre><code id="script1">import csv
import os
import re
import sys
from datetime import datetime

from exclude_patterns import FULL_EXCLUDED_PATTERNS


LAST_DIRECTORY_FILE = "docs.txt"


def get_creation_date(filepath):
    """Get the creation date of a file formatted as MM-DD-YY."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        print(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


def format_file_size(size_in_bytes):
    """Format file size into a human-readable string."""
    try:
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} B"
        size_in_bytes /= 1024
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} KB"
        size_in_bytes /= 1024
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} MB"
        size_in_bytes /= 1024
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} GB"
        size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} TB"
    except Exception as e:
        print(f"Error formatting file size: {e}")
        return "Unknown"


def generate_dry_run_csv(directories, csv_path):
    """Scan the given directories and generate a CSV of matching document files."""
    rows = []

    excluded_patterns = FULL_EXCLUDED_PATTERNS

    file_types = {
        ".pdf": "Documents",
        ".csv": "Documents",
        ".html": "Documents",
        ".css": "Documents",
        ".js": "Documents",
        ".json": "Documents",
        ".sh": "Documents",
        ".md": "Documents",
        ".txt": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".ppt": "Documents",
        ".pptx": "Documents",
        ".xlsx": "Documents",
        ".py": "Documents",
        ".xml": "Documents",
    }

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [
                d
                for d in dirs
                if not any(
                    re.match(pattern, os.path.join(root, d))
                    for pattern in excluded_patterns
                )
            ]

            for file in files:
                file_path = os.path.join(root, file)

                if any(re.match(pattern, file_path) for pattern in excluded_patterns):
                    continue

                file_ext = os.path.splitext(file)[1].lower()

                if file_ext in file_types:
                    try:
                        file_size = format_file_size(os.path.getsize(file_path))
                        creation_date = get_creation_date(file_path)
                        rows.append([file, file_size, creation_date, root])
                    except FileNotFoundError:
                        print(f"File not found during scan, skipping: {file_path}")
                        continue

    write_csv(csv_path, rows)


def write_csv(csv_path, rows):
    """Write the collected rows to a CSV file."""
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Filename", "File Size", "Creation Date", "Original Path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Original Path": row[3],
                }
            )


def get_unique_file_path(base_path):
    """If base_path exists, append _1, _2, etc. until a unique path is found."""
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def save_last_directory(directory):
    """Save the last scanned directory."""
    with open(LAST_DIRECTORY_FILE, "w", encoding="utf-8") as file:
        file.write(directory)


def load_last_directory():
    """Load the last scanned directory if available."""
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def sanitize_filename(name):
    """Convert a folder name into a safe filename."""
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


if __name__ == "__main__":
    if len(sys.argv) &gt; 1:
        directories = sys.argv[1:]
    else:
        directories = []
        last_directory = load_last_directory()

        while True:
            if last_directory:
                use_last = (
                    input(
                        f"Do you want to use the last directory '{last_directory}'? (Y/N): "
                    )
                    .strip()
                    .lower()
                )
                if use_last == "y":
                    directories.append(last_directory)
                    break
                else:
                    source_directory = input(
                        "Please enter a new source directory to scan for document files: "
                    ).strip()
            else:
                source_directory = input(
                    "Please enter a source directory to scan for document files: "
                ).strip()

            if source_directory == "":
                break

            if os.path.isdir(source_directory):
                directories.append(source_directory)
                save_last_directory(source_directory)
                break
            else:
                print(f"'{source_directory}' is not a valid directory. Please try again.")

    if directories:
        print(f"Scanning directories: {directories}")

        folder_names = [
            sanitize_filename(os.path.basename(os.path.normpath(d)))
            for d in directories
        ]
        joined_folder_names = "_".join(folder_names)

        if not joined_folder_names:
            joined_folder_names = "root"

        csv_filename = f"docs-{joined_folder_names}.csv"
        csv_output_path = os.path.join(os.getcwd(), csv_filename)
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_dry_run_csv(directories, csv_output_path)
        print(f"Document scan completed. Output saved to {csv_output_path}")
    else:
        print("No directories were provided to scan.")
</code></pre>
          </article>

          <article class="script-panel reveal">
            <div class="script-top">
              <div class="script-title">Script 2 — MMDD fallback</div>
              <div class="script-tag">folder-based name + _MMDD fallback</div>
            </div>
            <pre><code id="script2">import csv
import os
import re
import sys
from datetime import datetime

from exclude_patterns import FULL_EXCLUDED_PATTERNS


LAST_DIRECTORY_FILE = "docs.txt"


def get_creation_date(filepath):
    """Get the creation date of a file formatted as MM-DD-YY."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        print(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


def format_file_size(size_in_bytes):
    """Format file size into a human-readable string."""
    try:
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} B"
        size_in_bytes /= 1024
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} KB"
        size_in_bytes /= 1024
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} MB"
        size_in_bytes /= 1024
        if size_in_bytes &lt; 1024:
            return f"{size_in_bytes:.2f} GB"
        size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} TB"
    except Exception as e:
        print(f"Error formatting file size: {e}")
        return "Unknown"


def generate_dry_run_csv(directories, csv_path):
    """Scan the given directories and generate a CSV of matching document files."""
    rows = []

    excluded_patterns = FULL_EXCLUDED_PATTERNS

    file_types = {
        ".pdf": "Documents",
        ".csv": "Documents",
        ".html": "Documents",
        ".css": "Documents",
        ".js": "Documents",
        ".json": "Documents",
        ".sh": "Documents",
        ".md": "Documents",
        ".txt": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".ppt": "Documents",
        ".pptx": "Documents",
        ".xlsx": "Documents",
        ".py": "Documents",
        ".xml": "Documents",
    }

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [
                d
                for d in dirs
                if not any(
                    re.match(pattern, os.path.join(root, d))
                    for pattern in excluded_patterns
                )
            ]

            for file in files:
                file_path = os.path.join(root, file)

                if any(re.match(pattern, file_path) for pattern in excluded_patterns):
                    continue

                file_ext = os.path.splitext(file)[1].lower()

                if file_ext in file_types:
                    try:
                        file_size = format_file_size(os.path.getsize(file_path))
                        creation_date = get_creation_date(file_path)
                        rows.append([file, file_size, creation_date, root])
                    except FileNotFoundError:
                        print(f"File not found during scan, skipping: {file_path}")
                        continue

    write_csv(csv_path, rows)


def write_csv(csv_path, rows):
    """Write the collected rows to a CSV file."""
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Filename", "File Size", "Creation Date", "Original Path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Original Path": row[3],
                }
            )


def get_unique_file_path(base_path):
    """
    If base_path exists, append _MMDD.
    If that also exists, append _MMDD_1, _MMDD_2, etc.
    """
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    date_suffix = datetime.now().strftime("%m%d")

    new_path = f"{base}_{date_suffix}{ext}"
    if not os.path.exists(new_path):
        return new_path

    counter = 1
    while True:
        new_path = f"{base}_{date_suffix}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def save_last_directory(directory):
    """Save the last scanned directory."""
    with open(LAST_DIRECTORY_FILE, "w", encoding="utf-8") as file:
        file.write(directory)


def load_last_directory():
    """Load the last scanned directory if available."""
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def sanitize_filename(name):
    """Convert a folder name into a safe filename."""
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


if __name__ == "__main__":
    if len(sys.argv) &gt; 1:
        directories = sys.argv[1:]
    else:
        directories = []
        last_directory = load_last_directory()

        while True:
            if last_directory:
                use_last = (
                    input(
                        f"Do you want to use the last directory '{last_directory}'? (Y/N): "
                    )
                    .strip()
                    .lower()
                )
                if use_last == "y":
                    directories.append(last_directory)
                    break
                else:
                    source_directory = input(
                        "Please enter a new source directory to scan for document files: "
                    ).strip()
            else:
                source_directory = input(
                    "Please enter a source directory to scan for document files: "
                ).strip()

            if source_directory == "":
                break

            if os.path.isdir(source_directory):
                directories.append(source_directory)
                save_last_directory(source_directory)
                break
            else:
                print(f"'{source_directory}' is not a valid directory. Please try again.")

    if directories:
        print(f"Scanning directories: {directories}")

        folder_names = [
            sanitize_filename(os.path.basename(os.path.normpath(d)))
            for d in directories
        ]
        joined_folder_names = "_".join(folder_names)

        if not joined_folder_names:
            joined_folder_names = "root"

        csv_filename = f"docs-{joined_folder_names}.csv"
        csv_output_path = os.path.join(os.getcwd(), csv_filename)
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_dry_run_csv(directories, csv_output_path)
        print(f"Document scan completed. Output saved to {csv_output_path}")
    else:
        print("No directories were provided to scan.")
</code></pre>
          </article>
        </div>
      </section>
    </main>

    <footer>
      Use either script as-is, depending on whether you want numeric fallback or MMDD fallback.
    </footer>
  </div>

  <script>
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('in');
      });
    }, { threshold: 0.12 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    document.querySelectorAll('[data-copy]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-copy');
        const text = document.getElementById(id).textContent;
        try {
          await navigator.clipboard.writeText(text);
          const original = btn.textContent;
          btn.textContent = 'Copied';
          setTimeout(() => btn.textContent = original, 1400);
        } catch (e) {
          alert('Copy failed. Please copy manually.');
        }
      });
    });
  </script>
</body>
</html>

