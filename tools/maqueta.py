#!/usr/bin/env python3
"""Maqueta navegable de la arquitectura multipágina (RIBETE 1.3, baja fidelidad).
Genera páginas reales con URL propia para validar navegación antes del diseño."""
import pathlib, re, subprocess
R = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://patribarbero.com'
_main = subprocess.run(['git', '-C', str(R), 'show', 'origin/main:index.html'], capture_output=True, text=True).stdout
EMAIL = re.search(r'mailto:([^"?]+)', _main).group(1)

NAV = [('/', 'Inicio', 'home'), ('/sobre-mi/', 'Sobre mí', 'sobre'), ('/contenido/', 'Contenido', 'cont'), ('/marcas/', 'Marcas', 'marcas'), ('/contacto/', 'Contacto', 'contacto')]

CSS = '''
@font-face{font-family:'Anton';src:url('/assets/f/Anton.ttf') format('truetype');font-display:swap}
@font-face{font-family:'Rubik';src:url('/assets/f/Rubik.ttf') format('truetype');font-weight:300 900;font-display:swap}
:root{--le:#FFF5F1;--w:#fff;--ch:#2B140C;--fr:#FF5C9D;--co:#2346FF;--ma:#FFE15A;--ni:#FFD3E4;--gr:#7A665E;color-scheme:light only}
*{box-sizing:border-box}
html{scroll-padding-top:84px}
body{margin:0;background:var(--le);color:var(--ch);font:400 17px/1.55 'Rubik',system-ui,sans-serif;overflow-x:hidden}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.proto{background:var(--ch);color:var(--le);font-size:13px;text-align:center;padding:7px 14px}
.proto b{color:var(--ma)}
header{position:sticky;top:0;z-index:20;background:rgba(255,245,241,.95);backdrop-filter:blur(8px);border-bottom:1px solid rgba(43,20,12,.08)}
.nav{display:flex;align-items:center;gap:20px;height:68px}
.logo{font-family:'Anton';font-size:26px;text-decoration:none;text-transform:uppercase}
.logo span{color:var(--fr)}
.links{display:flex;gap:4px;margin:0 0 0 auto;padding:0;list-style:none}
.links a{display:block;text-decoration:none;font-weight:600;font-size:15px;padding:10px 12px;border-radius:10px;position:relative}
.links a:hover{background:var(--w)}
.links a[aria-current=page]::after{content:"";position:absolute;left:12px;right:12px;bottom:3px;height:7px;background:linear-gradient(var(--fr) 0 2.5px,transparent 2.5px 4.5px,var(--co) 4.5px 7px)}
.menu{display:none;margin-left:auto;border:0;background:var(--ch);color:var(--le);font:600 15px 'Rubik';padding:10px 16px;border-radius:999px;cursor:pointer}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:0 22px;border-radius:999px;font:600 16px 'Rubik';text-decoration:none;border:0;cursor:pointer}
.btn.p{background:var(--fr);color:var(--ch)}
.btn.s{background:var(--w);box-shadow:inset 0 0 0 2px var(--ch)}
:focus-visible{outline:3px solid var(--co);outline-offset:3px;border-radius:8px}
@media (max-width:860px){.links{display:none;position:absolute;top:68px;left:0;right:0;flex-direction:column;background:var(--le);padding:8px 16px 18px;border-bottom:1px solid rgba(43,20,12,.1)}.links.open{display:flex}.links a{font-size:18px;padding:14px 8px}.menu{display:block}.nav .btn{display:none}}
main{padding:28px 0 64px}
.crumbs{font-size:13.5px;color:var(--gr);margin-bottom:14px}
.crumbs a{text-decoration:none}
.T{font-family:'Anton';text-transform:uppercase;line-height:.92;font-weight:400;margin:0}
h1.T{font-size:clamp(48px,8vw,104px)}
.goal{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:22px 0 30px}
.goal div{background:var(--w);border-radius:12px;padding:14px 16px;font-size:14.5px}
.goal b{display:block;font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--gr);margin-bottom:4px}
@media (max-width:760px){.goal{grid-template-columns:1fr}}
.blocks{display:grid;gap:14px}
.blk{border:2px dashed rgba(43,20,12,.22);border-radius:22px;padding:20px 22px;background:rgba(255,255,255,.55);display:grid;gap:6px;align-content:start}
.blk h2{margin:0;font:700 19px/1.25 'Rubik'}
.blk p{margin:0;color:var(--gr);font-size:15px}
.blk .tag{justify-self:start;font-size:12px;font-weight:600;padding:5px 10px;border-radius:999px;background:var(--ni)}
.blk .tag.ok{background:#E3F3E6}.blk .tag.prop{background:var(--ni)}.blk .tag.pend{background:var(--ma)}
.blk.hero{min-height:220px;background:var(--w);border-style:solid;border-color:transparent;box-shadow:0 10px 28px rgba(43,20,12,.08)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.two{grid-template-columns:1fr}}
.links-int{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.links-int a{font-weight:600;font-size:14.5px;color:var(--co)}
footer{border-top:1px solid rgba(43,20,12,.08);padding:28px 0 48px;color:var(--gr);font-size:14px}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px 22px;justify-content:space-between}
footer nav{display:flex;flex-wrap:wrap;gap:14px}
footer a{text-decoration:none}
'''

