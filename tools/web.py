#!/usr/bin/env python3
"""Genera la web de Patri Barbero (RIBETE 1.3, multipágina). Ejecutar: python3 tools/web.py
Cada página tiene URL propia, SEO propio y comparte cabecera, pie, estilos y scripts."""
import pathlib, re, subprocess, shutil, html as H
R = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://patribarbero.com'
_main = subprocess.run(['git', '-C', str(R), 'show', 'origin/main:index.html'], capture_output=True, text=True).stdout
EMAIL = re.search(r'mailto:([^"?]+)', _main).group(1)
SPRITE = re.search(r'<svg width="0".*?</svg>', _main, re.S).group(0)
V = '20261122b'  # versión de los archivos (para que el navegador no use copias viejas)

ARR = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4.5L12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLAY = '<span class="pl" aria-hidden="true"><svg viewBox="0 0 10 12"><path fill="currentColor" d="M0 0l10 6-10 6z"/></svg></span>'
YT, IG, TT = 'https://www.youtube.com/@patribarbero', 'https://www.instagram.com/patribarbero_/', 'https://www.tiktok.com/@patribarbero_'
SERV = [('/colaboraciones/', 'Colabora en mis redes', 'Tu marca en mis vídeos de YouTube, Reels y TikTok', 'colab'),
        ('/ugc/', 'Contenido UGC', 'Vídeos para las redes y anuncios de tu marca', 'ugc'),
        ('/gestion-de-redes/', 'Gestión de redes', 'Llevo las redes de tu negocio', 'redes')]

def nav(key):
    def a(h, t, k): return f'<li><a href="{h}"' + (' aria-current="page"' if k == key else '') + f'>{t}</a></li>'
    sub = ''.join(f'<li><a href="{h}"' + (' aria-current="page"' if k == key else '') + f'><b>{t}</b><small>{d}</small></a></li>' for h, t, d, k in SERV)
    cur = ' cur' if key in ('colab', 'ugc', 'redes', 'trabaja') else ''
    return ('<li class="m-only"><a href="/"' + (' aria-current="page"' if key == 'home' else '') + '>Inicio</a></li>'
            + a('/contenido/', 'Contenido', 'cont') + a('/estadisticas/', 'Estadísticas', 'stats')
            + f'<li><button class="dd{cur}" type="button" aria-expanded="false" aria-controls="sub">Trabaja conmigo<span aria-hidden="true"></span></button>'
            + f'<ul class="sub" id="sub">{sub}<li><a class="all" href="/trabaja-conmigo/"' + (' aria-current="page"' if key == 'trabaja' else '') + '>Ver las tres opciones</a></li></ul></li>'
            + a('/sobre-mi/', 'Sobre mí', 'sobre')
            + '<li class="m-only"><a href="/contacto/"' + (' aria-current="page"' if key == 'contacto' else '') + '>Contacto</a></li>')

PAGES = []
def page(path, key, title, desc, body, scripts='', noindex=False, preload_img=''):
    rob = '<meta name="robots" content="noindex">' if noindex else ''
    pre = f'<link rel="preload" as="image" href="{preload_img}" fetchpriority="high">' if preload_img else ''
    out = f'''<!doctype html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="only light"><meta name="supported-color-schemes" content="light">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">{rob}
<meta property="og:type" content="website"><meta property="og:site_name" content="Patri Barbero"><meta name="application-name" content="Patri Barbero"><meta name="apple-mobile-web-app-title" content="Patri Barbero"><meta property="og:locale" content="es_ES">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg?v=r13" type="image/svg+xml"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#FFF5F1">
<link rel="preload" href="/assets/f/anton.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/f/rubik.woff2" as="font" type="font/woff2" crossorigin>{pre}
<link rel="stylesheet" href="/assets/css/site.css?v={V}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"Patri Barbero","alternateName":"patribarbero.com","url":"https://patribarbero.com/"}}</script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
{SPRITE}
<header class="top"><div class="wrap bar">
  <a class="logo" href="/" aria-label="Patri Barbero, inicio">Patri <span>Barbero</span></a>
  <button class="menu" type="button" aria-expanded="false" aria-controls="links">Menú</button>
  <ul class="links" id="links">{nav(key)}</ul>
  <a class="lang" href="@@LANG@@">EN</a>
  <a class="btn p" href="/contacto/">Contacto</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div><a class="logo" href="/">Patri <span>Barbero</span></a><p>Moda como identidad · Madrid<br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <nav aria-label="Pie"><a href="/contenido/">Contenido</a><a href="/estadisticas/">Estadísticas</a><a href="/trabaja-conmigo/">Trabaja conmigo</a><a href="/colaboraciones/">Colabora en mis redes</a><a href="/ugc/">Contenido UGC</a><a href="/gestion-de-redes/">Gestión de redes</a><a href="/sobre-mi/">Sobre mí</a><a href="/contacto/">Contacto</a><a href="{YT}" target="_blank" rel="noopener">YouTube ↗</a></nav>
  <div class="legal"><span>© 2026 Patri Barbero</span><a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{TT}" target="_blank" rel="noopener">TikTok</a></div>
</div></footer>
<dialog class="vd" id="vd" aria-label="Vídeo"><div class="box"><div class="frame"></div></div><button class="x" type="button">Cerrar ✕</button></dialog>
<script src="/assets/js/site.js?v={V}" defer></script>
{scripts}
</body>
</html>
'''
    f = R / 'index.html' if path == '/' else (R / path.strip('/') if path.endswith('.html') else R / path.strip('/') / 'index.html')
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(out)
    PAGES.append((path, out))

STATS = f'<script src="/datos.js?v={V}" defer></script><script src="/assets/js/stats.js?v={V}" defer></script>'

def crumbs(*items):
    return '<nav class="crumbs" aria-label="Estás en">' + ' <span aria-hidden="true">›</span> '.join(
        (f'<a href="{h}">{t}</a>' if h else f'<span aria-current="page">{t}</span>') for h, t in items) + '</nav>'

def win(title, inner, cls=''):
    return f'<div class="win {cls}"><div class="win-bar"><i></i><i></i><i></i><b>{title}</b></div><div class="win-rib"></div><div class="win-body">{inner}</div></div>'

PEEK = {'/contenido/': ['yt4.jpg', 'oversized.jpg', 'yt3.jpg'], '/colaboraciones/': ['zBPboLQZKAo.jpg', 'pYXWRYBJd9s.jpg', 'CecPikzWLI8.jpg'],
        '/ugc/': ['broches.jpg', 'abc.jpg', 'oversized.jpg'], '/gestion-de-redes/': ['lun · post', 'mié · reel', 'vie · stories']}
def peek(href):
    items = PEEK.get(href, [])
    return '<div class="peek">' + ''.join((f'<img src="/img/{x}" alt="" loading="lazy">' if x.endswith('.jpg') else '<span class="pk-note">' + x.split(' · ')[0] + '<b>' + x.split(' · ')[1] + '</b></span>') for x in items) + '</div>'
def door(href, pat, title, text, go):
    return f'<a class="door rv" href="{href}"><div class="fold" aria-hidden="true"><div class="tab {pat}"></div><div class="body {pat}"></div>{peek(href)}<div class="flap {pat}"></div></div><h3>{title}</h3><p>{text}</p><span class="go">{go} {ARR}</span></a>'

def vid(yt, img, title, meta='', vertical=False):
    v = ' v' if vertical else ''
    dv = ' data-v="1"' if vertical else ''
    return f'<button class="vid{v}" type="button" data-yt="{yt}"{dv} data-title="{H.escape(title)}"><span class="th"><img src="/img/{img}" alt="" loading="lazy">{PLAY}</span><b>{title}</b>' + (f'<small>{meta}</small>' if meta else '') + '</button>'

def short_card(kind, ref, img, title, meta):
    if kind == 'yt':
        return vid(ref, img, title, meta, True)
    th = f'<img src="/img/{img}" alt="" loading="lazy">' if img else f'<span class="ph-cover vichy"><span class="T">{H.escape(title)}</span></span>'
    return f'<a class="vid v" href="{ref}" target="_blank" rel="noopener"><span class="th">{th}{PLAY}</span><b>{title} <span class="ext">Instagram ↗</span></b><small>{meta}</small></a>'

