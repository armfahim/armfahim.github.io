# Connecting `armfahim.com` (Cloudflare → GitHub Pages)

A step-by-step guide to put your portfolio on your own domain with free HTTPS.
Follow the steps **in order**. Do **not** add a `CNAME` file to the repo manually —
Step 4 does it for you at the right time, which avoids breaking the
`armfahim.github.io` URL in the meantime.

> **Canonical setup:** `armfahim.com` is the primary address (apex domain).
> `www.armfahim.com` will automatically redirect to it.

---

## Step 0 — Prerequisite

Your site must already be live at **https://armfahim.github.io** (the normal deploy).
Confirm that works first, then continue.

---

## Step 1 — Register the domain on Cloudflare

1. Sign in at <https://dash.cloudflare.com> (create a free account if needed).
2. Go to **Domain Registration → Register Domains**.
3. Search **`armfahim.com`**, add it to cart, and complete registration.
   - Cloudflare Registrar charges wholesale price (no markup) and includes
     free WHOIS privacy.
4. Registering automatically creates a **DNS zone** for `armfahim.com` in your account.

---

## Step 2 — Add the DNS records

Open **`armfahim.com` → DNS → Records** and add the following.

**Set every record's proxy status to “DNS only” (grey cloud, not orange).**
GitHub Pages issues its own SSL certificate, and that validation needs the
records unproxied. (See the note at the bottom if you specifically want
Cloudflare’s proxy/CDN.)

### Apex (`armfahim.com`) — four A records

| Type | Name | Value (IPv4)      | Proxy    |
|------|------|-------------------|----------|
| A    | `@`  | `185.199.108.153` | DNS only |
| A    | `@`  | `185.199.109.153` | DNS only |
| A    | `@`  | `185.199.110.153` | DNS only |
| A    | `@`  | `185.199.111.153` | DNS only |

### Apex — four AAAA records (IPv6, recommended)

| Type | Name | Value (IPv6)          | Proxy    |
|------|------|-----------------------|----------|
| AAAA | `@`  | `2606:50c0:8000::153` | DNS only |
| AAAA | `@`  | `2606:50c0:8001::153` | DNS only |
| AAAA | `@`  | `2606:50c0:8002::153` | DNS only |
| AAAA | `@`  | `2606:50c0:8003::153` | DNS only |

### `www` subdomain — one CNAME

| Type  | Name  | Value                 | Proxy    |
|-------|-------|-----------------------|----------|
| CNAME | `www` | `armfahim.github.io`  | DNS only |

Save. DNS usually propagates within minutes on Cloudflare.

---

## Step 3 — (Optional) verify the domain in GitHub

Prevents anyone else from ever claiming your domain on their GitHub account.
GitHub → **Settings → Pages → “Verify a domain”** (account-level) and follow the
TXT-record prompt. Optional but nice; you can skip and still proceed.

---

## Step 4 — Point GitHub Pages at the domain

1. Go to your repo → **Settings → Pages**.
2. Under **Custom domain**, type **`armfahim.com`** and click **Save**.
   - This automatically commits a `CNAME` file to the repo — that’s expected.
3. GitHub runs a **DNS check**. Wait for the green check ✓
   (usually minutes; can take up to 24h).
4. Once checked, tick **Enforce HTTPS**.
   - The TLS certificate is provisioned automatically by GitHub (Let’s Encrypt).
     If the box is greyed out, wait a bit and refresh — the cert is still being issued.

Done. Visiting **https://armfahim.com** now serves your portfolio, `www` redirects
to it, and `armfahim.github.io` redirects to `armfahim.com`.

---

## Step 5 — Switch the site’s URLs to the new domain (optional, after it’s live)

Once `https://armfahim.com` is confirmed working, tell Claude (or do it yourself)
to update the canonical URL in these spots so search engines and share previews
use the real domain:

- `index.html` — `og:url` / any canonical link, and the footer
- `tools/make_cv.py` — the contact line + footer (`armfahim.github.io` → `armfahim.com`),
  then re-run `python tools/make_cv.py`
- `README.md` — the live link

Keeping `armfahim.github.io` also works indefinitely (it just redirects), so this
step is purely cosmetic.

---

## Troubleshooting

- **Site shows “404” or a redirect loop right after Step 4** — DNS or the cert
  hasn’t finished. Wait and refresh; give it up to a few hours.
- **HTTPS box is greyed out** — the certificate is still being issued. Come back later.
- **You added the records as “proxied” (orange cloud)** — either switch them to
  **DNS only**, or go to **SSL/TLS → Overview** and set the mode to **Full**
  (never “Flexible” — that causes infinite redirects with GitHub Pages).
- **Changed your mind / want to remove the domain** — clear the Custom domain field
  in Settings → Pages and delete the `CNAME` file; the site returns to
  `armfahim.github.io`.

---

### Quick reference — GitHub Pages apex IPs

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
AAAA  @   2606:50c0:8000::153
AAAA  @   2606:50c0:8001::153
AAAA  @   2606:50c0:8002::153
AAAA  @   2606:50c0:8003::153
CNAME www armfahim.github.io
```
