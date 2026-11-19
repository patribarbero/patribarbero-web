#!/usr/bin/env python3
"""Genera la web nueva de Patri Barbero (rama rediseno). Páginas estáticas con cabecera/pie comunes.
El email de contacto se toma de la web publicada (rama main), para no duplicarlo aquí."""
import pathlib, re, subprocess
R = pathlib.Path('/home/claude/repo-web')
SPR = pathlib.Path('/home/claude/repo-web/tools/sprites.html').read_text()
SPR = SPR.replace('</svg>', '<symbol id="burst" viewBox="0 0 24 24"><path fill="currentColor" d="M12 0l2.4 8.2L22.4 4 17 11l7 1-7 1 5.4 7-8-4.2L12 24l-2.4-8.2L1.6 20 7 13l-7-1 7-1-5.4-7 8 4.2z"/></symbol></svg>')
BASE = 'https://patribarbero.com'
_main = subprocess.run(['git', '-C', str(R), 'show', 'main:index.html'], capture_output=True, text=True).stdout
EMAIL = re.search(r'mailto:([^"?]+)', _main).group(1)
ARR = '<svg class="i arr" aria-hidden="true"><use href="#arrow"/></svg>'

def head(title, desc, path, extra=''):
    url = BASE + path
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Patri Barbero">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/img/og.jpg">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#F5EFE8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Instrument+Serif:ital@1&family=Rubik:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
{SPR}
'''

def header(cur):
    def a(href, txt, key):
        c = ' aria-current="page"' if key == cur else ''
        return f'<a href="{href}"{c}>{txt}</a>'
    return f'''<header class="top">
  <div class="wrap bar">
    <a class="logo" href="/" aria-label="Patri Barbero, inicio"><i class="tagdot" aria-hidden="true"></i>Patri Barbero</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav">Menú</button>
    <nav class="nav" id="nav" aria-label="Principal">
      {a('/influencer/', 'Influencer', 'inf')}
      {a('/ugc/', 'UGC', 'ugc')}
      {a('/community-manager/', 'Community manager', 'cm')}
      <a class="cta" href="#contacto">Contacto</a>
    </nav>
  </div>
</header>
'''

def switch(cur):
    items = [('/influencer/', 'Influencer', 'inf'), ('/ugc/', 'UGC', 'ugc'), ('/community-manager/', 'Community manager', 'cm')]
    return '<nav class="switch" aria-label="Servicios">' + ''.join(
        f'<a href="{h}"' + (' aria-current="page"' if k == cur else '') + f'>{t}</a>' for h, t, k in items) + '</nav>'

def contact(title_html, sub):
    return f'''<section class="sec-pad" id="contacto">
  <div class="wrap">
    <div class="contact-band rv">
      <div><p class="label" style="color:#D8C4D1;margin-bottom:16px">Contacto</p><h2>{title_html}</h2><p style="margin-top:16px;color:#D8C4D1;max-width:46ch">{sub}</p></div>
      <div class="links">
        <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
        <div class="soc">
          <a href="https://www.youtube.com/@patribarbero" target="_blank" rel="noopener"><svg class="i"><use href="#yt"/></svg>YouTube</a>
          <a href="https://www.instagram.com/patribarbero_/" target="_blank" rel="noopener"><svg class="i"><use href="#ig"/></svg>Instagram</a>
          <a href="https://www.tiktok.com/@patribarbero_" target="_blank" rel="noopener"><svg class="i"><use href="#tt"/></svg>TikTok</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

def foot(scripts=''):
    return f'''<footer class="foot">
  <div class="wrap">
    <span>© <span id="y">2026</span> Patri Barbero · Madrid</span>
    <nav aria-label="Pie"><a href="/influencer/">Influencer</a><a href="/ugc/">UGC</a><a href="/community-manager/">Community manager</a><a href="mailto:{EMAIL}">{EMAIL}</a></nav>
  </div>
</footer>
<dialog class="vd" id="vd" aria-label="Vídeo"><div class="box"><div class="frame"></div></div><button class="x" type="button">Cerrar ✕</button></dialog>
<script src="/assets/site.js" defer></script>
{scripts}
</body>
</html>
'''

def marquee(words):
    s = ''.join(f'<span>{w}</span>' for w in words)
    return f'<div class="marquee" aria-hidden="true"><div class="track">{s}{s}</div></div>'

def form(kind, title, subject, sets):
    fs = ''.join(f'<fieldset{" hidden" if i else ""}><legend>{lg}</legend>{body}</fieldset>' for i, (lg, body) in enumerate(sets))
    dots = '<i></i>' * len(sets)
    return f'''<div class="sheet rv d1">
  <div class="sheet-h"><h3>{title}</h3><span class="ref">Hoja de encargo<br>N.º {kind}</span></div>
  <form class="brief" novalidate data-subject="{subject}">
    <div class="steps" aria-hidden="true">{dots}</div>
    {fs}
    <div class="hp" aria-hidden="true"><label>No rellenar <input name="web_site" tabindex="-1" autocomplete="off"></label></div>
    <p class="err" role="alert"></p>
    <div class="nav-row">
      <button class="back" type="button" data-back>← Atrás</button>
      <span></span>
      <button class="btn ink" type="button" data-next>Siguiente {ARR}</button>
      <button class="btn rose" type="submit" data-send hidden>Preparar mi solicitud {ARR}</button>
    </div>
  </form>
  <div class="done" hidden>
    <div class="seal">¡Lo<br>tengo!</div>
    <h3>Tu solicitud está lista</h3>
    <p>Se ha abierto tu correo con todo rellenado. Solo tienes que pulsar <b>enviar</b>. Te respondo en 24–48 h laborables.</p>
    <a class="btn ink" data-mail href="#">Abrir mi correo {ARR}</a>
    <button class="back" type="button" data-copy>¿No se abre? Copiar el texto</button>
    <p class="note"></p>
  </div>
</div>'''