def page(path, key, title, desc, h1, crumbs, goal, blocks, noindex=False):
    links = ''.join(f'<li><a href="{h}"' + (' aria-current="page"' if k == key else '') + f'>{t}</a></li>' for h, t, k in NAV)
    cr = ' › '.join(f'<a href="{h}">{t}</a>' for h, t in crumbs) if crumbs else ''
    g = ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in goal)
    rob = '<meta name="robots" content="noindex">' if noindex else ''
    html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light only">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}">{rob}
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/img/og.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>{CSS}</style></head>
<body>
<div class="proto">Maqueta de <b>arquitectura</b> (RIBETE 1.3, baja fidelidad). No es la web publicada.</div>
<header><nav class="wrap nav" aria-label="Principal"><a class="logo" href="/">Patri <span>Barbero</span></a>
<button class="menu" type="button" aria-expanded="false" aria-controls="links">Menú</button>
<ul class="links" id="links">{links}</ul><a class="btn p" href="/marcas/">Colabora conmigo</a></nav></header>
<main id="main"><div class="wrap">
{('<p class="crumbs">' + cr + '</p>') if cr else ''}
<h1 class="T">{h1}</h1>
<div class="goal">{g}</div>
<div class="blocks">{blocks}</div>
</div></main>
<footer><div class="wrap"><span>© Patri Barbero · Moda como identidad</span>
<nav aria-label="Pie"><a href="/marcas/">Marcas</a><a href="/marcas/ugc/">UGC</a><a href="/contacto/">Contacto</a><a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad</a></nav></div></footer>
<script>(function(){{var m=document.querySelector('.menu'),l=document.getElementById('links');m.addEventListener('click',function(){{var o=l.classList.toggle('open');m.setAttribute('aria-expanded',o);m.textContent=o?'Cerrar':'Menú'}})}})();</script>
</body></html>'''
    out = R / path.strip('/') / 'index.html' if path != '/' else R / 'index.html'
    if path.endswith('.html'): out = R / path.strip('/')
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)

def B(title, text, tag='prop', hero=False, links=None):
    t = {'ok': 'Existe / aprobado', 'prop': 'Propuesta', 'pend': 'Pendiente de datos o validación'}[tag]
    li = ('<div class="links-int">' + ''.join(f'<a href="{h}">{x} →</a>' for h, x in links) + '</div>') if links else ''
    return f'<section class="blk{" hero" if hero else ""}"><span class="tag {tag}">{t}</span><h2>{title}</h2><p>{text}</p>{li}</section>'

page('/', 'home', 'Patri Barbero · Moda sporty y femenina', 'Creadora de contenido de moda: te enseño a vestirte sporty sin dejar de sentirte femenina. YouTube, Instagram y TikTok.',
  'Patri Barbero', None,
  [('Para quién', 'Cualquier visitante: comunidad, marcas, curiosos.'), ('Objetivo', 'Entender quién soy en 5 segundos y elegir puerta.'), ('Acción principal', 'Ir a Marcas o a Contenido.')],
  B('Portada con la foto del espejo', 'Nombre en Anton + promesa «Te enseño a vestirte sporty sin dejar de sentirte femenina» + dos botones (Soy una marca · Ver mi contenido). Candidata para el texto orbital 3D: es el único sitio donde el efecto tiene sentido como firma.', 'prop', True)
  + B('Tres carpetas de tela (segunda puerta)', 'Conocerme · Ver contenido · Colaborar. Complementan al menú, no lo sustituyen.', 'ok', links=[('/sobre-mi/', 'Sobre mí'), ('/contenido/', 'Contenido'), ('/marcas/', 'Marcas')])
  + B('Datos rápidos verificados', '3 cifras con fuente y fecha (suscriptores, visualizaciones, seguidores). Salen del mismo archivo de datos que Marcas.', 'ok')
  + B('Último vídeo de YouTube', 'Una ventana con la miniatura y el título del último vídeo.', 'prop', links=[('/contenido/', 'Todo el contenido')])
  + B('Banda para marcas', 'Una frase y un botón a Marcas. Sin repetir el media kit aquí.', 'prop', links=[('/marcas/', 'Marcas')]))

page('/sobre-mi/', 'sobre', 'Sobre mí · Patri Barbero', 'Quién es Patri Barbero, cómo entiende la moda (sporty y femenina a la vez) y su trayectoria en marketing digital e influencer marketing.',
  'Sobre mí', [('/', 'Inicio'), ('/sobre-mi/', 'Sobre mí')],
  [('Para quién', 'Comunidad y marcas que quieren conocerme mejor; empresas que miran mi perfil profesional.'), ('Objetivo', 'Confianza: quién soy, desde dónde hablo y qué sé hacer.'), ('Acción principal', 'Ir a Contenido o a Marcas.')],
  B('Quién soy', 'Foto flotante real + texto corto en primera persona. Territorio: sporty y femenina a la vez; «no hay que sufrir para ir mona».', 'ok', True)
  + B('Cómo hablo de moda', 'Los 5 pasos de mi diferencial: qué se lleva, qué transmite, por qué ahora, qué identidad construye, cómo llevarlo siendo tú.', 'ok')
  + B('Trayectoria profesional', 'Digital Business (ESIC), comunicación en González Byass, agencia de influencer marketing (sin nombrar clientes ni usar sus materiales). Enlace con ancla interna #trayectoria para compartirlo.', 'ok')
  + B('Lema y cierre', '«Vestirse también es construirse» + botones a Contenido y Marcas.', 'prop', links=[('/contenido/', 'Contenido'), ('/marcas/', 'Marcas')]))

page('/contenido/', 'cont', 'Mi contenido · Patri Barbero', 'Vídeos de moda sporty y femenina en YouTube, Reels y TikTok: tendencias con filtro, cómo combinar e identidad.',
  'Mi contenido', [('/', 'Inicio'), ('/contenido/', 'Contenido')],
  [('Para quién', 'Comunidad nueva y marcas que quieren ver cómo trabajo.'), ('Objetivo', 'Enseñar el contenido real y llevar a los canales.'), ('Acción principal', 'Suscribirse en YouTube / seguir en IG y TikTok.')],
  B('Tres pilares', 'Tendencias pasadas por el filtro · Cómo combinar · Identidad y comunidad. Cada uno con 2–3 piezas reales.', 'ok', True)
  + B('YouTube', 'Pestaña con el último vídeo y los más vistos (vídeo nuevo cada domingo). Ventanas con miniatura; el vídeo se abre al pulsar, no se carga antes.', 'prop')
  + B('Reels y TikTok', 'Pestaña con 4–6 piezas verticales y enlaces a los perfiles.', 'prop')
  + B('Para marcas', 'Una línea: «¿Quieres aparecer en mis vídeos?» → Marcas.', 'prop', links=[('/marcas/', 'Marcas')]))

page('/marcas/', 'marcas', 'Colabora con Patri Barbero · Media kit para marcas', 'Media kit y colaboraciones: comunidad hispanohablante, sobre todo mujeres de 15 a 35 años, que busca vestir sporty y femenina. Datos verificados y formatos.',
  'Trabajemos juntas', [('/', 'Inicio'), ('/marcas/', 'Marcas')],
  [('Para quién', 'Marcas y agencias. Es la URL que envías al proponer una colaboración.'), ('Objetivo', 'Que entiendan valor, audiencia y formatos sin salir de la página.'), ('Acción principal', 'Pedir propuesta (formulario con «marca» ya marcado).')],
  B('Propuesta de valor', 'Quién soy en 2 líneas + promesa + foto real. Funciona aunque sea la primera página que ven.', 'ok', True)
  + B('Media kit integrado', 'Cifras por plataforma con fuente y fecha, audiencia (edad, país, género) y Shorts del periodo. Mismo archivo de datos que hoy. Botón «Descargar PDF» generado desde esta página.', 'pend')
  + B('Formatos', 'Integración en YouTube · vídeo dedicado · Reels/TikTok · eventos y experiencias. Sin tarifas públicas.', 'ok')
  + B('Colaboraciones reales', 'Vivaia, The Colour Nook y Modibodi, con su vídeo. Logos de UGC solo si están autorizados.', 'ok')
  + B('Cómo trabajamos', 'Me escribes → te propongo → creamos → publicación o entrega.', 'ok')
  + B('UGC', 'Tarjeta que lleva a la página propia de UGC (otro comprador, otro portfolio).', 'prop', links=[('/marcas/ugc/', 'UGC')])
  + B('Gestión de redes', 'Solo una línea «también a petición» con enlace a contacto, hasta tener casos reales que enseñar.', 'prop', links=[('/contacto/?tipo=redes', 'Contacto')])
  + B('Contacto', 'Botón a /contacto/?tipo=marca y email directo.', 'prop', links=[('/contacto/?tipo=marca', 'Pedir propuesta')]))

page('/marcas/ugc/', 'marcas', 'Contenido UGC para marcas · Patri Barbero', 'Vídeo UGC para las redes y anuncios de tu marca: formatos, portfolio, proceso y derechos de uso claros.',
  'Contenido UGC', [('/', 'Inicio'), ('/marcas/', 'Marcas'), ('/marcas/ugc/', 'UGC')],
  [('Para quién', 'Marcas que quieren vídeo para sus canales o anuncios, no publicación en mis redes.'), ('Objetivo', 'Demostrar que sé grabar y contar un producto.'), ('Acción principal', 'Pedir contenido (formulario con «UGC» marcado).')],
  B('Qué es y para quién', 'Una frase clara: contenido para tus canales; no depende de mis seguidores.', 'ok', True)
  + B('Portfolio', 'Vídeos etiquetados: encargo UGC · colaboración en mis redes · contenido propio. Faltan encargos UGC que se puedan enseñar.', 'pend')
  + B('Formatos y extras', 'Vídeo de producto, a cámara, unboxing, tutorial, lifestyle, fotos. Derechos para anuncios y exclusividad por periodo.', 'prop')
  + B('Proceso', 'Brief → propuesta → producto → guion → grabación y edición → entrega con una revisión.', 'prop', links=[('/contacto/?tipo=ugc', 'Pedir contenido'), ('/marcas/', 'Volver a Marcas')]))

page('/contacto/', 'contacto', 'Contacto · Patri Barbero', 'Escríbeme para colaboraciones, contenido UGC o gestión de redes. Respuesta en 24–48 h laborables.',
  'Hablemos', [('/', 'Inicio'), ('/contacto/', 'Contacto')],
  [('Para quién', 'Quien ya sabe que quiere escribir.'), ('Objetivo', 'Recibir solicitudes completas.'), ('Acción principal', 'Enviar el formulario.')],
  B('Formulario único con tipo', 'Soy marca · agencia · negocio · otro, y me interesa influencer · UGC · gestión de redes. Llega ya marcado desde cada página (?tipo=). Campos que cambian según el tipo.', 'prop', True)
  + B('Envío', 'Hoy los formularios abren el correo de la persona. Propuesta: envío directo desde Cloudflare con protección antispam. Necesita tu aprobación (servicio de envío de emails).', 'pend')
  + B('Email y redes', f'{EMAIL} · YouTube · Instagram · TikTok. Sin teléfono ni tarifas.', 'ok'))

page('/aviso-legal/', '', 'Aviso legal · Patri Barbero', 'Aviso legal de patribarbero.com.', 'Aviso legal', [('/', 'Inicio')],
  [('Obligatorio', 'Web con actividad comercial en España.'), ('Falta', 'Nombre, NIF y datos de contacto que quieras publicar.'), ('Estado', 'Pendiente')],
  B('Texto legal', 'Se redacta cuando tenga tus datos identificativos.', 'pend'), noindex=True)
page('/privacidad/', '', 'Privacidad · Patri Barbero', 'Política de privacidad de patribarbero.com.', 'Privacidad', [('/', 'Inicio')],
  [('Obligatorio', 'Hay formulario y vídeos incrustados.'), ('Falta', 'Responsable del tratamiento.'), ('Estado', 'Pendiente')],
  B('Texto de privacidad', 'Formularios, YouTube sin cookies hasta pulsar, y sin analítica con cookies.', 'pend'), noindex=True)
page('/404.html', '', 'Página no encontrada · Patri Barbero', 'Esta página no existe.', 'Esta talla no la tenemos', [('/', 'Inicio')],
  [('Qué pasa', 'La dirección no existe.'), ('Qué ofrecer', 'Volver a las páginas principales.'), ('Tono', 'Con humor, en mi voz.')],
  B('Volver', 'Enlaces a Inicio, Contenido, Marcas y Contacto.', 'prop', links=[('/', 'Inicio'), ('/contenido/', 'Contenido'), ('/marcas/', 'Marcas'), ('/contacto/', 'Contacto')]), noindex=True)

(R / '_redirects').write_text('/media-kit /marcas/ 301\n/media-kit/ /marcas/ 301\n/colaboraciones /marcas/ 301\n/colaboraciones/ /marcas/ 301\n/ugc /marcas/ugc/ 301\n/ugc/ /marcas/ugc/ 301\n/influencer /marcas/ 301\n/influencer/ /marcas/ 301\n')
(R / 'robots.txt').write_text('User-agent: *\nDisallow: /laboratorio/\nSitemap: https://patribarbero.com/sitemap.xml\n')
(R / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in ['/', '/sobre-mi/', '/contenido/', '/marcas/', '/marcas/ugc/', '/contacto/']) + '</urlset>\n')
print('ok')
