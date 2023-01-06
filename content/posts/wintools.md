---
title: "Windows Tools"
date: 2023-01-06T12:00:00+02:00
---

This is a running collection of tools I use to make Windows good.


### AutoHotkey + SharpKeys
→ **Arrow keys etc w/o moving hands** (a bit vim-like; but in any app)

See [Many but finite's 'Home Row Computing'](https://manybutfinite.com/post/home-row-computing/)


### WinCompose
→ **Keyboard shortcuts for special characters** (Greek letters, math symbols, arrows, accents, ..)

- [wincompose.info](http://wincompose.info/) | [github](https://github.com/samhocevar/wincompose)
- tray app, C#, active development
- Kinda wonky UI, but works
- Supports the [.XCompose] format from the linux world.
  - [My `.XCompose` file](https://github.com/tfiers/dotfiles/blob/main/.XCompose)
- Big advantage over e.g. Julia's great `\alpha<tab>`-completion
  (see first "Julia likes" slide [here](/posts/julia-for-scientists)):
  available in every text field in every app.

<!--
Hugo syntax for is {{< ref "julia-for-scientists" >}}
(https://gohugo.io/content-management/cross-references).
But that doesn't even insert a link.
-->

[.XCompose]: https://wiki.debian.org/XCompose


### Beeftext
→ **text snippets**

- [beeftext.org](https://beeftext.org) | [github](https://github.com/xmichelo/Beeftex)
- tray app, C++, modern GUI (Qt5), active development
- Great UX

What I use it for (i.e. things I'm tired of typing over and over)
- To make images less huge on github: `<img width=400 src="…">`


### PasteIntoFile
→ **Paste images on the clipboard in Explorer** without having to go through Paint

- [github:eltos](https://github.com/eltos/PasteIntoFile)
- tray app, C#, active development
- [Long history](https://github.com/eltos/PasteIntoFile/issues/15).
  eltos's fork is the most advanced version.

PowerPoint is one of the best tools for vector graphic design, weirdly/sadly.
To use diagrams made in PPT in LaTeX, I copy a diagram from PPT and paste it as an svg files using this great tool.



### ExplorerPatcher
→ **Get back Win10 taskbar & context menu in Win11**

- [github](https://github.com/valinet/ExplorerPatcher)
- C, active development
- accessed by right-clicking taskbar > 'Properties'


### Misc

- [Windows Terminal](https://github.com/microsoft/terminal#readme)
- [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/)
  - More and more dev tools have a good UX on Windows.
    But most still suck, even if they technically support Windows.
    WSL, especially in combination with VS Code remote dev, works well then.
- [Windows PowerTools](https://learn.microsoft.com/en-us/windows/powertoys/)
  - Open source, active dev. Well done Microsoft.