def fld(label, inp, small=''):
    sm = f' <small>{small}</small>' if small else ''
    return f'<label class="fld" data-label="{label}"><span>{label}{sm}</span>{inp}</label>'

def opts(label, name, items, req=False, typ='checkbox'):
    rg = ' data-req-group' if req else ''
    o = ''.join(f'<label class="opt"><input type="{typ}" name="{name}" value="{x}" data-msg="Elige al menos una opción."><span>{x}</span></label>' for x in items)
    return f'<div class="fld" data-label="{label}"><span>{label}</span><div class="opts"{rg}>{o}</div></div>'

CONTACT_SET = ('Tus datos', '<div class="f2">' + fld('Nombre', '<input type="text" name="nombre" required autocomplete="name" data-msg="Dime tu nombre.">') + fld('Email', '<input type="email" name="email" required autocomplete="email" data-msg="Necesito un email válido para responderte.">') + '</div>'
               + '<label class="consent"><input type="checkbox" name="acepto" required data-msg="Necesito tu permiso para usar estos datos y responderte."><span>Acepto que Patri Barbero use estos datos solo para responder a mi solicitud.</span></label>')

def write(path, html):
    p = R / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(html)

# ============================================================ HOME
home = head('Patri Barbero · Creadora de contenido, UGC y community manager en Madrid',
            'Creadora de contenido de moda en YouTube, Instagram y TikTok. Colaboraciones como influencer, vídeo UGC para marcas y gestión de redes sociales para negocios.', '/')
home += header('home')
home += f'''<main id="main">
<section class="home-hero">
  <div class="wrap">
    <div class="hh-top">
      <h1 class="display hh-title rv">Contenido que<br>se <span class="serif">mira</span>, se<br>entiende y vende.</h1>
      <div class="hh-side rv d2">
        <p class="label rose">Patri Barbero · Madrid</p>
        <p>Creo contenido de moda para mi comunidad, produzco vídeo UGC para marcas y ayudo a negocios con sus redes. <b style="color:var(--ink)">Elige qué necesitas:</b></p>
      </div>
    </div>
    <div class="rack">
      <div class="rail" aria-hidden="true"></div>
      <div class="tags">
        <a class="tag t-inf" href="/influencer/">
          <div class="body"><i class="hole" aria-hidden="true"></i>
            <div class="media" aria-hidden="true"><img src="/img/hero.jpg" alt="" loading="lazy"></div>
            <p class="num"><span>01</span><span>Mis redes</span></p>
            <h2 class="name">Influen&shy;cer</h2>
            <p class="q">¿Quieres que tu marca aparezca en mis vídeos, contada como parte de mi día a día?</p>
            <p class="go"><span>Colaborar en mis redes</span><b><svg class="i"><use href="#arrow"/></svg></b></p>
          </div>
        </a>
        <a class="tag t-ugc" href="/ugc/">
          <div class="body"><i class="hole" aria-hidden="true"></i>
            <div class="media" aria-hidden="true"><img src="/img/broches.jpg" alt="" loading="lazy"></div>
            <p class="num"><span>02</span><span>Para tus canales</span></p>
            <h2 class="name">UGC</h2>
            <p class="q">¿Necesitas vídeos creativos para tus redes o tus anuncios, sin depender de mis seguidores?</p>
            <p class="go"><span>Pedir contenido</span><b><svg class="i"><use href="#arrow"/></svg></b></p>
          </div>
        </a>
        <a class="tag t-cm" href="/community-manager/">
          <div class="body"><i class="hole" aria-hidden="true"></i>
            <div class="media" aria-hidden="true" style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px"><img src="/img/oversized.jpg" alt="" loading="lazy"><img src="/img/abc.jpg" alt="" loading="lazy"><img src="/img/broches.jpg" alt="" loading="lazy"></div>
            <p class="num"><span>03</span><span>Para negocios</span></p>
            <h2 class="name">Commu&shy;nity</h2>
            <p class="q">¿Quieres que alguien se ocupe de tus redes con estrategia, calendario y constancia?</p>
            <p class="go"><span>Gestionar mis redes</span><b><svg class="i"><use href="#arrow"/></svg></b></p>
          </div>
        </a>
      </div>
    </div>
  </div>
  {marquee(['Moda como identidad','Vídeo UGC','Estrategia de redes','YouTube · Instagram · TikTok','Desde Madrid'])}
</section>

<section class="sec-pad">
  <div class="wrap who">
    <figure class="rv"><img src="/img/hero.jpg" alt="Patri Barbero en su espacio de grabación" loading="lazy" width="1100" height="1467"><figcaption><b data-n="youtube.suscriptores" data-f="k1">–</b><span>suscriptores en YouTube</span></figcaption></figure>
    <div>
      <p class="label rose rv">Quién está detrás</p>
      <h2 class="sec rv d1" style="margin:14px 0 22px">Creadora <span class="serif">y</span> estratega.</h2>
      <p class="lead rv d2">Soy Patri. Creo contenido de moda sobre estilo, tendencias e identidad, porque para mí <b>vestirse también es construirse</b>. Estudié Digital Business en ESIC y he trabajado en comunicación y en una agencia de influencer marketing, así que conozco las campañas desde los dos lados: el de la creadora y el de la marca.</p>
      <div class="facts rv d3">
        <div><b data-n="youtube.vis" data-f="k1">–</b><span>visualizaciones en YouTube en 28 días</span></div>
        <div><b data-n="youtube.audiencia.mujeres" data-f="pct0">–</b><span>de mi audiencia de YouTube son mujeres</span></div>
        <div><b>3</b><span>plataformas: YouTube, Instagram y TikTok</span></div>
      </div>
      <p class="note rv d3" style="margin-top:10px">Datos de YouTube Studio · actualizados el <span data-date="actualizado">–</span></p>
    </div>
  </div>
</section>
</main>
'''
home += contact('¿Tienes algo <span class="serif">en mente?</span>', 'Escríbeme directamente o entra en el servicio que te interesa: cada uno tiene su propio formulario, con las preguntas justas.')
home += foot('<script src="/datos.js" defer></script><script src="/assets/stats.js" defer></script>')
write('index.html', home)