def band(title_html, text, btns):
    return f'<section class="sec tight"><div class="wrap"><div class="band rv"><div><h2 class="T h2">{title_html}</h2><p>{text}</p></div><div class="ctas" style="margin:0">{btns}</div></div></div></section>'

COLLABS = [('zBPboLQZKAo', 'zBPboLQZKAo.jpg', 'Tips para vestir con estilo en otoño', 'Integración en YouTube · agosto 2025', 'logo_vivaia.svg', 'Vivaia'),
           ('gKLj2hae2ww', 'gKLj2hae2ww.jpg', 'Esto en la moda no es normal', 'Segunda integración en YouTube', 'logo_vivaia.svg', 'Vivaia'),
           ('pYXWRYBJd9s', 'pYXWRYBJd9s.jpg', 'Colorimetría con The Colour Nook', 'Taller contado en vídeo · abril 2026', 'logo_colournook.jpg', 'The Colour Nook'),
           ('CecPikzWLI8', 'CecPikzWLI8.jpg', 'Vlog del evento de lanzamiento', 'Evento · mayo 2024', 'logo_modibodi.svg', 'Modibodi')]
# Ejemplos UGC por sector: (id de YouTube, miniatura, título, etiqueta, clase de etiqueta). Vacío = tarjeta «pídeme muestras»
UGC_EX = [('moda', 'Moda', [(y, i, t, 'Contenido propio', 'own') for y, i, t, m in [('u0GktqmTMh8', 'oversized.jpg', 'Oversized y femenina', ''), ('MKhsAIKXquk', 'broches.jpg', 'Vuelven los broches', ''), ('wu2mG4YX1dI', 'abc.jpg', 'Elige A, B o C', '')]]),
          ('belleza', 'Belleza', []), ('lifestyle', 'Lifestyle', []), ('alimentacion', 'Alimentación', []),
          ('deporte', 'Deporte y fitness', []), ('viajes', 'Viajes', []), ('apps', 'Apps y servicios', [])]
# Los más vistos en vídeo corto (la portada de Nike Shox llega cuando Patri la pase; mientras, tarjeta con el titular)
TOP_SHORTS = [
    ('ig', 'https://www.instagram.com/reel/Df4_yVToCd5/', '', '¿Vuelven las Nike Shox?', 'Reel · 168 mil reproducciones en 2 días'),
    ('yt', 'u0GktqmTMh8', 'oversized.jpg', 'Oversized y femenina', 'Short · 35,7 mil visualizaciones'),
    ('yt', 'MKhsAIKXquk', 'broches.jpg', 'Vuelven los broches', 'Short · 19,8 mil visualizaciones'),
    ('yt', 'wu2mG4YX1dI', 'abc.jpg', 'Elige A, B o C', 'Reel · 13,5 mil reproducciones'),
]
# Tipos de vídeo del canal (listas de YouTube)
TYPES = [('tendencias 🔥', 'Tendencias', 'Qué se lleva esta temporada, por qué aparece y cómo llevarlo cómoda y mona.', 'yt4.jpg'),
         ('outfits fáciles ✨', 'Outfits fáciles', 'Guías para combinar sin pensar mucho: looks de diario, de invierno y sin repetir.', 'yt3.jpg'),
         ('prendas y armario 👗', 'Prendas y armario', 'Una prenda o un calzado a fondo: cuál elegir, con qué y para qué estilo.', 'yt1.jpg'),
         ('moda como identidad 💗', 'Moda como identidad', 'Qué dice de ti lo que te pones y cómo encontrar tu estilo sin seguir reglas.', 'yt2.jpg'),
         ('el lenguaje de los colores 🎨', 'El lenguaje de los colores', 'Qué transmite cada color y cómo combinarlos en tus outfits.', '')]
SHORTS = [('u0GktqmTMh8', 'oversized.jpg', 'Oversized y femenina', 'Short · 35,7 mil visualizaciones'),
          ('MKhsAIKXquk', 'broches.jpg', 'Vuelven los broches', 'Short · 19,8 mil visualizaciones'),
          ('wu2mG4YX1dI', 'abc.jpg', 'Elige A, B o C', 'Reel · formato interactivo')]
LONG = [('yt1.jpg', 'Invierno: ¿qué zapatilla eres?'), ('yt2.jpg', '¿Cuáles? No depende solo de tu cara'), ('yt3.jpg', 'Viste bien en invierno sin repetir looks'), ('yt4.jpg', 'Tendencias de otoño')]

# =================================================== INICIO
home = f'''<section class="home-hero"><div class="wrap hh">
  <div class="hh-txt">
    <div class="hh-id">
    <p class="kicker rv">Creadora de contenido de moda · Madrid</p>
    <h1 class="T h1 rv">Patri<br>Barbero</h1>
    <span class="rib rv" aria-hidden="true"></span>
    </div>
    <div class="hh-more">
    <p class="lead rv">Te enseño a vestirte <span class="hl">sporty sin dejar de sentirte femenina</span>. Tendencias, cómo combinarlas y qué dicen de ti, en YouTube, Instagram y TikTok.</p>
    <div class="ctas rv"><a class="btn p" href="/trabaja-conmigo/">Trabaja conmigo {ARR}</a><a class="btn s" href="/contenido/">Ver mi contenido</a></div>
    <div class="proof rv">
      <a href="/estadisticas/"><b data-n="youtube.suscriptores" data-f="k1">—</b><small>suscriptores en YouTube</small></a>
      <a href="/estadisticas/"><b data-n="youtube.vis" data-f="k1">—</b><small>visualizaciones en 28 días</small></a>
      <a href="/estadisticas/"><b data-n="youtube.audiencia.mujeres" data-f="pct0">—</b><small>de mi audiencia son mujeres</small></a>
    </div>
    </div>
  </div>
  <div class="orb-wrap">
    <div class="orb" data-phrase="Moda como identidad" data-reps="2" data-dur="26" aria-hidden="true">
      <div class="floor"></div>
      <div class="scene back"><div class="tilt"><div class="ring-b"></div></div></div>
      <div class="me-box"><img class="me" src="/img/patri-espejo-1100.webp" srcset="/img/patri-espejo-1100.webp 432w, /img/patri-espejo-1800.webp 708w" sizes="(max-width:860px) 30vw, 340px" alt="" width="708" height="1800" fetchpriority="high">
      </div>
      <div class="scene front"><div class="tilt"><div class="ring-f"></div></div></div>
      <div class="me-box sels">
        <div class="sel" style="--x:5.5%;--y:53%;--w:48%;--h:20%"><i></i><span class="sel-chip">bolso bowling · el toque sporty</span></div>
        <div class="sel" style="--x:19.5%;--y:44.3%;--w:53.5%;--h:6.8%"><i></i><span class="sel-chip">cinturón rojo · une el look</span></div>
      </div>
    </div>
    <p class="sr">Moda como identidad. Patri frente al espejo con top blanco, pantalón negro y bolso rojo.</p>
    <button class="orb-pause" type="button" aria-pressed="false">❚❚ Pausar</button>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Empieza por aquí</p><h2 class="T h2 rv">¿Qué buscas?</h2></div><p class="lead rv">Elige una carpeta. Cada una te lleva a su página.</p></div>
  <div class="doors">
    {door('/contenido/', 'rayas', 'Ver mi contenido', 'Vídeos de YouTube, Reels y TikTok sobre moda sporty y femenina.', 'Abrir')}
    {door('/colaboraciones/', 'vichy', 'Colabora en mis redes', 'Tu marca dentro de mis vídeos, contada como parte de mi día a día.', 'Abrir')}
    {door('/ugc/', 'lunares', 'Contenido UGC', 'Vídeos para las redes y los anuncios de tu marca.', 'Abrir')}
    {door('/gestion-de-redes/', 'mante', 'Gestión de redes', 'Estrategia, contenido y publicación para tu negocio.', 'Abrir')}
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">YouTube · vídeo largo cada domingo</p><h2 class="T h2 rv">En el canal</h2></div><p class="lead rv">Mis vídeos de YouTube: tendencias pasadas por mi filtro y guías para combinar.</p></div>
  <div class="rv">{win('youtube · patri barbero', '<div class="grid4">' + ''.join(f'<a class="vid" href="{YT}" target="_blank" rel="noopener"><span class="th"><img src="/img/{img}" alt="" loading="lazy">{PLAY}</span><b>{t}</b></a>' for img, t in LONG) + f'</div><p style="margin-top:22px"><a class="btn d" href="{YT}" target="_blank" rel="noopener">Ir al canal de YouTube ↗</a></p>')}</div>
</div></section>

{band('¿Tienes una <em>marca</em>?', 'Colaboraciones en mis redes, contenido UGC para tus canales o gestión de tus redes. Elige lo que necesitas.', f'<a class="btn p" href="/trabaja-conmigo/">Trabaja conmigo {ARR}</a><a class="btn s" href="/estadisticas/">Ver estadísticas</a>')}
'''
page('/', 'home', 'Patri Barbero · Moda sporty y femenina en YouTube, Instagram y TikTok',
     'Creadora de contenido de moda: te enseño a vestirte sporty sin dejar de sentirte femenina. Colaboraciones con marcas, contenido UGC y gestión de redes.',
     home, STATS + f'<script src="/assets/js/orbital.js?v={V}" defer></script>', preload_img='/img/patri-espejo-1100.webp')

