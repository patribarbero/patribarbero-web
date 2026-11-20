#!/usr/bin/env python3
"""Maqueta navegable de la arquitectura multipágina (RIBETE 1.3, baja fidelidad) · v2 (20/11/2026).
Genera páginas reales con URL propia para validar navegación antes del diseño."""
import pathlib, re, subprocess
R = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://patribarbero.com'
_main = subprocess.run(['git', '-C', str(R), 'show', 'origin/main:index.html'], capture_output=True, text=True).stdout
EMAIL = re.search(r'mailto:([^"?]+)', _main).group(1)

# Menú: Contenido · Estadísticas · Trabaja conmigo ▾ · Sobre mí · [Contacto]
SERV = [('/colaboraciones/', 'Colaboraciones', 'Tu marca en mis vídeos de YouTube, Reels y TikTok', 'colab'),
        ('/ugc/', 'UGC', 'Vídeos para las redes y anuncios de tu marca', 'ugc'),
        ('/gestion-de-redes/', 'Gestión de redes', 'Llevo las redes de tu negocio', 'redes')]

CSS = '''
@font-face{font-family:'Anton';src:url('/assets/f/Anton.ttf') format('truetype');font-display:swap}
@font-face{font-family:'Rubik';src:url('/assets/f/Rubik.ttf') format('truetype');font-weight:300 900;font-display:swap}
:root{--le:#FFF5F1;--w:#fff;--ch:#2B140C;--fr:#FF5C9D;--co:#2346FF;--ma:#FFE15A;--ni:#FFD3E4;--gr:#7A665E;color-scheme:light only}
*{box-sizing:border-box}
body{margin:0;background:var(--le);color:var(--ch);font:400 17px/1.55 'Rubik',system-ui,sans-serif;overflow-x:hidden}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.proto{background:var(--ch);color:var(--le);font-size:13px;text-align:center;padding:7px 14px}
.proto b{color:var(--ma)}
header{position:sticky;top:0;z-index:20;background:rgba(255,245,241,.95);backdrop-filter:blur(8px);border-bottom:1px solid rgba(43,20,12,.08)}
.nav{display:flex;align-items:center;gap:16px;height:68px}
.logo{font-family:'Anton';font-size:26px;text-decoration:none;text-transform:uppercase;white-space:nowrap}
.logo span{color:var(--fr)}
.links{display:flex;align-items:center;gap:2px;margin:0 0 0 auto;padding:0;list-style:none}
.links>li{position:relative}
.links a,.links .dd{display:block;text-decoration:none;font:600 15px 'Rubik';padding:10px 12px;border-radius:10px;position:relative;background:none;border:0;color:var(--ch);cursor:pointer}
.links a:hover,.links .dd:hover{background:var(--w)}
.links [aria-current=page]::after,.links .dd.cur::after{content:"";position:absolute;left:12px;right:12px;bottom:3px;height:7px;background:linear-gradient(var(--fr) 0 2.5px,transparent 2.5px 4.5px,var(--co) 4.5px 7px)}
.dd::before{content:"";float:right;width:7px;height:7px;margin:6px 0 0 8px;border-right:2px solid;border-bottom:2px solid;transform:rotate(45deg)}
.sub{position:absolute;top:calc(100% + 8px);left:-8px;width:330px;background:var(--w);border-radius:22px;box-shadow:0 18px 40px rgba(43,20,12,.16);padding:10px;list-style:none;margin:0;display:none}
.sub.open{display:block}
.sub a{padding:12px 14px;border-radius:12px}
.sub a b{display:block;font-size:15.5px}
.sub a small{display:block;font-weight:400;color:var(--gr);font-size:13.5px;margin-top:2px}
.sub a[aria-current=page]{background:var(--le)}
.sub a[aria-current=page]::after{display:none}
.sub .all{border-top:1px solid rgba(43,20,12,.08);margin-top:6px;padding-top:12px;font-size:14px;color:var(--co)}
.menu{display:none;margin-left:auto;border:0;background:var(--ch);color:var(--le);font:600 15px 'Rubik';padding:10px 16px;border-radius:999px;cursor:pointer}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:0 22px;border-radius:999px;font:600 16px 'Rubik';text-decoration:none;border:0;cursor:pointer}
.btn.p{background:var(--fr);color:var(--ch)}
.btn.s{background:var(--w);box-shadow:inset 0 0 0 2px var(--ch)}
:focus-visible{outline:3px solid var(--co);outline-offset:3px;border-radius:8px}
.m-only{display:none}
@media (max-width:960px){
 .links{display:none;position:absolute;top:68px;left:0;right:0;flex-direction:column;align-items:stretch;background:var(--le);padding:8px 16px 20px;border-bottom:1px solid rgba(43,20,12,.1);max-height:calc(100vh - 68px);overflow:auto}
 .links.open{display:flex}.links a,.links .dd{font-size:18px;padding:13px 8px;text-align:left;width:100%}
 .dd{pointer-events:none}.dd::before{display:none}
 .sub{position:static;display:block;width:auto;box-shadow:none;background:transparent;padding:0 0 0 10px}
 .sub a{padding:10px 8px}.sub a small{display:none}
 .menu{display:block}.nav>.btn{display:none}.m-only{display:block}
}
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
.blk .tag{justify-self:start;font-size:12px;font-weight:600;padding:5px 10px;border-radius:999px}
.blk .tag.ok{background:#E3F3E6}.blk .tag.prop{background:var(--ni)}.blk .tag.pend{background:var(--ma)}
.blk.hero{background:var(--w);border-style:solid;border-color:transparent;box-shadow:0 10px 28px rgba(43,20,12,.08)}
.links-int{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.links-int a{font-weight:600;font-size:14.5px;color:var(--co)}
footer{border-top:1px solid rgba(43,20,12,.08);padding:28px 0 48px;color:var(--gr);font-size:14px}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px 22px;justify-content:space-between}
footer nav{display:flex;flex-wrap:wrap;gap:14px}
footer a{text-decoration:none}
/* portada con texto orbital */
.home-hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:center;margin-bottom:30px}
.home-hero .lead{font-size:clamp(19px,2vw,23px);line-height:1.4;max-width:30ch;margin:20px 0 26px}
.home-hero .ctas{display:flex;gap:12px;flex-wrap:wrap}
.orb-wrap{position:relative;display:grid;place-items:center}
.orb{--H:min(78vh,108vw,820px);position:relative;height:var(--H);width:calc(var(--H)*.78);font-size:calc(var(--H)/100)}
.orb .me{position:absolute;left:50%;bottom:0;height:94%;width:auto;transform:translateX(-50%);z-index:2;filter:drop-shadow(0 1.4em 1.6em rgba(43,20,12,.14));pointer-events:none}
.orb .scene{position:absolute;inset:0;perspective:calc(var(--H)*3.2);perspective-origin:50% 44%;pointer-events:none}
.orb .back{z-index:1}.orb .front{z-index:3}
.orb .tilt{position:absolute;left:50%;top:44%;width:0;height:0;transform-style:preserve-3d;transform:rotateX(-14deg) rotateZ(-4deg)}
.orb .ring-f,.orb .ring-b{position:absolute;left:0;top:0;transform-style:preserve-3d;will-change:transform}
.orb .l{position:absolute;left:0;top:0;transform-style:preserve-3d;font:400 var(--fs,11em)/1 'Anton',Impact,sans-serif;text-transform:uppercase;white-space:pre}
.orb .l>i{display:block;font-style:normal;transform:translate(-50%,-50%);backface-visibility:hidden;-webkit-backface-visibility:hidden}
.orb .front .l>i{color:var(--fr);text-shadow:0 0 .06em rgba(43,20,12,.25)}
.orb .back .l>i{color:var(--ch);opacity:.85;transform:translate(-50%,-50%) rotateY(180deg)}
.orb-pause{position:absolute;right:8px;bottom:8px;z-index:5;border:0;border-radius:999px;background:var(--w);color:var(--ch);font:600 14px 'Rubik';padding:9px 14px;box-shadow:0 6px 18px rgba(43,20,12,.14);cursor:pointer}
@media (max-width:860px){.home-hero{grid-template-columns:1fr}.orb-wrap{order:-1}}
'''