# ============================================================ INFLUENCER
inf_form = form('INF', 'Propuesta de colaboración', 'Colaboración influencer', [
  ('Tu marca', '<div class="f2">' + fld('Marca o agencia', '<input type="text" name="empresa" required autocomplete="organization" data-msg="¿De qué marca o agencia escribes?">') + fld('Web o Instagram', '<input type="text" name="web" placeholder="marca.com o @marca">') + '</div>'
     + fld('Producto o campaña', '<textarea name="campana" required placeholder="Qué queréis contar y a quién" data-msg="Cuéntame brevemente la campaña."></textarea>')),
  ('Formato', opts('Plataformas', 'plataformas', ['YouTube', 'Instagram', 'TikTok', 'Aún no lo sé'], True)
     + opts('Formato', 'formato', ['Integración en vídeo largo', 'Vídeo dedicado', 'Short / Reel / TikTok', 'Stories', 'Evento', 'Abierta a propuestas'], True)
     + '<div class="f2">' + fld('Fecha de publicación', '<input type="text" name="fecha" placeholder="p. ej. 2.ª quincena de enero">') + fld('Presupuesto orientativo', '<select name="presupuesto"><option value="">Prefiero hablarlo</option><option>Menos de 300 €</option><option>300–700 €</option><option>700–1.500 €</option><option>Más de 1.500 €</option></select>', 'opcional') + '</div>'),
  CONTACT_SET])

shorts = [('u0GktqmTMh8', 'oversized.jpg', 'Oversized y femenina', 'trabajos.oversized_youtube', 'Short'),
          ('MKhsAIKXquk', 'broches.jpg', 'Vuelven los broches', 'trabajos.broches_youtube', 'Short'),
          ('wu2mG4YX1dI', 'abc.jpg', 'Elige A, B o C', 'trabajos.abc_instagram', 'Reel')]
reels = ''.join(f'''<button class="reel rv d{i}" type="button" data-yt="{y}" data-title="{t}">
  <img src="/img/{im}" alt="" loading="lazy" width="480" height="853"><span class="pl"><i><svg><use href="#play"/></svg></i>{t}</span>
  <span class="stat"><b data-n="{k}" data-f="k1">–</b> {"visualizaciones" if fmt=="Short" else "reproducciones"} · {fmt}</span></button>''' for i, (y, im, t, k, fmt) in enumerate(shorts))

collabs = [('zBPboLQZKAo', 'Vivaia', 'Integración', 'Tips para vestir con estilo en otoño', '17 ago 2025'),
           ('gKLj2hae2ww', 'Vivaia', 'Segunda integración', 'Esto en la moda no es normal', ''),
           ('pYXWRYBJd9s', 'The Colour Nook', 'Taller', 'Colorimetría: por qué nada te queda bien', '29 abr 2026'),
           ('CecPikzWLI8', 'Modibodi', 'Evento', 'Vlog: un día con el evento de Modibodi', '15 may 2024')]
clist = ''.join(f'<li><button type="button" data-yt="{y}" data-wide="1" data-title="{t}" data-img="/img/{y}.jpg"><span class="b">{b}</span><span class="t">{t}</span><span class="k">{k}{" · " + d if d else ""}</span><span class="pv" aria-hidden="true">Ver ↗</span></button></li>' for y, b, k, t, d in collabs)

inf = head('Influencer de moda · Colabora con Patri Barbero en YouTube, Instagram y TikTok',
           'Colaboraciones con marcas en el canal de moda de Patri Barbero: comunidad hispanohablante, mayoritariamente femenina, que busca estilo con identidad. Estadísticas actualizadas y formatos.', '/influencer/',
           '<link rel="stylesheet" href="/assets/influencer.css">')