# =================================================== CONTENIDO
cont = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('', 'Contenido'))}
  <div class="ph-grid"><div><h1 class="T h1 rv">Mi contenido</h1><p class="lead rv">Hablo de moda para chicas que viven en zapatillas y también quieren ir monas. Cada tendencia pasa por el mismo filtro: <span class="hl">cómoda y femenina a la vez</span>.</p>
    <div class="ctas rv"><a class="btn d" href="{YT}" target="_blank" rel="noopener">YouTube ↗</a><a class="btn s" href="{IG}" target="_blank" rel="noopener">Instagram ↗</a><a class="btn s" href="{TT}" target="_blank" rel="noopener">TikTok ↗</a></div></div>
    <div class="rv"><div class="chips" style="gap:10px"><span class="chip"><i></i>Tendencias con filtro</span><span class="chip"><i></i>Cómo combinar</span><span class="chip"><i></i>Identidad y comunidad</span></div><div class="chips" style="gap:10px;margin-top:10px"><span class="chip on">YouTube · vídeo largo cada domingo</span><span class="chip on">6 vídeos cortos a la semana en Reels, TikTok y Shorts</span></div></div></div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="grid3">
    <article class="feat rv"><p class="kicker" style="margin:0">Pilar 1</p><h2 class="h3">Tendencias pasadas por el filtro</h2><p>Qué se lleva, qué transmite, por qué aparece ahora y cómo llevarlo cómoda y femenina.</p></article>
    <article class="feat rv"><p class="kicker" style="margin:0">Pilar 2</p><h2 class="h3">Cómo combinar</h2><p>Guías prácticas para mezclar lo deportivo con lo femenino, en las dos direcciones.</p></article>
    <article class="feat rv"><p class="kicker" style="margin:0">Pilar 3</p><h2 class="h3">Identidad y comunidad</h2><p>Qué dice de ti cada elección y qué chica construye la mezcla. Vestirse también es construirse.</p></article>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="tabs" role="tablist" aria-label="Plataforma"><button role="tab" aria-selected="true" aria-controls="p-yt" id="t-yt">YouTube</button><button role="tab" aria-selected="false" aria-controls="p-sh" id="t-sh">Reels, TikTok y Shorts</button></div>
  <div id="p-yt" role="tabpanel" aria-labelledby="t-yt">{win('youtube · qué vas a encontrar en el canal', '<p class="muted" style="margin-bottom:20px">Un vídeo largo cada domingo, de 10 a 20 minutos. Estos son los tipos de vídeo que hago:</p><div class="types">' + ''.join(f'<a class="type" href="{YT}/playlists" target="_blank" rel="noopener"><span class="th">' + (f'<img src="/img/{img}" alt="" loading="lazy">' if img else '<span class="sw" aria-hidden="true"><i style="background:var(--fr)"></i><i style="background:var(--co)"></i><i style="background:var(--ma)"></i><i style="background:var(--ch)"></i></span>') + f'</span><span class="chip">{lst}</span><b>{t}</b><small>{d}</small></a>' for lst, t, d, img in TYPES) + f'</div><p style="margin-top:22px"><a class="btn d" href="{YT}" target="_blank" rel="noopener">Ver el canal ↗</a></p>')}</div>
  <div id="p-sh" role="tabpanel" aria-labelledby="t-sh" hidden>{win('vídeos cortos · los más vistos', '<div class="grid4 shorts">' + ''.join(short_card(*x) for x in TOP_SHORTS) + '</div><p class="note" style="margin-top:16px">Reproducciones en la plataforma donde se publicó cada uno. Subo los mismos vídeos a Instagram, TikTok y YouTube Shorts.</p>')}</div>
</div></section>