def nav(key):
    def a(h, t, k): return f'<li><a href="{h}"' + (' aria-current="page"' if k == key else '') + f'>{t}</a></li>'
    sub = ''.join(f'<li><a href="{h}"' + (' aria-current="page"' if k == key else '') + f'><b>{t}</b><small>{d}</small></a></li>' for h, t, d, k in SERV)
    cur = ' cur' if key in ('colab', 'ugc', 'redes', 'trabaja') else ''
    return (f'<li class="m-only"><a href="/"' + (' aria-current="page"' if key == 'home' else '') + '>Inicio</a></li>'
            + a('/contenido/', 'Contenido', 'cont') + a('/estadisticas/', 'Estadísticas', 'stats')
            + f'<li><button class="dd{cur}" type="button" aria-expanded="false" aria-controls="sub">Trabaja conmigo</button>'
            + f'<ul class="sub" id="sub">{sub}<li><a class="all" href="/trabaja-conmigo/"' + (' aria-current="page"' if key == 'trabaja' else '') + '>Ver las tres opciones →</a></li></ul></li>'
            + a('/sobre-mi/', 'Sobre mí', 'sobre') + f'<li class="m-only"><a href="/contacto/"' + (' aria-current="page"' if key == 'contacto' else '') + '>Contacto</a></li>')