inf += header('inf')
inf += f'''<main id="main">
<section class="cover">
  <div class="wrap">
    {switch('inf')}
    <div class="cv">
      <div class="cv-left">
        <p class="label rose rv">Influencer · Moda como identidad</p>
        <h1 class="display cv-title rv d1">Vestirse<br>también es<br><span class="serif">construirse.</span></h1>
        <p class="lead rv d2">Hablo de moda para mujeres que quieren entender qué se lleva, qué transmite y cómo llevarlo siendo ellas. Cuando una marca entra en mis vídeos, <b>entra como parte de esa conversación</b>, no como un anuncio.</p>
        <div class="rv d3" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn rose" href="#propuesta">Proponer una colaboración {ARR}</a><a class="btn line" href="#datos">Ver estadísticas</a></div>
      </div>
      <figure class="cv-mag rv d1">
        <img src="/img/hero.jpg" alt="Patri Barbero" width="1100" height="1467" fetchpriority="high">
        <p class="cl cl1"><b data-n="youtube.suscriptores" data-f="k1">–</b><span>suscriptores<br>en YouTube</span></p>
        <p class="cl cl2"><b data-n="youtube.audiencia.mujeres" data-f="pct0">–</b><span>de mi audiencia<br>son mujeres</span></p>
        <p class="cl cl3"><b data-n="youtube.vis" data-f="k1">–</b><span>visualizaciones<br>en 28 días</span></p>
        <span class="issue">N.º <span data-date="actualizado" data-fmt="short">–</span></span>
      </figure>
    </div>
  </div>
</section>
{marquee(['Tendencias','Estilo personal','Identidad','Autoestima','Moda real'])}

<section class="sec-pad" id="contenido">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rose rv">Mi contenido</p><h2 class="sec rv d1" style="margin-top:14px">De qué <span class="serif">hablo</span></h2></div>
      <p class="lead rv d2">Cuatro temas que se cruzan en casi todos mis vídeos. Por eso tu producto encaja cuando aporta algo a uno de ellos.</p></div>
    <div class="swatches">
      <article class="sw s1 rv"><span class="code">TEMA 01</span><h3>Tendencias, con criterio</h3><p>Qué se lleva, de dónde viene y qué transmite, sin repetir lo mismo que todo el mundo.</p></article>
      <article class="sw s2 rv d1"><span class="code">TEMA 02</span><h3>Estilo personal</h3><p>Cómo adaptar una prenda a ti: proporciones, combinaciones y versiones para distintos días.</p></article>
      <article class="sw s3 rv d2"><span class="code">TEMA 03</span><h3>Identidad y autoestima</h3><p>La ropa como forma de decir quién eres y de sentirte cómoda siendo tú.</p></article>
      <article class="sw s4 rv d3"><span class="code">TEMA 04</span><h3>Moda real</h3><p>Ir mona sin sufrir: comodidad, situaciones reales y prendas que de verdad se usan.</p></article>
    </div>
    <div class="reels-head"><h3>Vídeos que representan mi canal</h3><p class="note">Cifras orgánicas acumuladas a <span data-date="trabajos.fecha">–</span></p></div>
    <div class="reels">{reels}</div>
  </div>
</section>

<section class="sec-pad dark" id="datos">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rv">Comunidad y estadísticas</p><h2 class="sec rv d1" style="margin-top:14px">Mi comunidad, <span class="serif">en datos</span></h2></div>
      <p class="lead rv d2">Datos de YouTube Studio y Metricool. Actualizados el <b style="color:#fff" data-date="actualizado">–</b> · últimos 28 días (<span data-per="periodo.desde|periodo.hasta">–</span>).</p></div>
    <div class="kpis rv">
      <div class="kpi"><span class="pf"><svg class="i"><use href="#yt"/></svg>YouTube</span><b data-n="youtube.suscriptores" data-f="int">–</b><span>suscriptores</span><small><b data-n="youtube.vis" data-f="k1">–</b> visualizaciones · <b data-n="youtube.netos" data-f="k1" data-pre="+">–</b> suscriptores en 28 días</small></div>
      <div class="kpi"><span class="pf"><svg class="i"><use href="#ig"/></svg>Instagram</span><b data-n="instagram.seguidores" data-f="int">–</b><span>seguidores</span><small><b data-n="instagram.reproducciones" data-f="k1">–</b> reproducciones de Reels · <b data-n="instagram.interaccion" data-f="pct1">–</b> interacción</small></div>
      <div class="kpi"><span class="pf"><svg class="i"><use href="#tt"/></svg>TikTok</span><b data-n="tiktok.seguidores" data-f="int">–</b><span>seguidores</span><small><b data-n="tiktok.vistas" data-f="k1">–</b> vistas en 28 días</small></div>
    </div>
    <div class="dgrid">
      <div class="panel rv">
        <h3>Visualizaciones de cada Short</h3><p class="note">Shorts publicados en el periodo · la línea marca la mediana</p>
        <div class="cols" id="c-shorts"></div>
        <p class="tip" id="c-tip" aria-live="polite">Pasa el dedo o el ratón por las barras.</p>
      </div>
      <div class="panel rv d1">
        <h3>Quién me ve en YouTube</h3><p class="note">Espectadores con sesión iniciada · <span data-per="youtube.audiencia.desde|youtube.audiencia.hasta">–</span></p>
        <div class="gender"><div class="gbar"><i style="width:0" data-w="youtube.audiencia.mujeres"></i></div><p><b data-n="youtube.audiencia.mujeres" data-f="pct1">–</b> mujeres</p></div>
        <div class="a2"><div><p class="label">Edad</p><ul class="bars" data-bars="youtube.audiencia.edad" data-hi="25–34"></ul></div>
        <div><p class="label">Países</p><ul class="bars" data-bars="youtube.audiencia.paises" data-hi="ES"></ul></div></div>
      </div>
    </div>
    <p class="note rv" style="margin-top:20px;color:#BFA9B8">Las plataformas no se suman entre sí porque miden cosas distintas. Contenido en español para una comunidad hispanohablante, sobre todo de España y Latinoamérica.</p>
  </div>
</section>

<section class="sec-pad" id="formatos">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rose rv">Cómo colaboramos</p><h2 class="sec rv d1" style="margin-top:14px">Formatos</h2></div>
      <p class="lead rv d2">Cada colaboración se adapta a lo que la marca quiere contar. Estos son los formatos más habituales.</p></div>
    <ol class="fmts">
      <li class="rv"><span>01</span><div><h3>Integración en vídeo largo</h3><p>Tu producto dentro de un vídeo de YouTube, en los primeros minutos y explicado en contexto.</p></div></li>
      <li class="rv d1"><span>02</span><div><h3>Vídeo dedicado</h3><p>Un vídeo completo construido alrededor de tu producto o tu campaña.</p></div></li>
      <li class="rv d2"><span>03</span><div><h3>Shorts, Reels y TikTok</h3><p>Piezas cortas nativas de cada plataforma, con una idea clara y gancho desde el primer segundo.</p></div></li>
      <li class="rv d3"><span>04</span><div><h3>Eventos y experiencias</h3><p>Lanzamientos, talleres o presentaciones contados desde dentro, como el vlog con Modibodi o el taller de colorimetría.</p></div></li>
    </ol>
    <div class="collabs rv">
      <p class="label">Colaboraciones publicadas en mi canal</p>
      <ul class="clist">{clist}</ul>
      <div class="cfloat" aria-hidden="true"><img alt=""></div>
    </div>
  </div>
</section>

<section class="sec-pad" id="propuesta" style="padding-top:0">
  <div class="wrap order">
    <div class="order-aside">
      <p class="label rose rv">Propuesta</p>
      <h2 class="sec rv d1">¿Lo <span class="serif">hacemos?</span></h2>
      <p class="lead rv d2">Cuéntame la campaña en tres pasos. Te respondo en 24–48 h laborables con disponibilidad, enfoque y presupuesto.</p>
      <ul class="rv d3"><li>Contenido en español: subtítulos automáticos y traducción del audio al inglés desde YouTube.</li><li>Revisión del contenido antes de publicar.</li><li>Las tarifas dependen del formato, la plataforma y el uso.</li></ul>
    </div>
    {inf_form}
  </div>
</section>
</main>
'''
inf += contact('Hablemos de <span class="serif">tu campaña.</span>', '¿Prefieres escribirme directamente? Aquí tienes mi correo y mis redes.')
inf += foot('<script src="/datos.js" defer></script><script src="/assets/stats.js" defer></script>')
write('influencer/index.html', inf)

