---
title: "Windows power user Tools"
date: 2023-01-06T12:00:00+02:00
---

This is a running collection of tools I use to make Windows good.


### [AutoHotkey] + [SharpKeys]
→ **See [Many but finite's 'Home Row Computing'](https://manybutfinite.com/post/home-row-computing/)**

Allows me to type arrow keys & backspace without having to
move my hands away from the 'home row' on the keyboard (`asdf`, `jkl;`)\
I.e. like vim; but in any textfield, in any app.

[AutoHotkey]: https://www.autohotkey.com/
[SharpKeys]: http://www.randyrants.com/category/sharpkeys/


### [WinCompose]
→ **Keyboard shortcuts for special characters** (Greek letters, math symbols, arrows, accents, ..)

- tray app, C#, [active development](https://github.com/samhocevar/wincompose)
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

[WinCompose]: http://wincompose.info
[.XCompose]: https://wiki.debian.org/XCompose


### [Beeftext]
→ **Text snippets (auto-replace shortcodes)**

- tray app, C++, modern GUI (Qt5), [active development](https://github.com/xmichelo/Beeftext)
- Great UX

What I use it for (i.e. things I'm tired of typing over and over)
- To make images less huge on github: `<img width=400 src="…">`

[Beeftext]: https://beeftext.org


### [PasteIntoFile]
→ **Paste images on the clipboard in Explorer** (without having to go through Paint)

- tray app, C#, active development
- [Long history](https://github.com/eltos/PasteIntoFile/issues/15).
  eltos's fork (the one linked here) is the most advanced version.

PowerPoint is one of the best tools for vector graphic design, weirdly/sadly.
To use diagrams made in PPT in LaTeX, I copy a diagram from PPT and paste it as an svg files using this great tool.

[PasteIntoFile]: https://github.com/eltos/PasteIntoFile


### [ExplorerPatcher]
→ **Get the Win10 taskbar & context menu back in Windows 11**

- C, active development
- accessed by right-clicking taskbar > 'Properties'

[ExplorerPatcher]: https://github.com/valinet/ExplorerPatcher


### Misc

- [Windows Terminal](https://github.com/microsoft/terminal#readme)
- [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/)
  - More and more dev tools have a good UX on Windows.
    But most still suck, even if they technically support Windows.
    WSL, especially in combination with VS Code remote dev, works well then.
- [Microsoft PowerToys](https://learn.microsoft.com/en-us/windows/powertoys/)
  - Open source, active dev. Well done Microsoft.
