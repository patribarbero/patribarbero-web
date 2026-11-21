"""Versión en inglés: traduce las páginas ya generadas en español.
- Rutas en inglés bajo /en/.
- Traduce nodos de texto y algunos atributos con el diccionario de en_dict.py.
- Lista lo que falte por traducir (para no publicar nada a medias)."""
import re, html as H
from en_dict import T, PATHS, KEEP

ATTRS = ('alt', 'placeholder', 'aria-label', 'data-msg', 'title', 'content', 'data-label', 'data-title', 'data-phrase', 'data-unit')
SPANISH = re.compile(r'[áéíóúñ¿¡]|\b(de|la|el|que|y|en|para|con|mis|tus|cómo|qué)\b', re.I)

def en_path(p):
    base, q = (p.split('?', 1) + [''])[:2]
    base, frag = (base.split('#', 1) + [''])[:2]
    if base in PATHS: base = PATHS[base]
    return base + ('?' + q if q else '') + ('#' + frag if frag else '')

def tr(txt, missing):
    k = ' '.join(txt.split())
    if not k: return txt
    if k in T:
        lead = txt[:len(txt) - len(txt.lstrip())]; trail = txt[len(txt.rstrip()):]
        return lead + T[k] + trail
    if re.search(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]{2}', k) and k not in KEEP and not k.startswith('http'): missing.add(k)
    return txt

def translate(html, missing):
    # partes que no se tocan: scripts, svg, style
    parts = re.split(r'(<script\b.*?</script>|<svg\b.*?</svg>|<style\b.*?</style>)', html, flags=re.S)
    out = []
    for i, part in enumerate(parts):
        if i % 2: out.append(part); continue
        def tag(m):
            t = m.group(0)
            t = re.sub(r'\b(href)="(/[^"]*)"', lambda a: f'{a.group(1)}="{en_path(a.group(2))}"', t)
            for at in ATTRS:
                t = re.sub(r'(\s' + at + r')="([^"]*)"', lambda a: f'{a.group(1)}="{H.escape(tr(H.unescape(a.group(2)), missing), quote=True)}"', t)
            return t
        part = re.sub(r'<[a-zA-Z][^>]*>', tag, part)
        part = re.sub(r'(?:(?<=>)|^)([^<>]+)(?=<|$)', lambda m: tr(m.group(1), missing), part)
        out.append(part)
    return ''.join(out)

LANG = '<a class="lang" href="@@LANG@@">EN</a>'

def build(pages, R):
    missing = set()
    for path, html in pages:
        if path == '/404.html': continue
        ep = PATHS.get(path)
        if not ep: continue
        h = translate(html, missing)
        h = h.replace('<html lang="es"', '<html lang="en"').replace('content="es_ES"', 'content="en_GB"')
        h = h.replace(f'https://patribarbero.com{path}"', f'https://patribarbero.com{ep}"')
        alt = f'<link rel="alternate" hreflang="es" href="https://patribarbero.com{path}"><link rel="alternate" hreflang="en" href="https://patribarbero.com{ep}"><link rel="alternate" hreflang="x-default" href="https://patribarbero.com{path}">'
        h = h.replace('</head>', alt + '\n</head>', 1)
        h = h.replace(LANG, f'<a class="lang" hreflang="es" lang="es" href="{path}" aria-label="Ver en español"><svg class="flag" viewBox="0 0 750 500" aria-hidden="true"><path fill="#AA151B" d="M0 0h750v500H0z"/><path fill="#F1BF00" d="M0 125h750v250H0z"/></svg>ES</a>')
        f = R / ep.strip('/') / 'index.html'
        f.parent.mkdir(parents=True, exist_ok=True); f.write_text(h)
        # español: hreflang + selector hacia el inglés
        fes = R / 'index.html' if path == '/' else R / path.strip('/') / 'index.html'
        s = fes.read_text().replace('</head>', alt + '\n</head>', 1).replace(LANG, f'<a class="lang" hreflang="en" lang="en" href="{ep}" aria-label="English version"><svg class="flag" viewBox="0 0 60 30" aria-hidden="true"><clipPath id="gbc"><path d="M0 0v30h60V0z"/></clipPath><clipPath id="gbt"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#gbc)"><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#gbt)" stroke="#C8102E" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>EN</a>')
        fes.write_text(s)
    for f in R.rglob('*.html'):
        t = f.read_text()
        if LANG in t: f.write_text(t.replace(LANG, '<a class="lang" hreflang="en" lang="en" href="/en/" aria-label="English version"><svg class="flag" viewBox="0 0 60 30" aria-hidden="true"><clipPath id="gbc"><path d="M0 0v30h60V0z"/></clipPath><clipPath id="gbt"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#gbc)"><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#gbt)" stroke="#C8102E" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>EN</a>'))
    if missing:
        print('SIN TRADUCIR:', len(missing))
        for m in sorted(missing): print('  ', repr(m))
