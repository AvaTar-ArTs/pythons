### macos terminal to convert md into pdf

To convert a Markdown (`.md`) file into a PDF using the macOS Terminal, you can use a combination of the `pandoc` tool and a LaTeX engine like `pdflatex`. Here's a step-by-step guide:

### Step 1: Install `pandoc`

First, you'll need to install `pandoc`. You can do this via Homebrew, a popular package manager for macOS. If you don't have Homebrew installed, you can install it by following the instructions on the [Homebrew website](https://brew.sh/).

Once you have Homebrew, open Terminal and install `pandoc`:

```sh
brew install pandoc
```

### Step 2: Install a LaTeX Distribution

For `pandoc` to convert Markdown files to PDF, you need a LaTeX distribution. A common and relatively lightweight choice is BasicTeX. You can install it with Homebrew as well:

```sh
brew install --cask mactex-no-gui
```

Alternatively, you can download and install the full MacTeX distribution from the [MacTeX website](https://www.tug.org/mactex/), but it's quite large.

### Step 3: Convert Markdown to PDF

Now that you have both `pandoc` and a LaTeX engine installed, you can convert your Markdown file to a PDF. Use the following command, replacing `input.md` with the path to your Markdown file and `output.pdf` with the desired output file name:

```sh
pandoc input.md -o output.pdf
```

### Additional Options

`pandoc` supports a wide range of options. Here are a few useful ones:
- **Template:** Use a custom LaTeX template:
  ```sh
  pandoc input.md -o output.pdf --template=mytemplate.tex
  ```
- **Metadata:** Set title, author, and date metadata:
  ```sh
  pandoc input.md -o output.pdf --metadata title="Document Title" --metadata author="Author Name" --metadata date="2023-10-01"
  ```
- **Table of Contents:** Include a table of contents:
  ```sh
  pandoc input.md -o output.pdf --toc
  ```

### Example

Here's a full example command that sets the title, author, and includes a table of contents:

```sh
pandoc input.md -o output.pdf --metadata title="My Document" --metadata author="John Doe" --toc
```

### Verifying Installation

To verify that `pandoc` was installed correctly, you can check the version:

```sh
pandoc --version
```

And for the LaTeX engine, e.g., `pdflatex`:

```sh
pdflatex --version
```

That's it! You should now be able to convert Markdown files to PDF using the macOS Terminal.

### shortcut in vscode to switch between the terminal and editor

In Visual Studio Code (VSCode), you can quickly switch between the terminal and the editor using keyboard shortcuts. Here are the default shortcuts to manage this:

1. **Toggle Terminal**
   - **Command + `** (backtick, the key below the Esc key on most keyboards)
   - This shortcut toggles the visibility of the integrated terminal. If the terminal is not currently focused, it will open and focus it. If it is already focused, it will hide it.

2. **Focus Terminal**
   - **Ctrl + `** (backtick)
   - This focuses the terminal without toggling its visibility.

3. **Focus Active Editor**
   - **Command + 1** (or **Ctrl + 1** on Windows/Linux)
   - This shortcut focuses the first editor group. Generally, it's used to switch back to the editor if you're currently focused on the terminal or another part of the VSCode interface.

4. **Toggle Panel (including Terminal)**
   - **Command + J** (on macOS)
   - **Ctrl + J** (on Windows/Linux)
   - This toggles the visibility of the entire panel area, which includes the terminal, output, problems, etc.

### Customizing Shortcuts

If you want to customize these shortcuts or assign new ones, you can do it through the Keyboard Shortcuts menu:

1. Press **Command + K, Command + S** (or **Ctrl + K, Ctrl + S** on Windows/Linux) to open the Keyboard Shortcuts overview.
2. Use the search bar at the top to find the command you want to customize (e.g., "Focus Terminal", "Focus Active Editor").
3. Click the pencil icon next to the command to re-assign the shortcut.

### Example for Customizing Focus Terminal

- Open Keyboard Shortcuts with **Command + K, Command + S**.
- Search for `workbench.action.terminal.focus`.
- Click on the pencil icon to the left of the command and assign a new keybinding.

This customization allows you to set up VSCode to match your working style and make switching between the terminal and editor even faster.