# A.R.M. Fahim — Portfolio

Personal portfolio website for **A.R.M. Fahim**, Software Engineer (Java · Spring Boot).

🔗 **Live:** https://armfahim.github.io

## Built with

- Plain HTML, CSS, and vanilla JavaScript — no build step, no dependencies
- Modern dark theme with a persisted light-mode toggle
- Fully responsive, accessible, and fast
- Hosted for free on **GitHub Pages**

## Structure

```
.
├── index.html          # Page content
├── css/style.css       # Styles & theming
├── js/main.js          # Interactions (theme, reveal, typewriter, nav)
├── assets/             # Static files, incl. the generated CV PDF
└── tools/make_cv.py    # Regenerates the downloadable CV (see below)
```

## Local preview

Just open `index.html` in a browser, or serve the folder:


Then visit http://localhost:8000

## Updating the CV

The privacy-cleaned CV (`assets/A.R.M.-Fahim-CV.pdf`) — email, LinkedIn, and city
only; no phone, address, or references' contacts — is generated from a script.
Edit the content in `tools/make_cv.py`, then regenerate:

```bash
pip install -r tools/requirements.txt
python tools/make_cv.py
```

It writes straight into `assets/`, so just commit the updated PDF afterwards.

## Deploy (GitHub Pages)

This repo is named `armfahim.github.io`, so pushing to the `main` branch
publishes automatically at https://armfahim.github.io. In the repo:
**Settings → Pages → Source: Deploy from a branch → `main` / `root`.**