JS = '''(function(){var m=document.querySelector('.menu'),l=document.getElementById('links');m.addEventListener('click',function(){var o=l.classList.toggle('open');m.setAttribute('aria-expanded',o);m.textContent=o?'Cerrar':'Menú'});
var d=document.querySelector('.dd'),s=document.getElementById('sub');d.addEventListener('click',function(e){e.stopPropagation();var o=s.classList.toggle('open');d.setAttribute('aria-expanded',o)});
document.addEventListener('click',function(e){if(!s.contains(e.target)&&innerWidth>960){s.classList.remove('open');d.setAttribute('aria-expanded',false)}});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){s.classList.remove('open');d.setAttribute('aria-expanded',false);d.focus()}});})();'''

def page(path, key, title, desc, h1, crumbs, goal, blocks, noindex=False, hero='', scripts=''):
    cr = ' › '.join(f'<a href="{h}">{t}</a>' for h, t in crumbs) if crumbs else ''
    g = ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in goal)
    rob = '<meta name="robots" content="noindex">' if noindex else ''
    head = hero if hero else f'<h1 class="T">{h1}</h1>'
    html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light only">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}">{rob}
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/img/og.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>{CSS}</style></head>
<body>
<div class="proto">Maqueta de <b>arquitectura</b> v2 (RIBETE 1.3, baja fidelidad). No es la web publicada.</div>
<header><nav class="wrap nav" aria-label="Principal"><a class="logo" href="/" aria-label="Patri Barbero, inicio">Patri <span>Barbero</span></a>
<button class="menu" type="button" aria-expanded="false" aria-controls="links">Menú</button>
<ul class="links" id="links">{nav(key)}</ul><a class="btn p" href="/contacto/">Contacto</a></nav></header>
<main id="main"><div class="wrap">
{('<p class="crumbs">' + cr + '</p>') if cr else ''}
{head}
<div class="goal">{g}</div>
<div class="blocks">{blocks}</div>
</div></main>
<footer><div class="wrap"><span>© Patri Barbero · Moda como identidad</span>
<nav aria-label="Pie"><a href="/estadisticas/">Estadísticas</a><a href="/colaboraciones/">Colaboraciones</a><a href="/ugc/">UGC</a><a href="/gestion-de-redes/">Gestión de redes</a><a href="/contacto/">Contacto</a><a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad</a></nav></div></footer>
<script>{JS}</script>{scripts}
</body></html>'''
    out = R / 'index.html' if path == '/' else (R / path.strip('/') if path.endswith('.html') else R / path.strip('/') / 'index.html')
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)

def B(title, text, tag='prop', hero=False, links=None):
    t = {'ok': 'Existe / aprobado', 'prop': 'Propuesta', 'pend': 'Pendiente de datos o validación'}[tag]
    li = ('<div class="links-int">' + ''.join(f'<a href="{h}">{x} →</a>' for h, x in links) + '</div>') if links else ''
    return f'<section class="blk{" hero" if hero else ""}"><span class="tag {tag}">{t}</span><h2>{title}</h2><p>{text}</p>{li}</section>'

CRUMB_T = ('/trabaja-conmigo/', 'Trabaja conmigo')

# ---------- INICIO (con el texto orbital real) ----------
HERO = '''<div class="home-hero">
 <div><h1 class="T" style="font-size:clamp(56px,9vw,120px)">Patri<br>Barbero</h1>
  <p class="lead">Te enseño a vestirte sporty sin dejar de sentirte femenina, en YouTube, Instagram y TikTok.</p>
  <div class="ctas"><a class="btn p" href="/trabaja-conmigo/">Trabaja conmigo</a><a class="btn s" href="/contenido/">Ver mi contenido</a></div></div>
 <div class="orb-wrap"><div class="orb" data-phrase="Moda como identidad" data-reps="2" data-dur="26" aria-hidden="true">
  <div class="scene back"><div class="tilt"><div class="ring-b"></div></div></div>
  <img class="me" src="/img/patri-espejo-1100.webp" srcset="/img/patri-espejo-1100.webp 432w, /img/patri-espejo-1800.webp 708w" sizes="(max-width:860px) 45vw, 330px" alt="" width="708" height="1800" fetchpriority="high">
  <div class="scene front"><div class="tilt"><div class="ring-f"></div></div></div>
 </div><button class="orb-pause" type="button" aria-pressed="false">❚❚ Pausar</button><span class="sr" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Moda como identidad</span></div>