# ============================================================ UGC
ugc_form = form('UGC', 'Pedir contenido UGC', 'Solicitud UGC', [
  ('Tu marca y producto', '<div class="f2">' + fld('Marca', '<input type="text" name="empresa" required autocomplete="organization" data-msg="¿Qué marca es?">') + fld('Web o tienda', '<input type="text" name="web" placeholder="marca.com">') + '</div>'
     + fld('Producto o servicio', '<textarea name="producto" required placeholder="Qué es, a quién va dirigido y qué quieres destacar" data-msg="Cuéntame qué producto o servicio es."></textarea>')),
  ('Qué necesitas', opts('Tipo de contenido', 'tipo', ['Vídeo de producto', 'Hablando a cámara', 'Unboxing', 'Tutorial o demo', 'Lifestyle', 'Fotos de producto', 'Aún no lo sé'], True)
     + '<div class="f2">' + fld('Número de piezas', '<select name="piezas"><option>1</option><option>2–3</option><option>4–6</option><option>Más de 6</option><option>No lo sé aún</option></select>')
     + fld('¿Dónde se usará?', '<select name="uso"><option>Redes de la marca (orgánico)</option><option>Anuncios (publicidad de pago)</option><option>Las dos cosas</option><option>Web o tienda online</option><option>No lo sé aún</option></select>') + '</div>'
     + '<div class="f2">' + fld('Plazo', '<input type="text" name="plazo" placeholder="p. ej. antes del 15 de diciembre">') + fld('Presupuesto orientativo', '<select name="presupuesto"><option value="">Prefiero hablarlo</option><option>Menos de 200 €</option><option>200–500 €</option><option>500–1.000 €</option><option>Más de 1.000 €</option></select>', 'opcional') + '</div>'),
  CONTACT_SET])

rack = ''.join(f'''<button class="hanger rv d{i%3}" type="button" data-yt="{y}" data-title="{t}"><span class="hook" aria-hidden="true"></span>
  <span class="hv"><img src="/img/{im}" alt="" loading="lazy" width="480" height="853"><span class="pl"><i><svg><use href="#play"/></svg></i></span></span>
  <span class="ht"><span class="chip own">Contenido propio</span><b>{t}</b><small>{s}</small></span></button>''' for i, (y, im, t, s) in enumerate([
    ('MKhsAIKXquk', 'broches.jpg', 'Vuelven los broches', 'Hablando a cámara · producto en mano'),
    ('u0GktqmTMh8', 'oversized.jpg', 'Oversized y femenina', 'Prueba de looks · antes y después'),
    ('wu2mG4YX1dI', 'abc.jpg', 'Elige A, B o C', 'Formato interactivo · retención'),
  ]))
rack += ''.join(f'''<button class="hanger wide rv d{i%3}" type="button" data-yt="{y}" data-wide="1" data-title="{t}"><span class="hook" aria-hidden="true"></span>
  <span class="hv"><img src="/img/{y}.jpg" alt="" loading="lazy" width="640" height="360"><span class="pl"><i><svg><use href="#play"/></svg></i></span></span>
  <span class="ht"><span class="chip collab">Colaboración en mis redes</span><b>{t}</b><small>{s}</small></span></button>''' for i, (y, t, s) in enumerate([
    ('gKLj2hae2ww', 'Vivaia · calzado cómodo', 'Integración con producto en uso real'),
    ('pYXWRYBJd9s', 'The Colour Nook · taller', 'Experiencia contada en vídeo'),
  ]))

