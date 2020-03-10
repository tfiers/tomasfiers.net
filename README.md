About
-----

Source for my personal website, [tomasfiers.net](https://tomasfiers.net).

- It uses [Hugo](https://gohugo.io/) as a static site generator; i.e. to convert Markdown files to HTML.
- The theme is [Hyde](https://themes.gohugo.io/hyde/)
- The site is auto-built and hosted by [Netlify](https://www.netlify.com/)

Many thanks to all three!


Deployment
----------

The site is auto-published on each commit to GitHub.  
> Deploy/build status: [![Netlify Status](https://api.netlify.com/api/v1/badges/cca080cc-e1f3-4785-ae25-b3ac42521276/deploy-status)](https://app.netlify.com/sites/tomasfiers/deploys)

Text-only changes can therefore be made simply on GitHub.

For other development (layout eg), see the next section.


Local development
-----------------

Clone with
```
git clone --recursive
```
to make sure the required [submodules](.gitmodules) are also downloaded.
<br>
<br>

[Install](https://gohugo.io/getting-started/installing/)
the Hugo version specified in [`netlify.toml`](netlify.toml).  
> Example, using the [Chocolatey package manager](https://chocolatey.org/install)
on Windows:
> ```
> choco install hugo --version 0.42 --yes
> ```
<br>
<br>

👉 To launch a local server with live-reloading:
```bash
hugo server
```
This command keeps the built site in memory.

When working on layout, use
```
hugo server --disableFastRender
```
<br>
<br>

To build to disk:
```
hugo
```