{band('¿Quieres salir en <em>mis vídeos</em>?', 'Integro marcas en mis vídeos como parte de la conversación, no como un anuncio pegado.', f'<a class="btn p" href="/colaboraciones/">Colabora en mis redes {ARR}</a>')}
'''
page('/contenido/', 'cont', 'Mi contenido · Patri Barbero', 'Vídeos de moda sporty y femenina en YouTube, Reels y TikTok: tendencias con filtro, cómo combinar e identidad.', cont)

# =================================================== ESTADÍSTICAS
def kpi(ico, name, big_key, big_f, lbl, rows, src):
    dl = ''.join(f'<div><dt>{a}</dt><dd><span data-n="{k}" data-f="{f}">—</span></dd></div>' for a, k, f in rows)
    return f'<div class="win kpi rv"><div class="win-bar"><i></i><i></i><i></i><b>{name}</b></div><div class="win-rib"></div><div class="win-body"><span class="big" data-n="{big_key}" data-f="{big_f}">—</span><span class="lbl">{lbl}</span><dl>{dl}</dl><p class="src">{src}</p></div></div>'
stats = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('', 'Estadísticas'))}
  <div class="ph-grid"><div><h1 class="T h1 rv">Estadísticas</h1><p class="lead rv">Mi comunidad en datos reales, sacados de los paneles de cada plataforma. Últimos 28 días: <span data-per="periodo.desde|periodo.hasta">—</span>.</p>
    <div class="ctas rv"><span class="upd"><i></i>Actualizado el <span data-date="actualizado">—</span></span><button class="btn s no-print" type="button" data-print>Guardar como PDF</button></div></div>
    <div class="rv"><p class="muted" style="font-size:16px">Contenido en español para una comunidad hispanohablante, sobre todo de España y Latinoamérica, mayoritariamente femenina. Las plataformas no se suman entre sí porque miden cosas distintas.</p></div></div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="kpis">
    {kpi('yt', 'youtube', 'youtube.suscriptores', 'int', 'suscriptores', [('Visualizaciones · 28 días', 'youtube.vis', 'int'), ('Suscriptores nuevos · 28 días', 'youtube.netos', 'int'), ('Clics en miniaturas (vídeos largos)', 'youtube.ctr_largos', 'pct1')], 'YouTube Studio')}
    {kpi('ig', 'instagram', 'instagram.seguidores', 'int', 'seguidores', [('Reproducciones de Reels · 28 días', 'instagram.reproducciones', 'int'), ('Interacción sobre alcance', 'instagram.interaccion', 'pct1'), ('Guardados', 'instagram.guardados', 'int')], 'Datos de Metricool, a la espera de la lectura directa de Instagram')}
    {kpi('tt', 'tiktok', 'tiktok.seguidores', 'int', 'seguidores', [('Vistas · 28 días', 'tiktok.vistas', 'int'), ('Vídeo más visto', 'tiktok.top', 'int'), ('Vídeos publicados', 'tiktok.videos', 'int')], 'Datos de Metricool, a la espera de la lectura directa de TikTok')}
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="star rv"><div class="star-n"><span class="T" data-n="destacado.vistas" data-f="k1">—</span><small>reproducciones</small></div>
    <div><p class="kicker" style="margin:0 0 6px">Reel más visto · Instagram</p><h2 class="h3">«<span data-txt="destacado.titulo">—</span>»</h2><p class="muted">Publicado el <span data-date="destacado.fecha">—</span>. Cifra a las <span data-n="destacado.horas">—</span> horas, medida el <span data-date="destacado.medido">—</span> con Metricool. Es posterior al periodo de 28 días, por eso aún no está en el gráfico de abajo.</p>
    <p style="margin-top:12px"><a href="https://www.instagram.com/reel/Df4_yVToCd5/" target="_blank" rel="noopener" style="color:var(--co);font-weight:600">Ver el Reel en Instagram ↗</a></p></div></div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Quién me ve</p><h2 class="T h2 rv">Audiencia</h2></div><p class="lead rv">Edad, país y género de las personas que ven mi contenido.</p></div>
  <div class="aud">
    <div class="rv">{win('youtube · audiencia', '<p class="subh">Mujeres</p><div class="gbar"><i data-w="youtube.audiencia.mujeres"></i></div><p><b data-n="youtube.audiencia.mujeres" data-f="pct1">—</b> de quienes me ven en YouTube son mujeres</p><div class="a2"><div><h4>Edad</h4><ul class="bars" data-bars="youtube.audiencia.edad" data-hi="25–34"></ul></div><div><h4>Países</h4><ul class="bars" data-bars="youtube.audiencia.paises" data-hi="ES"></ul></div></div><p class="note" style="margin-top:14px">Espectadores con sesión iniciada · <span data-per="youtube.audiencia.desde|youtube.audiencia.hasta">—</span></p>')}</div>
    <div class="rv">{win('instagram · seguidores', '<div class="a2" style="margin-top:0"><div><h4>Edad</h4><ul class="bars" data-bars="instagram.audiencia.edad" data-hi="18–24,25–34"></ul></div><div><h4>Países</h4><ul class="bars" data-bars="instagram.audiencia.paises" data-hi="ES"></ul></div></div><p class="note" style="margin-top:14px">Seguidores · <span data-date="instagram.audiencia.fecha">—</span>. TikTok aún no ofrece estos datos aquí.</p>')}</div>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Rendimiento reciente</p><h2 class="T h2 rv">Vídeo a vídeo</h2></div><p class="lead rv">Cada barra es un vídeo publicado en el periodo. La línea azul marca la mediana; en fresa, los que la duplican.</p></div>
  <div class="aud">
    <div class="rv">{win('youtube shorts', '<div class="cols" data-chart="youtube.shorts_periodo.por_short" data-tip="tip-yt" data-med="med-yt"></div><p class="tip" id="tip-yt" aria-live="polite">Pasa el dedo o el ratón por las barras.</p><p class="legend"><span><i style="background:var(--co)"></i>Mediana: <b id="med-yt">—</b></span><span><i style="background:var(--fr)"></i>Más del doble de la mediana</span></p>')}</div>
    <div class="rv">{win('instagram reels', '<div class="cols" data-chart="instagram.por_reel" data-unit="reproducciones" data-tip="tip-ig" data-med="med-ig"></div><p class="tip" id="tip-ig" aria-live="polite">Pasa el dedo o el ratón por las barras.</p><p class="legend"><span><i style="background:var(--co)"></i>Mediana: <b id="med-ig">—</b></span><span><i style="background:var(--fr)"></i>Más del doble de la mediana</span></p>')}</div>
  </div>
</div></section>

{band('¿Lo vemos <em>juntas</em>?', 'Si estas cifras encajan con tu marca, cuéntame la campaña y te preparo una propuesta.', f'<a class="btn p" href="/colaboraciones/">Colabora en mis redes {ARR}</a><a class="btn s" href="/contacto/?tipo=colaboracion">Pedir propuesta</a>')}
'''
page('/estadisticas/', 'stats', 'Estadísticas · Patri Barbero', 'Estadísticas reales de YouTube, Instagram y TikTok de Patri Barbero: comunidad, audiencia y rendimiento, con fecha de actualización.', stats, STATS)

# =================================================== TRABAJA CONMIGO
trab = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('', 'Trabaja conmigo'))}
  <h1 class="T h1 rv">Trabaja conmigo</h1>
  <p class="lead rv">Tres formas de trabajar juntas. Elige la que necesita tu marca o tu negocio.</p>
</div></section>
<section class="sec tight"><div class="wrap">
  <div class="doors three">
    {door('/colaboraciones/', 'vichy', 'Colabora en mis redes', '«Quiero aparecer en tus vídeos». Tu marca dentro de mi contenido de YouTube, Reels y TikTok, para mi comunidad.', 'Ver colaboraciones')}
    {door('/ugc/', 'lunares', 'Contenido UGC', '«Quiero vídeos para mis redes o anuncios». Grabo y edito contenido que publicas tú, en tus canales.', 'Ver contenido UGC')}
    {door('/gestion-de-redes/', 'mante', 'Gestión de redes', '«Quiero que lleves mis redes». Estrategia, calendario, contenido y publicación para tu negocio.', 'Ver gestión de redes')}
  </div>
  <p class="rv" style="margin-top:30px;font-size:17px">¿No lo tienes claro? <a href="/contacto/" style="color:var(--co);font-weight:600">Escríbeme</a> y te digo qué te encaja.</p>