ugc = head('Creadora UGC en España · Vídeos para marcas | Patri Barbero',
           'Vídeo UGC para marcas de moda, belleza, lifestyle, alimentación, apps y servicios: contenido para redes y anuncios, con entregables, revisiones y derechos de uso claros.', '/ugc/',
           '<link rel="stylesheet" href="/assets/ugc.css">')
ugc += header('ugc')
ugc += f'''<main id="main">
<section class="ugc-hero">
  <div class="wrap">
    {switch('ugc')}
    <div class="uh">
      <h1 class="display uh-title rv">Contenido<br>que tu marca<br>puede <span class="serif">usar</span><br>mañana.</h1>
      <div class="uh-side rv d2">
        <p class="lead">Vídeos UGC pensados para funcionar en tus redes y en tus anuncios: <b>gancho en el primer segundo, producto en contexto y un mensaje claro</b>. No dependen de mis seguidores, sino de cómo está contado.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><a class="btn rose" href="#pedir">Pedir contenido {ARR}</a><a class="btn line" href="#portfolio">Ver portfolio</a></div>
        <p class="note" style="margin-top:18px">Moda · belleza · lifestyle · alimentación · apps y servicios</p>
      </div>
    </div>
  </div>
</section>

<section class="sec-pad" id="portfolio" style="padding-top:clamp(24px,4vw,48px)">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rose rv">Portfolio</p><h2 class="sec rv d1" style="margin-top:14px">El <span class="serif">perchero</span></h2></div>
      <p class="lead rv d2">Una selección de piezas que enseñan cómo grabo, edito y cuento un producto. Cada una indica qué es: encargo UGC, colaboración en mis redes o contenido propio.</p></div>
  </div>
  <div class="rack-x" tabindex="0" aria-label="Portfolio, desliza para ver más"><div class="rail-x" aria-hidden="true"></div><div class="hangers">{rack}</div></div>
  <div class="wrap">
    <div class="legend rv"><span class="chip collab">Colaboración en mis redes</span><span class="chip own">Contenido propio</span></div>
    <div class="brands rv"><p class="label">He creado contenido UGC para</p>
      <div class="logos"><img src="/img/logo_miravia.svg" alt="Miravia"><img src="/img/logo_modibodi.svg" alt="Modibodi"><img src="/img/logo_perfumerias.png" alt="Perfumerías.com" class="dk"><img src="/img/logo_eggo.jpg" alt="Eggo"><img src="/img/logo_impress.svg" alt="Impress"><img src="/img/logo_matchaflix.svg" alt="Matchaflix"><img src="/img/logo_matchaandco.svg" alt="Matcha &amp; Co" class="tall"><img src="/img/logo_acelero.jpg" alt="Acelero"></div>
    </div>
  </div>
</section>

<section class="sec-pad dark">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rv">Servicios</p><h2 class="sec rv d1" style="margin-top:14px">Qué <span class="serif">produzco</span></h2></div>
      <p class="lead rv d2">Cada pieza se entrega lista para publicar, en vertical 9:16 y con una ronda de revisión incluida.</p></div>
    <div class="care">
      <article class="lbl rv"><p class="c-top"><span>01</span><span>15–45 s</span></p><h3>Vídeo de producto</h3><p>El producto en uso, con gancho, beneficio y llamada a la acción.</p><p class="c-comp">Ideal para: anuncios y redes</p></article>
      <article class="lbl rv d1"><p class="c-top"><span>02</span><span>20–60 s</span></p><h3>Hablando a cámara</h3><p>Testimonio o explicación en primera persona, natural y creíble.</p><p class="c-comp">Ideal para: anuncios de conversión</p></article>
      <article class="lbl rv d2"><p class="c-top"><span>03</span><span>30–60 s</span></p><h3>Unboxing y primeras impresiones</h3><p>La experiencia de recibir y probar el producto por primera vez.</p><p class="c-comp">Ideal para: lanzamientos y ecommerce</p></article>
      <article class="lbl rv"><p class="c-top"><span>04</span><span>30–90 s</span></p><h3>Tutorial o demo</h3><p>Cómo se usa, paso a paso, para resolver dudas antes de comprar.</p><p class="c-comp">Ideal para: apps, belleza y servicios</p></article>
      <article class="lbl rv d1"><p class="c-top"><span>05</span><span>15–30 s</span></p><h3>Lifestyle</h3><p>El producto dentro de un momento real: un outfit, una mañana, un plan.</p><p class="c-comp">Ideal para: moda y marca</p></article>
      <article class="lbl rv d2"><p class="c-top"><span>06</span><span>Pack</span></p><h3>Fotos de producto</h3><p>Fotografías en contexto para redes, web o fichas de producto.</p><p class="c-comp">Ideal para: catálogo y redes</p></article>
    </div>
    <div class="extras rv"><p class="label">Extras bajo petición</p>
      <ul><li>Variaciones de gancho para test A/B</li><li>Versión con y sin subtítulos</li><li>Formatos 1:1 y 4:5</li><li>Material bruto</li><li>Derechos para anuncios por periodo</li><li>Exclusividad por categoría y periodo</li><li>Entrega urgente</li></ul></div>
  </div>
</section>

<section class="sec-pad">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rose rv">Proceso</p><h2 class="sec rv d1" style="margin-top:14px">Del brief <span class="serif">a la entrega</span></h2></div>
      <p class="lead rv d2">Un proceso corto y claro para que sepas en todo momento qué pasa y qué te toca.</p></div>
    <ol class="flow">
      <li class="rv"><b>Brief</b><p>Me cuentas producto, objetivo y dónde se usará el contenido.</p></li>
      <li class="rv d1"><b>Propuesta</b><p>Te envío enfoque, entregables, plazos, derechos de uso y presupuesto cerrado.</p></li>
      <li class="rv d2"><b>Producto</b><p>Me envías el producto o el acceso al servicio.</p></li>
      <li class="rv d3"><b>Ideas y guion</b><p>Te paso los ganchos y el guion antes de grabar.</p></li>
      <li class="rv"><b>Grabación y edición</b><p>Grabo, edito, subtitulo y adapto a cada formato.</p></li>
      <li class="rv d1"><b>Entrega</b><p>Recibes los archivos finales con una ronda de revisión incluida.</p></li>
    </ol>
    <div class="terms rv">
      <div><h3>Siempre por escrito</h3><p>Antes de empezar acordamos qué se entrega, cuántas revisiones incluye y durante cuánto tiempo y en qué canales puedes usar el contenido.</p></div>
      <div><h3>Uso en anuncios</h3><p>El uso en publicidad de pago y la exclusividad se acuerdan por periodo. Nada de derechos ilimitados por defecto.</p></div>
      <div><h3>Tarifas</h3><p>Presupuesto a medida según número de piezas, complejidad, uso y plazos.</p></div>
    </div>
  </div>
</section>

<section class="sec-pad" id="pedir" style="padding-top:0">
  <div class="wrap order">
    <div class="order-aside">
      <p class="label rose rv">Pedir contenido</p>
      <h2 class="sec rv d1">Cuéntame <span class="serif">tu producto.</span></h2>
      <p class="lead rv d2">Con esta información te preparo una propuesta y un presupuesto cerrado.</p>
      <ul class="rv d3"><li>Respuesta en 24–48 h laborables.</li><li>Propuesta con entregables, plazos y derechos de uso.</li><li>Una ronda de revisión incluida.</li></ul>
    </div>
    {ugc_form}
  </div>
</section>
</main>
'''
ugc += contact('¿Hacemos <span class="serif">algo bonito?</span>', 'Si prefieres escribirme directamente, aquí tienes mi correo.')
ugc += foot('<script src="/assets/rack.js" defer></script>')
write('ugc/index.html', ugc)