</div>'''
page('/', 'home', 'Patri Barbero · Moda sporty y femenina', 'Creadora de contenido de moda: te enseño a vestirte sporty sin dejar de sentirte femenina. YouTube, Instagram y TikTok.',
  'Patri Barbero', None,
  [('Para quién', 'Cualquier visitante: comunidad, marcas, negocios.'), ('Objetivo', 'Entender quién soy en 5 segundos y elegir puerta.'), ('Acción principal', 'Trabaja conmigo o Ver mi contenido.')],
  B('Portada con el texto orbital', '«Moda como identidad», fresa delante y chocolate detrás, sobre tu foto real del espejo (esto de arriba ya es el prototipo funcionando). Con botón de pausa y versión fija para «reducir movimiento».', 'prop', True)
  + B('Cuatro carpetas de tela (segunda puerta)', 'Ver mi contenido · Colaboraciones · UGC · Gestión de redes. Complementan al menú, no lo sustituyen.', 'prop', links=[('/contenido/', 'Contenido'), ('/colaboraciones/', 'Colaboraciones'), ('/ugc/', 'UGC'), ('/gestion-de-redes/', 'Gestión de redes')])
  + B('Datos rápidos', '3 cifras verificadas con fecha y un botón «Ver estadísticas».', 'ok', links=[('/estadisticas/', 'Estadísticas')])
  + B('Último vídeo de YouTube', 'Una ventana con la miniatura y el título del último vídeo.', 'prop', links=[('/contenido/', 'Todo el contenido')]),
  hero=HERO, scripts='<script src="/assets/orbital.js" defer></script>')

page('/contenido/', 'cont', 'Mi contenido · Patri Barbero', 'Vídeos de moda sporty y femenina en YouTube, Reels y TikTok: tendencias con filtro, cómo combinar e identidad.',
  'Mi contenido', [('/', 'Inicio'), ('/contenido/', 'Contenido')],
  [('Para quién', 'Comunidad nueva y marcas que quieren ver cómo trabajo.'), ('Objetivo', 'Enseñar el contenido real y llevar a los canales.'), ('Acción principal', 'Suscribirse en YouTube / seguir en IG y TikTok.')],
  B('Tres pilares', 'Tendencias pasadas por el filtro · Cómo combinar · Identidad y comunidad, con 2–3 piezas reales cada uno.', 'ok', True)
  + B('YouTube', 'Último vídeo y más vistos (vídeo nuevo cada domingo). El vídeo solo se carga al pulsar.', 'prop')
  + B('Reels y TikTok', '4–6 piezas verticales y enlaces a los perfiles.', 'prop')
  + B('Para marcas', '«¿Quieres aparecer en mis vídeos?» → Colaboraciones.', 'prop', links=[('/colaboraciones/', 'Colaboraciones')]))

page('/estadisticas/', 'stats', 'Estadísticas y media kit · Patri Barbero', 'Estadísticas verificadas de YouTube, Instagram y TikTok de Patri Barbero: comunidad, audiencia y alcance, con fecha de actualización.',
  'Estadísticas', [('/', 'Inicio'), ('/estadisticas/', 'Estadísticas')],
  [('Para quién', 'Marcas y agencias (sobre todo para colaboraciones) y quien tenga curiosidad.'), ('Objetivo', 'Mostrar los datos reales en un sitio fácil de encontrar y de enviar.'), ('Acción principal', 'Descargar el media kit o ir a Colaboraciones.')],
  B('Resumen por plataforma', 'YouTube, Instagram y TikTok: seguidores y visualizaciones de los últimos 28 días, con fuente y fecha («Actualizado el …»).', 'ok', True)
  + B('Audiencia', 'Edad, país y género de cada plataforma, con datos nativos.', 'pend')
  + B('Rendimiento reciente', 'Gráfica de cada Short / Reel del periodo y mediana. Sin sumar plataformas entre sí.', 'ok')
  + B('Media kit en PDF', 'Descarga generada desde esta misma página, con las mismas cifras.', 'pend')
  + B('Siguiente paso', 'Botones a Colaboraciones y Contacto.', 'prop', links=[('/colaboraciones/', 'Colaboraciones'), ('/contacto/?tipo=colaboracion', 'Pedir propuesta')]))

page('/trabaja-conmigo/', 'trabaja', 'Trabaja conmigo · Patri Barbero', 'Tres formas de trabajar con Patri Barbero: colaboraciones en sus redes, contenido UGC para tu marca y gestión de redes para negocios.',
  'Trabaja conmigo', [('/', 'Inicio'), CRUMB_T],
  [('Para quién', 'Cualquier marca, agencia o negocio que aún no sabe qué necesita.'), ('Objetivo', 'Que elija en 5 segundos la opción que le encaja.'), ('Acción principal', 'Entrar en una de las tres páginas.')],
  B('¿Qué necesita tu marca?', 'Tres opciones grandes, cada una con una frase y un ejemplo: «Quiero aparecer en tus vídeos» (Colaboraciones) · «Quiero vídeos para mis redes o anuncios» (UGC) · «Quiero que lleves mis redes» (Gestión de redes).', 'prop', True, links=[(h, t) for h, t, d, k in SERV])
  + B('¿No lo tienes claro?', 'Escríbeme y te digo qué opción te encaja.', 'prop', links=[('/contacto/', 'Contacto')]))

page('/colaboraciones/', 'colab', 'Colaboraciones con marcas · Patri Barbero', 'Tu marca en los vídeos de Patri Barbero en YouTube, Reels y TikTok: comunidad de mujeres de 15 a 35 años que busca vestir sporty y femenina.',
  'Colaboraciones', [('/', 'Inicio'), CRUMB_T, ('/colaboraciones/', 'Colaboraciones')],
  [('Para quién', 'Marcas y agencias que quieren aparecer en mis redes. Es la URL que envías al proponer una colaboración.'), ('Objetivo', 'Que entiendan valor, audiencia y formatos sin salir de la página.'), ('Acción principal', 'Pedir propuesta (contacto con «colaboración» marcado).')],
  B('Propuesta de valor', 'Quién soy en 2 líneas + promesa + foto real. Funciona aunque sea la primera página que ven.', 'ok', True)
  + B('Tu audiencia en un vistazo', '3–4 cifras clave y audiencia resumida, con enlace a Estadísticas para el detalle y el PDF.', 'ok', links=[('/estadisticas/', 'Estadísticas completas')])
  + B('Formatos', 'Integración en YouTube · vídeo dedicado · Reels/TikTok · eventos y experiencias. Sin tarifas públicas.', 'ok')
  + B('Experiencia', 'Vivaia, The Colour Nook y Modibodi como prueba de experiencia, con su vídeo; pequeño, no como catálogo.', 'ok')
  + B('Cómo trabajamos', 'Me escribes → te propongo → creamos → publicación.', 'ok', links=[('/contacto/?tipo=colaboracion', 'Pedir propuesta')]))

page('/ugc/', 'ugc', 'Contenido UGC para marcas · Patri Barbero', 'Vídeo UGC para las redes y anuncios de tu marca: formatos, portfolio, proceso y derechos de uso claros.',
  'Contenido UGC', [('/', 'Inicio'), CRUMB_T, ('/ugc/', 'UGC')],
  [('Para quién', 'Marcas que quieren vídeo para sus canales o anuncios, no publicación en mis redes.'), ('Objetivo', 'Demostrar que sé grabar y contar un producto.'), ('Acción principal', 'Pedir contenido (contacto con «UGC» marcado).')],
  B('Qué es y para quién', 'Contenido para tus canales; no depende de mis seguidores. Sin estadísticas de mis redes aquí: no son lo que compras.', 'ok', True)
  + B('Portfolio', 'Vídeos etiquetados: encargo UGC · colaboración en mis redes · contenido propio. Faltan encargos UGC que se puedan enseñar.', 'pend')
  + B('Formatos y extras', 'Vídeo de producto, a cámara, unboxing, tutorial, lifestyle, fotos. Derechos para anuncios y exclusividad por periodo.', 'prop')
  + B('Proceso', 'Brief → propuesta → producto → guion → grabación y edición → entrega con una revisión.', 'prop', links=[('/contacto/?tipo=ugc', 'Pedir contenido')]))

page('/gestion-de-redes/', 'redes', 'Gestión de redes sociales para negocios · Patri Barbero', 'Gestión de redes para pequeños negocios y marcas: estrategia, calendario, diseño, vídeo, copys, publicación e informe mensual. Madrid y remoto.',
  'Gestión de redes', [('/', 'Inicio'), CRUMB_T, ('/gestion-de-redes/', 'Gestión de redes')],
  [('Para quién', 'Negocios (cafeterías, centros de belleza, tiendas, ecommerce) que necesitan a alguien para sus redes.'), ('Objetivo', 'Transmitir confianza con método, sin inventar clientes.'), ('Acción principal', 'Pedir presupuesto (contacto con «redes» marcado).')],
  B('Qué hago por tu negocio', 'Estrategia, calendario, diseño de publicaciones, edición de vídeo, copys, publicación e informe mensual.', 'prop', True)
  + B('Método', 'Análisis → estrategia → calendario → creación → publicación → medición, explicado de forma visual.', 'prop')
  + B('Un mes de trabajo', 'Semana 1 plan · 2 creación · 3 aprobación · 4 publicación e informe.', 'prop')
  + B('Qué incluye y qué no', 'Incluye / no incluye (desplazamientos y anuncios aparte) / qué necesito de ti. Sin precios públicos.', 'prop')
  + B('Con quién trabajas', 'Formación y experiencia reales; trabajo con pocos clientes a la vez. Casos reales cuando los haya.', 'pend', links=[('/contacto/?tipo=redes', 'Pedir presupuesto')]))

page('/sobre-mi/', 'sobre', 'Sobre mí · Patri Barbero', 'Quién es Patri Barbero, cómo entiende la moda (sporty y femenina a la vez) y su trayectoria en marketing digital e influencer marketing.',
  'Sobre mí', [('/', 'Inicio'), ('/sobre-mi/', 'Sobre mí')],
  [('Para quién', 'Comunidad, marcas y empresas que miran mi perfil profesional.'), ('Objetivo', 'Confianza: quién soy, desde dónde hablo y qué sé hacer.'), ('Acción principal', 'Contacto o Trabaja conmigo.')],
  B('Quién soy', 'Foto flotante real + texto corto en primera persona. Territorio: sporty y femenina a la vez.', 'ok', True)
  + B('Cómo hablo de moda', 'Qué se lleva, qué transmite, por qué ahora, qué identidad construye, cómo llevarlo siendo tú.', 'ok')
  + B('Trayectoria profesional', 'Digital Business (ESIC), comunicación en González Byass, agencia de influencer marketing (sin nombrar clientes ni usar sus materiales).', 'ok', links=[('/contacto/', 'Contacto')]))

page('/contacto/', 'contacto', 'Contacto · Patri Barbero', 'Escríbeme para colaboraciones, contenido UGC o gestión de redes. Respuesta en 24–48 h laborables.',
  'Hablemos', [('/', 'Inicio'), ('/contacto/', 'Contacto')],
  [('Para quién', 'Quien ya sabe que quiere escribir.'), ('Objetivo', 'Recibir solicitudes completas.'), ('Acción principal', 'Enviar el formulario.')],
  B('Formulario con tipo', 'Me interesa: colaboración · UGC · gestión de redes · otra cosa. Llega ya marcado desde cada página y las preguntas cambian según el tipo.', 'prop', True)
  + B('Envío', 'Hoy abre el correo de la persona. Propuesta: envío directo desde Cloudflare con antispam (necesita tu aprobación).', 'pend')
  + B('Email y redes', f'{EMAIL} · YouTube · Instagram · TikTok. Sin teléfono ni tarifas.', 'ok'))

page('/aviso-legal/', '', 'Aviso legal · Patri Barbero', 'Aviso legal de patribarbero.com.', 'Aviso legal', [('/', 'Inicio')],
  [('Obligatorio', 'Web con actividad comercial en España.'), ('Falta', 'Nombre, NIF y datos de contacto que quieras publicar.'), ('Estado', 'Pendiente')],
  B('Texto legal', 'Se redacta cuando tenga tus datos identificativos.', 'pend'), noindex=True)
page('/privacidad/', '', 'Privacidad · Patri Barbero', 'Política de privacidad de patribarbero.com.', 'Privacidad', [('/', 'Inicio')],
  [('Obligatorio', 'Hay formulario y vídeos incrustados.'), ('Falta', 'Responsable del tratamiento.'), ('Estado', 'Pendiente')],
  B('Texto de privacidad', 'Formularios, YouTube sin cookies hasta pulsar, sin analítica con cookies.', 'pend'), noindex=True)
page('/404.html', '', 'Página no encontrada · Patri Barbero', 'Esta página no existe.', 'Esta talla no la tenemos', [('/', 'Inicio')],
  [('Qué pasa', 'La dirección no existe.'), ('Qué ofrecer', 'Volver a las páginas principales.'), ('Tono', 'Con humor, en mi voz.')],
  B('Volver', 'Enlaces a Inicio, Estadísticas, Trabaja conmigo y Contacto.', 'prop', links=[('/', 'Inicio'), ('/estadisticas/', 'Estadísticas'), ('/trabaja-conmigo/', 'Trabaja conmigo'), ('/contacto/', 'Contacto')]), noindex=True)

# páginas de la v1 de la maqueta que desaparecen
import shutil
for old in ('marcas',):
    shutil.rmtree(R / old, ignore_errors=True)

(R / '_redirects').write_text('\n'.join([
  '/media-kit /estadisticas/ 301', '/media-kit/ /estadisticas/ 301',
  '/marcas /trabaja-conmigo/ 301', '/marcas/ /trabaja-conmigo/ 301', '/marcas/ugc/ /ugc/ 301',
  '/influencer /colaboraciones/ 301', '/influencer/ /colaboraciones/ 301',
  '/community-manager /gestion-de-redes/ 301', '/community-manager/ /gestion-de-redes/ 301', '']))
(R / 'robots.txt').write_text('User-agent: *\nDisallow: /laboratorio/\nSitemap: https://patribarbero.com/sitemap.xml\n')
(R / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in ['/', '/contenido/', '/estadisticas/', '/trabaja-conmigo/', '/colaboraciones/', '/ugc/', '/gestion-de-redes/', '/sobre-mi/', '/contacto/']) + '</urlset>\n')
print('ok')