</div></section>
'''
page('/trabaja-conmigo/', 'trabaja', 'Trabaja conmigo · Patri Barbero', 'Tres formas de trabajar con Patri Barbero: colaboraciones en sus redes, contenido UGC para tu marca y gestión de redes para negocios.', trab)

# =================================================== COLABORA EN MIS REDES
colab = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('/trabaja-conmigo/', 'Trabaja conmigo'), ('', 'Colabora en mis redes'))}
  <div class="ph-grid">
    <div><h1 class="T h1 rv">Colabora en mis redes</h1>
      <p class="lead rv">Integro tu marca en mis vídeos como parte de la conversación: el producto entra en un look real y explico <span class="hl">por qué encaja</span>. Para una comunidad de mujeres que quiere vestir cómoda y mona.</p>
      <div class="ctas rv"><a class="btn p" href="/contacto/?tipo=colaboracion">Pedir propuesta {ARR}</a><a class="btn s" href="/estadisticas/">Ver estadísticas</a></div></div>
    <div class="rv">{win('colaboraciones publicadas', '<div class="mini-grid">' + ''.join(f'<span class="th"><img src="/img/{i}" alt="" loading="lazy"><img class="lg" src="/img/{lg}" alt="{al}"></span>' for y, i, ttl, m, lg, al in COLLABS) + '</div>')}</div>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Tu audiencia en un vistazo</p><h2 class="T h2 rv">Mi comunidad</h2></div><p class="lead rv">Datos de los paneles de cada plataforma, actualizados el <span data-date="actualizado">—</span>.</p></div>
  <div class="grid4">
    <div class="feat rv"><span class="T" style="font-size:52px" data-n="youtube.suscriptores" data-f="k1">—</span><p>suscriptores en YouTube</p></div>
    <div class="feat rv"><span class="T" style="font-size:52px" data-n="youtube.vis" data-f="k1">—</span><p>visualizaciones en YouTube en 28 días</p></div>
    <div class="feat rv"><span class="T" style="font-size:52px" data-n="youtube.audiencia.mujeres" data-f="pct0">—</span><p>de mi audiencia de YouTube son mujeres</p></div>
    <div class="feat rv"><span class="T" style="font-size:52px">15–35</span><p>años: el público al que le hablo, en España y Latinoamérica</p></div>
  </div>
  <p class="rv" style="margin-top:18px"><a href="/estadisticas/" style="color:var(--co);font-weight:600">Ver todas las estadísticas y audiencia →</a></p>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Formatos</p><h2 class="T h2 rv">Cómo aparece tu marca</h2></div><p class="lead rv">Cada colaboración se adapta a lo que quieres contar. Sin tarifas públicas: te preparo una propuesta.</p></div>
  <div class="grid4">
    <article class="feat rv"><h3 class="h3">Integración en YouTube</h3><p>Tu producto dentro de un vídeo largo, en los primeros minutos y explicado en contexto.</p><span class="meta">Vídeo largo cada domingo</span></article>
    <article class="feat rv"><h3 class="h3">Vídeo dedicado</h3><p>Un vídeo completo construido alrededor de tu producto o de tu campaña.</p><span class="meta">YouTube</span></article>
    <article class="feat rv"><h3 class="h3">Reels, TikTok y Shorts</h3><p>Piezas cortas nativas de cada plataforma, con una idea clara desde el primer segundo.</p><span class="meta">Instagram · TikTok · YouTube</span></article>
    <article class="feat rv"><h3 class="h3">Eventos y experiencias</h3><p>Lanzamientos, talleres o presentaciones contados desde dentro.</p><span class="meta">Vlog o vídeo corto</span></article>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Experiencia</p><h2 class="T h2 rv">Ya lo he hecho</h2></div><p class="lead rv">Marcas con las que ya he colaborado en mi canal.</p></div>
  <div class="grid4">{''.join(f'<div class="rv xp"><div class="xp-logo"><img src="/img/{lg}" alt="{al}"></div>' + vid(y, i, t, m) + '</div>' for y, i, t, m, lg, al in COLLABS)}</div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Proceso</p><h2 class="T h2 rv">Cómo trabajamos</h2></div><p class="lead rv">Claro y sin sorpresas, desde el primer mensaje hasta la publicación.</p></div>
  <ol class="steps" style="--n:4">
    <li class="rv"><b>Me escribes</b><p>Cuéntame la marca, el objetivo y las fechas.</p></li>
    <li class="rv"><b>Te propongo</b><p>Idea, formato, plataformas y presupuesto adaptados a tu objetivo.</p></li>
    <li class="rv"><b>Creamos</b><p>Grabo y edito. Te enseño el contenido antes de publicar.</p></li>
    <li class="rv"><b>Publicamos</b><p>Sale en mis redes y te paso los resultados.</p></li>
  </ol>
</div></section>

{band('Hablemos de tu <em>campaña</em>', 'Respondo en 24–48 h laborables. Contenido en español, con subtítulos y traducción automática al inglés en YouTube.', f'<a class="btn p" href="/contacto/?tipo=colaboracion">Pedir propuesta {ARR}</a>')}
'''
page('/colaboraciones/', 'colab', 'Colabora en mis redes · Patri Barbero', 'Tu marca en los vídeos de Patri Barbero en YouTube, Reels y TikTok, para una comunidad de mujeres de 15 a 35 años que quiere vestir cómoda y femenina.', colab, STATS)

# =================================================== UGC
ugc = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('/trabaja-conmigo/', 'Trabaja conmigo'), ('', 'Contenido UGC'))}
  <div class="ph-grid">
    <div><h1 class="T h1 rv">Contenido UGC</h1>
      <p class="lead rv">Vídeos para que <span class="hl">los publique tu marca</span> en sus redes o en sus anuncios: gancho desde el primer segundo, producto en contexto y un mensaje claro. No dependen de mis seguidores, sino de cómo está contado.</p>
      <div class="ctas rv"><a class="btn p" href="/contacto/?tipo=ugc">Pedir contenido {ARR}</a><a class="btn s" href="#portfolio">Ver ejemplos</a></div></div>
    <div class="rv"><div class="chips" style="gap:10px"><span class="chip"><i></i>Moda</span><span class="chip"><i></i>Belleza</span><span class="chip"><i></i>Lifestyle</span><span class="chip"><i></i>Alimentación</span><span class="chip"><i></i>Deporte y fitness</span><span class="chip"><i></i>Viajes</span><span class="chip"><i></i>Apps y servicios</span><span class="chip dark">Vertical 9:16 listo para publicar</span></div></div>
  </div>
</div></section>

<section class="sec tight" id="marcas"><div class="wrap">
  <div class="rv card" style="padding:24px 26px"><p class="subh">Experiencia · He creado contenido UGC para</p><div class="logos"><img src="/img/logo_miravia.svg" alt="Miravia"><img src="/img/logo_modibodi.svg" alt="Modibodi"><img src="/img/logo_perfumerias.png" alt="Perfumerías.com" class="dk"><img src="/img/logo_eggo.jpg" alt="Eggo"><img src="/img/logo_impress.svg" alt="Impress"><img src="/img/logo_matchaflix.svg" alt="Matchaflix"><img src="/img/logo_matchaandco.svg" alt="Matcha &amp; Co" class="tall"><img src="/img/logo_acelero.jpg" alt="Acelero"><img src="/img/logo_mooves.png" alt="Mooves Studio"></div></div>
</div></section>

<section class="sec tight" id="portfolio"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Ejemplos</p><h2 class="T h2 rv">Cómo grabo</h2></div><p class="lead rv">Elige un sector. Cada vídeo indica qué es, para que sepas exactamente qué estás viendo.</p></div>
  <div class="tabs scroll" role="tablist" aria-label="Sector">{''.join(f'<button role="tab" aria-selected="{"true" if n == 0 else "false"}" aria-controls="s-{k}" id="ts-{k}">{lab}</button>' for n, (k, lab, ex) in enumerate(UGC_EX))}</div>
  {''.join(f'<div id="s-{k}" role="tabpanel" aria-labelledby="ts-{k}"' + ('' if n == 0 else ' hidden') + '>' + ('<div class="grid4 shorts">' + ''.join(vid(y, i, t, f'<span class="tag {c}">{tg}</span>', True) for y, i, t, tg, c in ex) + '</div>' if ex else f'<div class="card soon"><p><b>Ejemplos de {lab.lower()}</b></p><p class="muted">¿Quieres ver cómo grabo para tu sector? Pídemelo y te envío muestras.</p><a class="btn s" href="/contacto/?tipo=ugc">Pedir muestras</a></div>') + '</div>' for n, (k, lab, ex) in enumerate(UGC_EX))}
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Formatos</p><h2 class="T h2 rv">Qué grabo</h2></div><p class="lead rv">Cada pieza se entrega editada y con subtítulos, con al menos una ronda de revisión.</p></div>
  <div class="grid3">
    <article class="feat rv"><h3 class="h3">Vídeo de producto</h3><p>El producto en uso, con gancho, beneficio y llamada a la acción.</p><span class="meta">15–45 s · anuncios y redes</span></article>
    <article class="feat rv"><h3 class="h3">Hablando a cámara</h3><p>Testimonio o explicación en primera persona, natural y creíble.</p><span class="meta">20–60 s · anuncios</span></article>
    <article class="feat rv"><h3 class="h3">Unboxing</h3><p>Recibir y probar el producto por primera vez.</p><span class="meta">30–60 s · lanzamientos</span></article>
    <article class="feat rv"><h3 class="h3">Tutorial o demo</h3><p>Cómo se usa, paso a paso, para resolver dudas antes de comprar.</p><span class="meta">30–90 s · apps y belleza</span></article>
    <article class="feat rv"><h3 class="h3">Lifestyle</h3><p>El producto dentro de un momento real: un look, una mañana, un plan.</p><span class="meta">15–30 s · marca</span></article>
    <article class="feat rv"><h3 class="h3">Fotos de producto</h3><p>Fotografías en contexto para redes, web o fichas de producto.</p><span class="meta">Pack de fotos</span></article>
  </div>
  <div class="rv" style="margin-top:22px">{win('si lo necesitas, pídemelo', '<p style="margin-bottom:14px">Además de la pieza final, te puedo enviar <b>cualquiera de estas versiones</b>. Solo tienes que pedírmelo en el brief:</p><div class="chips"><span class="chip"><i></i>Variaciones de gancho</span><span class="chip"><i></i>Formatos 1:1 y 4:5</span><span class="chip"><i></i>Versión sin subtítulos</span><span class="chip"><i></i>Material en bruto</span></div><p class="note" style="margin-top:14px">El uso en anuncios, la exclusividad y los plazos urgentes se acuerdan en la propuesta.</p>')}</div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Proceso</p><h2 class="T h2 rv">Del brief a la entrega</h2></div><p class="lead rv">Antes de empezar acordamos por escrito qué se entrega, las revisiones y dónde y cuánto tiempo puedes usar el contenido.</p></div>
  <ol class="steps" style="--n:3">
    <li class="rv"><b>Brief</b><p>Me cuentas producto, objetivo y dónde se usará.</p></li>
    <li class="rv"><b>Propuesta</b><p>Enfoque, entregables, plazos, derechos de uso y presupuesto cerrado.</p></li>
    <li class="rv"><b>Producto</b><p>Me envías el producto o el acceso al servicio.</p></li>
    <li class="rv"><b>Ideas y guion</b><p>Te paso los ganchos y el guion antes de grabar.</p></li>
    <li class="rv"><b>Grabación y edición</b><p>Grabo, edito, subtitulo y adapto a cada formato.</p></li>
    <li class="rv"><b>Entrega</b><p>Archivos finales, con al menos una ronda de revisión.</p></li>
  </ol>