# ============================================================ COMMUNITY MANAGER
cm_form = form('CM', 'Gestión de redes', 'Gestión de redes', [
  ('Tu negocio', '<div class="f2">' + fld('Nombre del negocio', '<input type="text" name="empresa" required autocomplete="organization" data-msg="¿Cómo se llama tu negocio?">') + fld('Sector', '<input type="text" name="sector" placeholder="Cafetería, centro de belleza, tienda online…">') + '</div>'
     + '<div class="f2">' + fld('Ciudad', '<input type="text" name="ciudad" placeholder="Madrid, remoto…">') + fld('Tus redes', '<input type="text" name="redes" placeholder="@tunegocio">') + '</div>'),
  ('Qué necesitas', opts('Objetivo principal', 'objetivo', ['Que me conozcan más', 'Atraer clientes', 'Vender online', 'Ordenar y ser constante', 'Profesionalizar la imagen'], True)
     + opts('Redes', 'plataformas', ['Instagram', 'TikTok', 'Las dos'], True)
     + opts('¿Tienes fotos y vídeos?', 'materiales', ['Sí, os los paso', 'Algunos', 'No, necesito que se graben'], True, 'radio')
     + '<div class="f2">' + fld('¿Cuándo te gustaría empezar?', '<input type="text" name="inicio" placeholder="p. ej. enero">') + fld('Presupuesto mensual orientativo', '<select name="presupuesto"><option value="">Prefiero hablarlo</option><option>Menos de 400 €/mes</option><option>400–600 €/mes</option><option>600–900 €/mes</option><option>Más de 900 €/mes</option></select>', 'opcional') + '</div>'),
  CONTACT_SET])

cm = head('Community manager en Madrid · Gestión de redes para negocios | Patri Barbero',
          'Gestión de redes sociales para pequeños negocios y marcas: estrategia, calendario, diseño, edición de vídeo, copys, publicación y seguimiento mensual. Madrid y remoto.', '/community-manager/',
          '<link rel="stylesheet" href="/assets/cm.css">')
cm += header('cm')
pieces = [('A', 'Análisis', 'Revisamos tus redes, tu competencia y lo que ya funciona.'),
          ('B', 'Estrategia', 'Definimos objetivos, tono, temas y formatos para tu negocio.'),
          ('C', 'Calendario', 'Planificamos el mes: qué se publica, cuándo y con qué objetivo.'),
          ('D', 'Creación', 'Diseño de publicaciones, edición de vídeo y copys.'),
          ('E', 'Publicación', 'Programo y publico. Tú solo apruebas.'),
          ('F', 'Medición', 'Informe mensual con lo que ha funcionado y qué ajustamos.')]
