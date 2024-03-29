---
title: "Tools for Windows"
date: 2023-01-06T12:00:00+02:00
---

This is a running collection of tools I use to make Windows good.



### [AutoHotkey] + [SharpKeys]
→ **See [_Many but finite_'s 'Home Row Computing'](https://manybutfinite.com/post/home-row-computing/)**

Allows me to type arrow keys, backspace, `Delete`, `Home`, `End`, etc without having to
move my hands away from the 'home row' of the keyboard (`asdf`, `jkl;`)\
I.e. like vim; but available in any text field in any app.

In general, AutoHotkey enables [end-user programming] of the Windows GUI,
through a (slightly quirky) scripting language.

The functionality of many of the apps below can be implemented with AutoHotkey instead;
but dedicated config GUIs (plus collaborative open-source dev) makes the apps worth it.

[AutoHotkey]: https://www.autohotkey.com/
[SharpKeys]: http://www.randyrants.com/category/sharpkeys/
[end-user programming]: https://www.inkandswitch.com/end-user-programming/



### [WinCompose]
→ **Keyboard shortcuts for special characters** (Greek letters, math symbols, arrows, accents, ..)

→ See [my `.XCompose` file](https://github.com/tfiers/dotfiles/blob/main/.XCompose)

- tray app, C#, [active development](https://github.com/samhocevar/wincompose)
- Kinda wonky UI, but works
- Supports the [.XCompose] file format from the linux world.
- The big advantage over e.g. [Julia's] great `\alpha<tab>`-completion
  (see also the first "Julia likes" slide [here](/posts/julia-for-scientists)):
  this is available in every text field in every app.

<!--
Hugo syntax for is {{< ref "julia-for-scientists" >}}
(https://gohugo.io/content-management/cross-references).
But that doesn't even insert a link.
-->

[Julia's]: https://docs.julialang.org/en/v1/stdlib/REPL/#Tab-completion
[WinCompose]: http://wincompose.info
[.XCompose]: https://wiki.debian.org/XCompose



### [Beeftext]
→ **Text snippets** (auto-replace shortcodes with oft-typed text)

- tray app, C++, modern GUI (Qt5), [active development](https://github.com/xmichelo/Beeftext)
- Great UX

What I use it for (i.e. things I'm tired of typing over and over):

- To make images less huge on github: `<img width=400 src="…">`

[Beeftext]: https://beeftext.org



### [PasteIntoFile]
→ **Paste images on the clipboard directly as files in Windows Explorer** (without having to go through Paint)

- tray app, C#, active development
- [Long history](https://github.com/eltos/PasteIntoFile/issues/15).
  eltos's fork (the one linked here) is the most advanced version.

PowerPoint is one of the best tools for vector graphic design, weirdly/sadly.
To use diagrams made in PPT in LaTeX, I copy a diagram from PPT and paste it as an svg files using this great tool.

[PasteIntoFile]: https://github.com/eltos/PasteIntoFile



### [ExplorerPatcher]
→ **Get the old taskbar & context menu back in Windows 11**

- C, active development
- accessed by right-clicking taskbar > 'Properties'

[ExplorerPatcher]: https://github.com/valinet/ExplorerPatcher



### Microsoft-supported tools

All are open-source and under active development.

- [Microsoft PowerToys](https://learn.microsoft.com/en-us/windows/powertoys/)
- [Windows Terminal](https://github.com/microsoft/terminal#readme)
- [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/)
  - More and more dev tools have a good UX on Windows.
    But for a lot of them, Windows development is still painful, even if they nominally/technically support it.
    WSL, especially in combination with VS Code remote dev, is a good solution then.
- [VS Code](https://code.visualstudio.com)
- Do not use: PowerAutomate (bad UX).