</div></section>

{band('Cuéntame tu <em>producto</em>', 'Con unos pocos datos te preparo una propuesta y un presupuesto cerrado.', f'<a class="btn p" href="/contacto/?tipo=ugc">Pedir contenido {ARR}</a>')}
'''
page('/ugc/', 'ugc', 'Contenido UGC para marcas · Patri Barbero', 'Vídeo UGC para las redes y anuncios de tu marca: formatos, ejemplos, proceso y derechos de uso claros. Moda, belleza, lifestyle, alimentación, apps y servicios.', ugc)

# =================================================== GESTIÓN DE REDES
redes = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('/trabaja-conmigo/', 'Trabaja conmigo'), ('', 'Gestión de redes'))}
  <div class="ph-grid">
    <div><h1 class="T h1 rv">Gestión de redes</h1>
      <p class="lead rv">Llevo las redes de tu negocio con estrategia y constancia, para que no tengas que pensar cada día qué subir. <span class="hl">Tú te ocupas de tu negocio; yo, de que se vea.</span></p>
      <div class="ctas rv"><a class="btn p" href="/contacto/?tipo=redes">Pedir presupuesto {ARR}</a><a class="btn s" href="#metodo">Cómo trabajo</a></div></div>
    <div class="rv">{win('un mes conmigo', '<ul class="ticks arrow"><li><span><b>Semana 1 · Plan</b><small>Reunión corta, calendario del mes y materiales que necesito.</small></span></li><li><span><b>Semana 2 · Creación</b><small>Diseño, edición de vídeo y copys.</small></span></li><li><span><b>Semana 3 · Aprobación</b><small>Te lo paso todo junto para revisarlo, con al menos una ronda de cambios.</small></span></li><li><span><b>Semana 4 · Publicación e informe</b><small>Programo, publico y te envío el resumen.</small></span></li></ul>')}</div>
  </div>
</div></section>

<section class="sec tight" id="metodo"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Método</p><h2 class="T h2 rv">Paso a paso</h2></div><p class="lead rv">Seis pasos que se repiten cada mes, siempre a partir de <span class="hl">tus objetivos y tu público</span>. Nada de plantillas genéricas.</p></div>
  <ol class="steps" style="--n:3">
    <li class="rv"><b>Análisis</b><p>Qué quieres conseguir, a quién te diriges, cómo están tus redes y qué hace tu competencia.</p></li>
    <li class="rv"><b>Estrategia</b><p>Basada en tus objetivos y en tu público objetivo: tono, temas y formatos pensados para tu negocio.</p></li>
    <li class="rv"><b>Calendario</b><p>Qué se publica y cuándo, y a qué objetivo responde cada publicación.</p></li>
    <li class="rv"><b>Creación</b><p>Diseño, edición de vídeo y copys con la imagen de tu marca y para tu público.</p></li>
    <li class="rv"><b>Publicación</b><p>Programo y publico en los momentos en que tu público está más activo. Tú solo apruebas.</p></li>
    <li class="rv"><b>Medición</b><p>Informe mensual comparado con tus objetivos: qué ha funcionado y qué ajustamos.</p></li>
  </ol>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Claridad</p><h2 class="T h2 rv">Qué incluye</h2></div><p class="lead rv">Hay planes según el volumen de publicaciones, Stories y redes. El presupuesto se ajusta a tu negocio.</p></div>
  <div class="grid3">
    <div class="rv">{win('incluye', '<ul class="ticks"><li>Estrategia y calendario mensual</li><li>Diseño de publicaciones y edición de vídeo</li><li>Copys y hashtags</li><li>Programación y publicación</li><li>Stories según el plan</li><li>Informe mensual y ajustes</li></ul>')}</div>
    <div class="rv">{win('necesito de ti', '<ul class="ticks arrow"><li>Fotos y vídeos de tu negocio, o que pueda ir a grabarlos</li><li>Acceso a tus redes</li><li><span>Una persona de contacto<small>Con quien reunirme y que revise y apruebe los contenidos</small></span></li><li>Novedades y promociones con antelación</li></ul>')}</div>
    <div class="rv">{win('no incluye', '<ul class="ticks no"><li><span>Desplazamientos para grabar<small>Si hay que ir a tu negocio a grabar, se presupuestan aparte</small></span></li><li><span>Publicidad de pago<small>Gestión opcional, aparte</small></span></li><li><span>Atención a mensajes directos<small>Se puede gestionar aparte</small></span></li><li>Cambios ilimitados</li></ul>')}</div>
  </div>
  <div class="rv card" style="padding:22px 24px;margin-top:22px;max-width:820px"><p><b>Con quién trabajas.</b> <span class="muted">Estudié Digital Business en ESIC, he trabajado en comunicación de marca en una empresa multinacional y en campañas con creadores en una agencia. Gestiono mis propias redes cada semana y aplico el mismo método a las de tu negocio. Trabajo con pocos negocios a la vez para dedicarles el tiempo que necesitan.</span></p></div>
</div></section>

{band('¿Ponemos tus redes <em>en orden</em>?', 'Cuéntame tu negocio y te propongo un plan mensual a medida. Madrid y en remoto.', f'<a class="btn p" href="/contacto/?tipo=redes">Pedir presupuesto {ARR}</a>')}
'''
page('/gestion-de-redes/', 'redes', 'Gestión de redes sociales para negocios · Patri Barbero', 'Gestión de redes para pequeños negocios y marcas: estrategia, calendario, diseño, vídeo, copys, publicación e informe mensual. Madrid y en remoto.', redes)

# =================================================== SOBRE MÍ
sobre = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('', 'Sobre mí'))}
  <div class="ph-grid">
    <div class="rv cutout"><img src="/img/patri-espejo-1100.webp" srcset="/img/patri-espejo-1100.webp 432w, /img/patri-espejo-1800.webp 708w" sizes="(max-width:860px) 60vw, 360px" alt="Patri Barbero frente al espejo con top blanco, pantalón negro y bolso rojo" width="708" height="1800"></div>
    <div><h1 class="T h1 rv">Sobre mí</h1>
      <p class="lead rv">Soy Patri. Siempre voy en zapatillas y priorizo ir cómoda, pero me encanta verme mona y femenina. Por eso hablo de moda desde los dos lados: <span class="hl">no hay que sufrir para ir mona</span>.</p>
      <p class="rv" style="margin-top:16px;color:var(--gr)">No me quedo en qué se lleva: explico qué transmite, por qué aparece ahora y cómo llevarlo siendo tú. Porque para mí, vestirse también es <span class="serif" style="font-size:1.15em;color:var(--ch)">construirse</span>.</p></div>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Cómo hablo de moda</p><h2 class="T h2 rv">Mi filtro</h2></div><p class="lead rv">Cinco preguntas que me hago con cada tendencia.</p></div>
  <ol class="steps" style="--n:5">
    <li class="rv"><b>¿Qué se lleva?</b><p>La tendencia, sin rodeos.</p></li>
    <li class="rv"><b>¿Qué transmite?</b><p>Lo que comunica cuando te lo pones.</p></li>
    <li class="rv"><b>¿Por qué ahora?</b><p>De dónde viene y por qué aparece.</p></li>
    <li class="rv"><b>¿Qué identidad construye?</b><p>Qué chica hay detrás de la mezcla.</p></li>
    <li class="rv"><b>¿Cómo llevarlo siendo tú?</b><p>Versión cómoda y mona, adaptada a ti.</p></li>
  </ol>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Trayectoria</p><h2 class="T h2 rv">De dónde vengo</h2></div><p class="lead rv">Conozco las campañas desde los dos lados: el de la creadora y el de la marca.</p></div>
  <div class="rv" style="max-width:820px">{win('ficha · patri barbero', '<dl class="ficha"><div><dt>Formación</dt><dd>Grado universitario en Digital Business · ESIC</dd></div><div><dt>Formación</dt><dd>Diploma universitario en Herramientas Digitales y Multimedia</dd></div><div><dt>Comunicación</dt><dd>Comunicación de marca en una empresa multinacional</dd></div><div><dt>Agencia</dt><dd>Influencer marketing y campañas con creadores en una agencia</dd></div><div><dt>Creadora</dt><dd>Un vídeo largo en YouTube cada domingo y vídeos cortos varias veces por semana en Instagram, TikTok y YouTube Shorts</dd></div></dl>')}</div>