pat = ''.join(f'<li class="pc rv d{i%4}" style="--i:{i}"><span class="notch" aria-hidden="true"></span><span class="pl">PIEZA {k}</span><h3>{t}</h3><p>{d}</p><span class="cut" aria-hidden="true">✂</span></li>' for i, (k, t, d) in enumerate(pieces))
cm += f'''<main id="main">
<section class="cm-hero">
  <div class="wrap">
    {switch('cm')}
    <div class="ch">
      <h1 class="display ch-title rv">Tus redes,<br><span class="serif">a medida</span><br>y con método.</h1>
      <div class="ch-side rv d2">
        <p class="lead">Gestiono las redes de pequeños negocios y marcas para que publiquen con estrategia y constancia, sin que tengas que pensar cada día qué subir. <b>Tú te ocupas de tu negocio; yo, de que se vea.</b></p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><a class="btn rose" href="#empezar">Quiero empezar {ARR}</a><a class="btn line" href="#metodo">Ver cómo trabajo</a></div>
        <p class="note" style="margin-top:18px">Desde Madrid · también en remoto</p>
      </div>
    </div>
  </div>
</section>

<section class="sec-pad" id="metodo" style="padding-top:clamp(24px,4vw,48px)">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rose rv">Método</p><h2 class="sec rv d1" style="margin-top:14px">El <span class="serif">patrón</span></h2></div>
      <p class="lead rv d2">Como un patrón de costura: seis piezas que encajan entre sí. Cada mes las repasamos para que tus redes se ajusten a lo que necesita tu negocio.</p></div>
    <ol class="pattern">{pat}</ol>
  </div>
</section>

<section class="sec-pad dark">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rv">Un mes conmigo</p><h2 class="sec rv d1" style="margin-top:14px">Así nos <span class="serif">organizamos</span></h2></div>
      <p class="lead rv d2">Un ritmo fijo para que siempre sepas qué toca y nada se publique sin tu visto bueno.</p></div>
    <div class="month">
      <div class="wk rv"><span>Semana 1</span><h3>Plan</h3><p>Reunión corta, calendario del mes y lista de materiales que necesito.</p></div>
      <div class="wk rv d1"><span>Semana 2</span><h3>Creación</h3><p>Diseño, edición y copys de las publicaciones del mes.</p></div>
      <div class="wk rv d2"><span>Semana 3</span><h3>Aprobación</h3><p>Te paso todo junto para revisar. Una ronda de cambios incluida.</p></div>
      <div class="wk rv d3"><span>Semana 4</span><h3>Publicación e informe</h3><p>Programo, publico y te envío el resumen de resultados.</p></div>
    </div>
  </div>
</section>

<section class="sec-pad">
  <div class="wrap">
    <div class="sec-head"><div><p class="label rose rv">Claridad</p><h2 class="sec rv d1" style="margin-top:14px">Qué <span class="serif">incluye</span></h2></div>
      <p class="lead rv d2">Hay planes según el volumen de publicaciones, stories y redes. El presupuesto se ajusta a tu negocio.</p></div>
    <div class="incl">
      <div class="col rv"><h3>Incluye</h3><ul><li>Estrategia y calendario editorial mensual</li><li>Diseño de publicaciones y edición de vídeo</li><li>Copys y hashtags</li><li>Programación y publicación</li><li>Stories según el plan</li><li>Informe mensual y ajustes</li></ul></div>
      <div class="col rv d1"><h3>No incluye</h3><ul><li>Desplazamientos para grabar o fotografiar <small>se presupuestan aparte</small></li><li>Publicidad de pago <small>gestión opcional, presupuesto aparte</small></li><li>Atención al cliente por mensaje directo</li><li>Cambios ilimitados</li></ul></div>
      <div class="col rv d2"><h3>Necesito de ti</h3><ul><li>Fotos y vídeos de tu negocio, o acceso para grabarlos</li><li>Acceso a tus redes</li><li>Una persona de contacto que apruebe</li><li>Novedades y promociones con antelación</li></ul></div>
    </div>
    <div class="honest rv"><p><b>Con quién trabajas.</b> Soy creadora de contenido, con formación en Digital Business (ESIC) y experiencia en comunicación y en una agencia de influencer marketing. Gestiono mis propias redes cada semana y aplico el mismo método a las de tu negocio. Trabajo con pocos clientes a la vez para poder dedicarles el tiempo que necesitan.</p></div>
  </div>
</section>

<section class="sec-pad" id="empezar" style="padding-top:0">
  <div class="wrap order">
    <div class="order-aside">
      <p class="label rose rv">Empezar</p>
      <h2 class="sec rv d1">Cuéntame <span class="serif">tu negocio.</span></h2>
      <p class="lead rv d2">Con esto te propongo un plan y un presupuesto mensual a medida.</p>
      <ul class="rv d3"><li>Respuesta en 24–48 h laborables.</li><li>Sin permanencias largas: empezamos con un periodo de prueba.</li><li>Plazas limitadas cada mes.</li></ul>
    </div>
    {cm_form}
  </div>
</section>
</main>
'''
cm += contact('¿Ponemos tus redes <span class="serif">en orden?</span>', 'También puedes escribirme directamente.')
cm += foot()
write('community-manager/index.html', cm)

# ============================================================ 404
e404 = head('Página no encontrada · Patri Barbero', 'Esta página no existe.', '/404')
e404 += header('')
e404 += f'''<main id="main" class="e404"><div class="wrap">
  <p class="label rose">Error 404</p>
  <h1 class="display" style="font-size:clamp(48px,10vw,140px);margin:14px 0 18px">Esta talla<br><span class="serif" style="color:var(--rose)">no la tenemos.</span></h1>
  <p class="lead">La página que buscas no existe o ha cambiado de sitio. Prueba por aquí:</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:24px"><a class="btn ink" href="/">Inicio {ARR}</a><a class="btn line" href="/influencer/">Influencer</a><a class="btn line" href="/ugc/">UGC</a><a class="btn line" href="/community-manager/">Community manager</a></div>
</div></main>
<style>.e404{{padding:clamp(60px,10vw,140px) 0}}</style>
'''
e404 += foot()
write('404.html', e404)

write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in ['/', '/influencer/', '/ugc/', '/community-manager/']) + '</urlset>\n')
write('_redirects', '/media-kit /influencer/ 301\n/media-kit/ /influencer/ 301\n/gestion-redes /community-manager/ 301\n')
print('ok')
