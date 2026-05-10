Feb 12, 2021

# Creating a shortcut in vscode to switch between the terminal and editor

## Overview

I spend a lot of time in `vscode` swapping between the editor and terminal windows. To streamline the workflow and keep my hands from leaving the keyboard, I created the shortcut `ctrl + ;` to swap between the two windows.

![Image of vscode session with editor and terminal windows open](https://jasonmurray.org/images/2021-02-12-12-43-16.png)

## Details

Open the keyboard shortcuts settings:

![Image of vscode keyboard shortcut settings menu](https://jasonmurray.org/images/2021-02-12-12-26-03.png)

First, search for `Terminal: Focus on Terminal View`.

Change the setting by `right clicking` the keyboard shortcut. Then change the `Keybinding` to `ctrl + ;` and change `When` to `!terminalFocus`:

![Image of vscode keyboard shortcut settings](https://jasonmurray.org/images/2021-02-12-12-27-29.png)

Next, search for `View: Focus Active Editor Group`.

Change the setting by `right clicking` the keyboard shortcut. Then change the `Keybinding` to `ctrl + ;` and change `When` to `terminalFocus`:

Note: `vscode` may not let you change the `Keybinding` to the same shortcut as above. To resolve this issue, change the keybinding to `ctrl + =`, then change the `When` statement to `terminalFocus`. Now go back and change the `Keybinding` to `ctrl + ;`.

![Image of vscode keyboard shortcut settings](https://jasonmurray.org/images/2021-02-12-12-28-22.png)

Both commands will look like this when finished:

![Image of vscode keyboard shortcut settings](https://jasonmurray.org/images/2021-02-12-12-15-36.png)

Press `ctrl + ;` to toggle between the current editor window and the current terminal session.

------

[vscode](https://jasonmurray.org/tags/vscode)[terminal](https://jasonmurray.org/tags/terminal)[editor](https://jasonmurray.org/tags/editor)

175 Words

2021-02-12 12:15 -0600

[ NEWER
Simulating production networks with Cisco Modeling Lab: Install Guide](https://jasonmurray.org/posts/2021/cml/)[OLDER 
Caution: MAC address information leaked when booting Tails Linux on a MacBook Pro (not Tails fault)](https://jasonmurray.org/posts/2021/tailsleak/)

© 2024 [Jason Murray](https://jasonmurray.org/) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

Made with [Hugo](https://gohugo.io/) · Theme [Hermit](https://github.com/Track3/hermit) · 