</div></section>

{band('¿Hablamos?', 'Para colaboraciones, contenido UGC o gestión de redes, escríbeme.', f'<a class="btn p" href="/contacto/">Contacto {ARR}</a><a class="btn s" href="/trabaja-conmigo/">Trabaja conmigo</a>')}
'''
page('/sobre-mi/', 'sobre', 'Sobre mí · Patri Barbero', 'Quién es Patri Barbero: creadora de contenido de moda sporty y femenina, graduada en Digital Business por ESIC, con experiencia en comunicación e influencer marketing.', sobre)

# =================================================== CONTACTO
def fld(label, inp, req=False, small=''):
    star = ' <b class="req" aria-hidden="true">*</b>' if req else ''
    sm = f' <small>{small}</small>' if small else ''
    return f'<label class="fld" data-label="{label}"><span>{label}{star}{sm}</span>{inp}</label>'
SECT = ''.join(f'<option>{x}</option>' for x in ['Hostelería (bar, cafetería, restaurante)', 'Moda y complementos', 'Belleza y estética', 'Salud y bienestar', 'Deporte y fitness', 'Comercio local', 'Tienda online', 'Servicios profesionales', 'Educación y formación', 'Turismo y alojamiento', 'Inmobiliaria'])
contacto = f'''<section class="page-hero"><div class="wrap">
  {crumbs(('/', 'Inicio'), ('', 'Contacto'))}
  <div class="ph-grid" style="align-items:start">
    <div><h1 class="T h1 rv">Hablemos</h1>
      <p class="lead rv">Cuéntame qué necesitas y te respondo en 24–48 h laborables.</p>
      <div class="ctas rv" style="flex-direction:column;align-items:flex-start"><a class="btn s" href="mailto:{EMAIL}">{EMAIL}</a>
      <div class="chips"><a class="chip" href="{YT}" target="_blank" rel="noopener">YouTube ↗</a><a class="chip" href="{IG}" target="_blank" rel="noopener">Instagram ↗</a><a class="chip" href="{TT}" target="_blank" rel="noopener">TikTok ↗</a></div></div>
      <p class="note rv" style="margin-top:22px">Sin tarifas públicas: cada propuesta se adapta al proyecto.</p></div>
    <div class="rv">{win('mensaje nuevo · para patri', f"""
      <form class="form" id="contact" novalidate data-to="{EMAIL}">
        <p class="note legend-req"><b class="req">*</b> Campo obligatorio</p>
        <div class="fld" data-label="Me interesa"><span>Me interesa <b class="req" aria-hidden="true">*</b></span><div class="opts" role="radiogroup" aria-required="true">
          <label class="opt"><input type="radio" name="tipo" value="Colabora en mis redes" required data-msg="Elige qué te interesa."><span>Colabora en mis redes</span></label>
          <label class="opt"><input type="radio" name="tipo" value="Contenido UGC"><span>Contenido UGC</span></label>
          <label class="opt"><input type="radio" name="tipo" value="Gestión de redes"><span>Gestión de redes</span></label>
          <label class="opt"><input type="radio" name="tipo" value="Otra cosa"><span>Otra cosa</span></label></div></div>
        <div class="f2">{fld('Nombre', '<input type="text" name="nombre" required autocomplete="name" data-msg="Dime tu nombre.">', True)}{fld('Email', '<input type="email" name="email" required autocomplete="email" data-msg="Necesito un email válido para responderte.">', True)}</div>
        {fld('Marca, agencia o negocio', '<input type="text" name="empresa" required autocomplete="organization" data-msg="Dime el nombre de tu marca, agencia o negocio.">', True)}
        <div data-for="Colabora en mis redes" hidden class="form">
          <div class="f2">{fld('Plataformas', '<select name="plataformas"><option selected>Aún no lo sé</option><option>YouTube</option><option>Instagram</option><option>TikTok</option><option>Varias</option></select>')}{fld('Fecha de publicación', '<input type="text" name="fecha" placeholder="p. ej. 2.ª quincena de enero">')}</div>
          {fld('Presupuesto orientativo', '<select name="presupuesto"><option value="">Prefiero hablarlo</option><option>Menos de 300 €</option><option>300–700 €</option><option>700–1.500 €</option><option>Más de 1.500 €</option></select>')}
        </div>
        <div data-for="Contenido UGC" hidden class="form">
          <div class="f2">{fld('Número de piezas', '<select name="piezas"><option selected>No lo sé aún</option><option>1</option><option>2–3</option><option>4–6</option><option>Más de 6</option></select>')}{fld('¿Dónde se usará?', '<select name="uso"><option selected>No lo sé aún</option><option>Redes de la marca</option><option>Anuncios</option><option>Las dos cosas</option><option>Web o tienda online</option></select>')}</div>
          {fld('Plazo', '<input type="text" name="plazo" placeholder="p. ej. antes del 15 de diciembre">')}
        </div>
        <div data-for="Gestión de redes" hidden class="form">
          <div class="f2">{fld('Sector', '<select name="sector" required data-msg="Elige el sector de tu negocio."><option value="" selected>—</option>' + SECT + '<option>Otro</option></select>', True)}{fld('Ciudad', '<input type="text" name="ciudad" required autocomplete="address-level2" placeholder="p. ej. Madrid" data-msg="Dime en qué ciudad está tu negocio.">', True)}</div>
          <div data-otro hidden>{fld('¿Qué sector?', '<input type="text" name="sector_otro" required placeholder="Cuéntame a qué se dedica tu negocio" data-msg="Dime a qué se dedica tu negocio.">', True)}</div>
          <div class="f2">{fld('Tus redes', '<input type="text" name="redes" placeholder="@tunegocio (si ya las tienes)">')}{fld('¿Tienes fotos y vídeos?', '<select name="materiales" required data-msg="Dime si tienes fotos y vídeos."><option value="" selected>—</option><option>Sí, te los paso</option><option>Algunos</option><option>No, necesito que se graben</option></select>', True)}</div>
        </div>
        {fld('Cuéntame', '<textarea name="mensaje" placeholder="Qué quieres conseguir, producto, fechas…"></textarea>')}
        <div class="hp" aria-hidden="true"><label>No rellenar <input name="web_site" tabindex="-1" autocomplete="off"></label></div>
        <label class="consent"><input type="checkbox" name="acepto" required data-msg="Necesito tu permiso para usar estos datos y responderte."><span>Acepto que Patri Barbero use estos datos solo para responder a mi mensaje. <a href="/privacidad/">Privacidad</a> <b class="req" aria-hidden="true">*</b></span></label>
        <p class="err" role="alert"></p>
        <button class="btn p" type="submit">Enviar mensaje {ARR}</button>
      </form>
      <div class="done" id="done" hidden tabindex="-1"><div class="seal"><svg viewBox="0 0 20 20"><path d="M5 10.5l3.2 3.2L15 7" fill="none" stroke="#2B140C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h2 class="h3">¡Mensaje enviado!</h2><p class="muted">Gracias. Te respondo en 24–48 h laborables al email que me has dejado.</p></div>
      <div class="done" id="fail" hidden tabindex="-1"><h2 class="h3">No se ha podido enviar</h2><p class="muted">Algo ha fallado con la conexión. Puedes enviármelo desde tu correo, con el texto ya escrito:</p><a class="btn d" data-mail href="#">Abrir mi correo</a><button class="btn s" type="button" data-copy>Copiar el texto</button><p class="note"></p><p class="note why"></p></div>
    """)}</div>
  </div>
