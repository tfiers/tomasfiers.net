About
-----

Source for my personal website, [tomasfiers.net](https://tomasfiers.net).

- It uses [Hugo](https://gohugo.io/) as a static site generator; i.e. to convert Markdown files to HTML.
- The theme is [Hyde](https://themes.gohugo.io/hyde/)
- The site is auto-built and hosted by [Netlify](https://www.netlify.com/)

Many thanks to all three!


Setup local development
-----------------------

```
git clone --recursive git@github.com:tfiers/tomasfiers.net.git
```
The `--recursive` flag is necessary to also download required submodules
(which are listed in [`.gitmodules`](.gitmodules)).

[Install](https://gohugo.io/getting-started/installing/)
the Hugo version specified in [`netlify.toml`](netlify.toml).

E.g. using the [Chocolatey package manager](https://chocolatey.org/install)
on Windows:
```
choco install hugo --version 0.42 --yes
```


Build
-----

To launch a local server with live-reloading:
```bash
hugo server
```
This command keeps the built site in memory.

To build to disk:
```
hugo
```


Publish
-------

Auto-published on each commit to GitHub.

[🚀 Check deployment status](https://app.netlify.com/sites/tomasfiers/overview).