</div></section>
'''
page('/contacto/', 'contacto', 'Contacto · Patri Barbero', 'Escríbeme para colaboraciones en mis redes, contenido UGC o gestión de redes. Respuesta en 24–48 h laborables.', contacto)

# =================================================== LEGALES
TITULAR, LEGAL_MAIL = 'Victoria Patricia Barbero Moyá', EMAIL
def legal_page(path, title, desc, blocks):
    body = ''.join(f'<h2 class="h3" style="margin:30px 0 10px">{h}</h2>' + ''.join(f'<p style="margin-top:10px">{x}</p>' for x in ps) for h, ps in blocks)
    page(path, '', f'{title} · Patri Barbero', desc,
         f'<section class="page-hero"><div class="wrap">{crumbs(("/", "Inicio"), ("", title))}<h1 class="T h1">{title}</h1><div class="legal-txt card" style="padding:clamp(20px,3vw,32px);margin-top:24px;max-width:820px"><p class="note">Última actualización: 21 de noviembre de 2026</p>{body}</div></div></section>', noindex=True)

legal_page('/aviso-legal/', 'Aviso legal', 'Aviso legal de patribarbero.com.', [
  ('Titular de la web', [f'Titular: {TITULAR}, que actúa con el nombre profesional «Patri Barbero».', 'Domicilio: Madrid (España).', f'Email de contacto: <a href="mailto:{LEGAL_MAIL}">{LEGAL_MAIL}</a>.']),
  ('Objeto', ['Esta web presenta la actividad profesional de Patri Barbero como creadora de contenido de moda y los servicios que ofrece a marcas y negocios: colaboraciones en sus redes, contenido UGC y gestión de redes sociales.']),
  ('Propiedad intelectual', ['Los textos, fotografías, vídeos, diseños y logotipos de esta web pertenecen a su titular o se usan con permiso. No se pueden copiar, reproducir ni distribuir sin autorización por escrito.', 'Los nombres y logotipos de las marcas con las que se ha colaborado pertenecen a sus respectivos dueños y se muestran solo para indicar esos trabajos.']),
  ('Responsabilidad', ['La titular procura que la información de la web sea correcta y esté actualizada, pero no garantiza que no contenga errores. Las cifras de redes sociales indican la fecha y la fuente de la que se han obtenido.', 'La web enlaza a otros sitios (YouTube, Instagram, TikTok y otros). La titular no se hace responsable de sus contenidos ni de sus políticas.']),
  ('Ley aplicable', ['Esta web se rige por la legislación española.']),
])

legal_page('/privacidad/', 'Privacidad', 'Política de privacidad de patribarbero.com.', [
  ('Quién trata tus datos', [f'Responsable: {TITULAR} («Patri Barbero»). Email: <a href="mailto:{LEGAL_MAIL}">{LEGAL_MAIL}</a>.']),
  ('Qué datos recojo y para qué', ['Solo recojo los datos que me envías por el formulario de contacto o por email: nombre, email, marca o negocio y lo que me cuentes en el mensaje (por ejemplo, sector, ciudad, plazos o presupuesto).', 'Los uso únicamente para responderte y, si llegamos a trabajar juntas, para preparar y gestionar la propuesta o el encargo. No los uso para enviarte publicidad ni los vendo.']),
  ('Base legal', ['Tu consentimiento, que das al marcar la casilla del formulario o al escribirme, y la aplicación de medidas precontractuales cuando me pides una propuesta.']),
  ('Cuánto tiempo los guardo', ['El tiempo necesario para responderte y gestionar la relación. Si no llegamos a trabajar juntas, los borro en un plazo máximo de un año. Si hay un encargo, los guardo durante los plazos que exija la ley.']),
  ('Quién más los ve', ['El formulario se envía a mi correo a través de FormSubmit (formsubmit.co), un servicio de terceros que solo hace llegar el mensaje. Recibo y guardo los mensajes en Gmail (Google). La web está alojada en Cloudflare. Estos proveedores pueden tratar datos fuera del Espacio Económico Europeo con las garantías que exige la normativa.', 'No cedo tus datos a nadie más, salvo obligación legal.']),
  ('Cookies', ['Esta web no usa cookies propias, ni de análisis, ni de publicidad.', 'Los vídeos de YouTube solo se cargan si pulsas en ellos, y lo hacen desde youtube-nocookie.com. En ese momento, YouTube puede guardar información en tu navegador según su propia política.']),
  ('Tus derechos', [f'Puedes pedirme acceder a tus datos, corregirlos, borrarlos, limitar su uso, oponerte a él o llevártelos, escribiendo a <a href="mailto:{LEGAL_MAIL}">{LEGAL_MAIL}</a>. También puedes retirar tu consentimiento cuando quieras.', 'Si crees que no he tratado bien tus datos, puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).']),
  ('Menores', ['Si tienes menos de 14 años, no me envíes tus datos por el formulario.']),
])
page('/404.html', '', 'Página no encontrada · Patri Barbero', 'Esta página no existe.',
     f'<section class="page-hero"><div class="wrap"><p class="kicker">Error 404</p><h1 class="T h1">Esta talla<br>no la tenemos</h1><p class="lead" style="margin-top:20px">La página que buscas no existe o ha cambiado de sitio.</p><div class="ctas"><a class="btn p" href="/">Inicio {ARR}</a><a class="btn s" href="/estadisticas/">Estadísticas</a><a class="btn s" href="/trabaja-conmigo/">Trabaja conmigo</a><a class="btn s" href="/contacto/">Contacto</a></div></div></section>', noindex=True)

# limpieza de la maqueta anterior
for old in ('marcas',):
    shutil.rmtree(R / old, ignore_errors=True)
(R / 'datos.js').write_text(subprocess.run(['git', '-C', str(R), 'show', 'origin/main:datos.js'], capture_output=True, text=True).stdout) if not (R / 'datos.js').exists() else None
(R / '_redirects').write_text('\n'.join(['/media-kit /estadisticas/ 301', '/media-kit/ /estadisticas/ 301', '/marcas /trabaja-conmigo/ 301', '/marcas/ /trabaja-conmigo/ 301', '/marcas/ugc/ /ugc/ 301', '/influencer /colaboraciones/ 301', '/influencer/ /colaboraciones/ 301', '/colabora /colaboraciones/ 301', '/community-manager /gestion-de-redes/ 301', '/community-manager/ /gestion-de-redes/ 301', '']))
(R / '_headers').write_text('/assets/f/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/img/*\n  Cache-Control: public, max-age=2592000\n/datos.js\n  Cache-Control: public, max-age=300\n')
(R / 'robots.txt').write_text('User-agent: *\nDisallow: /laboratorio/\nSitemap: https://patribarbero.com/sitemap.xml\n')
(R / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in ['/', '/contenido/', '/estadisticas/', '/trabaja-conmigo/', '/colaboraciones/', '/ugc/', '/gestion-de-redes/', '/sobre-mi/', '/contacto/', '/en/', '/en/content/', '/en/stats/', '/en/work-with-me/', '/en/collaborations/', '/en/ugc/', '/en/social-media-management/', '/en/about/', '/en/contact/']) + '</urlset>\n')
import sys; sys.path.insert(0, str(pathlib.Path(__file__).parent)); import en; en.build(PAGES, R)
print('ok')
