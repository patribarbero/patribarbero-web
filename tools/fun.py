"""Piezas interactivas de la web: muñequita sporty ↔ femenina, armario del canal y escritorio escondido."""

# ------------------------------------------------------------------ MUÑEQUITA
# Cada prenda dice en qué pasos (0 = muy sporty … 4 = muy femenina) aparece.
SKIN, HAIR, CH, FR, CO, MA, NI, LE = '#F2C6A8', '#5A3825', '#2B140C', '#FF5C9D', '#2346FF', '#FFE15A', '#FFD3E4', '#FFF5F1'

def _g(steps, inner, cls=''):
    return f'<g class="pz {cls}" data-s="{steps}">{inner}</g>'

def _shoe(d, fill, extra=''):
    # zapato izquierdo; el derecho es su reflejo
    return f'<g><path d="{d}" fill="{fill}"/>{extra}</g><g transform="translate(240 0) scale(-1 1)"><path d="{d}" fill="{fill}"/>{extra}</g>'

def _mirror(inner):
    return f'<g>{inner}</g><g transform="translate(240 0) scale(-1 1)">{inner}</g>'

DOLL = f"""<svg class="doll" viewBox="0 0 240 500" role="img" aria-label="Muñequita que cambia de look">
  <ellipse cx="120" cy="478" rx="58" ry="7" fill="rgba(43,20,12,.10)"/>
  <path d="M101 40 Q99 16 120 16 Q141 16 139 40 Q143 74 147 116 Q141 126 132 118 Q131 94 130 70 L110 70 Q109 94 108 118 Q99 126 93 116 Q97 74 101 40 Z" fill="{HAIR}"/>
  <path d="M141 60 Q146 90 147 116" fill="none" stroke="#6E4630" stroke-width="2" opacity=".6"/>
  {_mirror(f'<path d="M95 89 Q86 93 85 112 L82 170 Q79 202 80 232 Q80 247 85 250 Q90 248 89 236 L91 172 L97 124 Z" fill="{SKIN}"/>')}
  <path d="M108 80 Q120 86 132 80 L146 89 Q152 96 148 128 Q142 158 137 176 Q146 198 145 222 L141 300 Q139 336 136 352 L133 452 L125 454 L123 352 Q121 300 121 244 L119 244 Q119 300 117 352 L115 454 L107 452 L104 352 Q101 336 99 300 L95 222 Q94 198 103 176 Q98 158 92 128 Q88 96 94 89 Z" fill="{SKIN}"/>
  <path d="M113 62 h14 v22 q-7 4 -14 0 Z" fill="#E8B596"/>
  <ellipse cx="120" cy="46" rx="18" ry="22" fill="{SKIN}"/>
  <circle cx="113" cy="47" r="5.2" fill="none" stroke="{CH}" stroke-width="1.3"/><circle cx="127" cy="47" r="5.2" fill="none" stroke="{CH}" stroke-width="1.3"/>
  <path d="M118.2 47 h3.6" stroke="{CH}" stroke-width="1.3"/>
  <circle cx="109" cy="56" r="3" fill="{FR}" opacity=".22"/><circle cx="131" cy="56" r="3" fill="{FR}" opacity=".22"/>
  <path d="M116 58 Q120 61.5 124 58" fill="none" stroke="#B5524A" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M101 44 Q102 22 122 22 Q139 24 139.5 44 Q131 30 116 34 Q107 37 101.5 50 Z" fill="{HAIR}"/>
  <path d="M101.5 50 Q98 70 100 92 Q104 86 104 70 Z" fill="{HAIR}"/>

  {_g('0 1', f'<path d="M95 218 L145 218 L141 300 Q139 336 136 352 L134 444 L123 446 L122.5 352 Q121 300 120.5 248 L119.5 248 Q119 300 117.5 352 L117 446 L106 444 L104 352 Q101 336 99 300 Z" fill="{CO}"/><path d="M105 438 h12 v9 h-12z M123 438 h12 v9 h-12z" fill="#1B35C8"/><path d="M98 226 Q101 300 106 440 M142 226 Q139 300 134 440" fill="none" stroke="#fff" stroke-width="2"/><path d="M120 250 Q119 320 118 440" fill="none" stroke="#1B35C8" stroke-width="1.4" opacity=".6"/>', 'jogger')}
  {_g('2 3', f'<path d="M103 172 L137 172 Q150 262 159 372 Q120 384 81 372 Q90 262 103 172 Z" fill="{NI}"/><path d="M112 186 Q108 280 104 374 M128 186 Q133 280 140 374" fill="none" stroke="#fff" stroke-width="2.2" opacity=".75"/><path d="M137 172 Q150 262 159 372 Q150 375 146 376 Q140 270 132 176 Z" fill="#F7B9D2" opacity=".7"/><path d="M102 170 h36 v7 h-36z" fill="#F7B9D2"/>', 'skirt')}
  {_g('4', f'<path d="M104 94 L106 82 M136 94 L134 82" stroke="{FR}" stroke-width="1.8"/><path d="M103 96 Q120 106 137 96 L140 128 Q138 158 137 176 Q148 262 160 384 Q120 396 80 384 Q92 262 103 176 Q102 158 100 128 Z" fill="{FR}"/><path d="M137 176 Q148 262 160 384 Q152 388 146 389 Q141 270 132 180 Z" fill="#E5488A" opacity=".55"/><path d="M114 190 Q110 290 106 386" fill="none" stroke="#fff" stroke-width="1.8" opacity=".35"/><path d="M103 96 Q120 106 137 96" fill="none" stroke="#E5488A" stroke-width="1.6"/>', 'dress')}
  {_g('0 1', f'<path d="M96 86 Q120 78 144 86 L157 96 Q166 112 164 150 L165 230 Q160 237 153 234 L151 160 L150 226 L90 226 L89 160 L87 234 Q80 237 75 230 L76 150 Q74 112 83 96 Z" fill="{CO}"/><path d="M104 84 Q120 108 136 84 Q130 94 120 96 Q110 94 104 84 Z" fill="#1B35C8"/><path d="M116 96 v18 M124 96 v18" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/><path d="M101 190 h38 l3 26 h-44 z" fill="#1B35C8" opacity=".85"/><path d="M90 218 h60 v8 h-60z M75 226 l12 3 v5 q-7 3 -12 -2z M165 226 l-12 3 v5 q7 3 12 -2z" fill="#1B35C8"/><path d="M150 100 Q160 150 157 226" fill="none" stroke="#1B35C8" stroke-width="2" opacity=".5"/>', 'hoodie')}
  {_g('2', f'<path d="M96 86 Q120 78 144 86 L157 96 Q166 112 164 150 L165 230 Q160 237 153 234 L151 160 L148 180 L92 180 L89 160 L87 234 Q80 237 75 230 L76 150 Q74 112 83 96 Z" fill="#CFC6C2"/><path d="M104 84 Q120 106 136 84 Q130 94 120 96 Q110 94 104 84 Z" fill="#B6ABA6"/><path d="M116 96 v16 M124 96 v16" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/><path d="M92 172 h56 v8 h-56z M75 226 l12 3 v5 q-7 3 -12 -2z M165 226 l-12 3 v5 q7 3 12 -2z" fill="#B6ABA6"/><path d="M150 100 Q160 150 157 226" fill="none" stroke="#B6ABA6" stroke-width="2"/>', 'crop')}
  {_g('3', f'<path d="M95 88 Q120 82 145 88 L153 96 Q159 112 157 150 L159 228 Q155 235 150 232 L148 160 L140 178 L100 178 L92 160 L90 232 Q85 235 81 228 L83 150 Q81 112 87 96 Z" fill="{MA}"/><path d="M110 86 L120 116 L130 86 Q120 90 110 86 Z" fill="{SKIN}"/><path d="M120 116 V176" stroke="#E5C53C" stroke-width="1.8"/><circle cx="120" cy="130" r="1.9" fill="{CH}"/><circle cx="120" cy="146" r="1.9" fill="{CH}"/><circle cx="120" cy="162" r="1.9" fill="{CH}"/><path d="M100 172 h40 v6 h-40z M81 222 l9 2 v6 q-6 3 -9 -2z M159 222 l-9 2 v6 q6 3 9 -2z" fill="#E5C53C"/><path d="M98 100 v70 M104 98 v72 M136 98 v72 M142 100 v70" stroke="#E5C53C" stroke-width="1" opacity=".7"/>', 'cardi')}
  {_g('2', f'<path d="M105 418 h12 v34 h-12z M123 418 h12 v34 h-12z" fill="#fff"/><path d="M105 424 h12 M123 424 h12" stroke="{FR}" stroke-width="1.8"/>', 'socks')}
  {_g('0 1 2', _mirror(f'<path d="M99 455 Q100 445 111 446 L118 449 Q129 459 125 474 L96 474 Q93 464 99 455 Z" fill="#fff"/><path d="M95 469 h31" stroke="{CH}" stroke-width="2.2"/><path d="M102 459 Q111 463 120 455" fill="none" stroke="{FR}" stroke-width="2.4" stroke-linecap="round"/><path d="M99 455 Q100 445 111 446" fill="none" stroke="#E7DDD9" stroke-width="1.4"/>'), 'chunky')}
  {_g('3', _mirror(f'<path d="M102 459 Q103 452 111 452 L117 454 Q126 461 122 472 L99 472 Q97 465 102 459 Z" fill="{CH}"/><path d="M104 457 L118 463 M105 463 L117 455" stroke="{NI}" stroke-width="1.6"/><path d="M99 470 h24" stroke="#fff" stroke-width="1.8"/>'), 'sneakerina')}
  {_g('4', _mirror(f'<path d="M103 461 Q104 455 111 455 L116 456 Q123 462 121 470 L101 470 Q99 466 103 461 Z" fill="{CH}"/><path d="M109 459 l-3.5 -2.5 v5z M109 459 l3.5 -2.5 v5z" fill="{FR}"/>'), 'ballet')}
  {_g('0', f'<path d="M100.5 36 Q101 16 120 16 Q139 16 139.5 36 Q120 31 100.5 36 Z" fill="{CO}"/><path d="M134 34 Q152 32 158 40 Q144 42 134 39 Z" fill="#1B35C8"/><circle cx="120" cy="17" r="2.4" fill="#1B35C8"/>', 'cap')}
  {_g('1 2 3 4', f'<circle cx="102" cy="55" r="3.4" fill="none" stroke="#D9A929" stroke-width="1.6"/><circle cx="138" cy="55" r="3.4" fill="none" stroke="#D9A929" stroke-width="1.6"/>', 'hoops')}
  {_g('2 3', f'<path d="M132 22 l-9 -6 v12z M132 22 l9 -6 v12z" fill="{FR}"/><circle cx="132" cy="22" r="2.4" fill="#E5488A"/>', 'bow')}
  {_g('3 4', f'<path d="M110 84 Q120 94 130 84" fill="none" stroke="#D9A929" stroke-width="1.5"/><circle cx="120" cy="89.5" r="2.2" fill="#D9A929"/>', 'necklace')}
  {_g('1', f'<path d="M98 88 L150 196" stroke="{CH}" stroke-width="1.6"/><rect x="142" y="190" width="20" height="15" rx="5" fill="{NI}"/><rect x="149" y="195" width="6" height="2.4" rx="1.2" fill="#D9A929"/>', 'minibag')}
  {_g('4', f'<path d="M154 236 Q161 222 170 236" fill="none" stroke="{CH}" stroke-width="1.8"/><rect x="150" y="236" width="26" height="15" rx="5" fill="{CH}"/><rect x="160" y="240" width="6" height="2.6" rx="1.3" fill="#D9A929"/>', 'bag')}
</svg>"""

STEPS = [  # título, texto, pasa el filtro
    ('100 % sporty', 'Chándal entero y gorra. Muy cómodo, pero le falta un toque que lo haga tuyo.', False),
    ('Base sporty + un toque', 'El mismo chándal con aros dorados y un bolsito: ya no parece que vienes del gimnasio.', True),
    ('Cómoda y mona', 'Sudadera corta, falda satinada y zapatillas con calcetín. Justo aquí está mi estilo.', True),
    ('Base femenina + toque sporty', 'Falda y punto con bailarinas deportivas: femenina sin sufrir.', True),
    ('100 % femenina', 'Vestido y bailarinas. Precioso, pero aquí falta el toque deportivo.', False),
]

def doll_section():
    steps = ''.join(f'<div class="dl-step" data-i="{i}"' + ('' if i == 2 else ' hidden') + f'><span class="chip {"on" if ok else ""}">{"Pasa mi filtro ✓" if ok else "Le falta el toque"}</span><h3 class="T">{t}</h3><p>{x}</p></div>' for i, (t, x, ok) in enumerate(STEPS))
    return f'''<section class="sec tight"><div class="wrap">
  <div class="sec-head"><div><p class="kicker rv">Mi filtro, en juguete</p><h2 class="T h2 rv">Sporty ↔ femenina</h2></div><p class="lead rv">Así pienso cada look: ni 100 % deportivo ni 100 % femenino. Mueve la barra y mira cómo cambia.</p></div>
  <div class="rv">{win_html('mi filtro · probador', f"""<div class="dl">
    <div class="dl-stage" data-step="2">{''.join(f'<img src="/img/muneca/paso{i+1}-560.webp" srcset="/img/muneca/paso{i+1}-560.webp 560w, /img/muneca/paso{i+1}-1024.webp 1024w" sizes="(max-width:760px) 70vw, 420px" width="1024" height="1536" alt="{t}" data-i="{i}"' + (' class="on"' if i == 2 else '') + (' loading="lazy"' if i != 2 else '') + '>' for i, (t, x, ok) in enumerate(STEPS))}</div>
    <div class="dl-side">
      <div class="dl-txt" aria-live="polite">{steps}</div>
      <label class="dl-range"><span class="sr">Nivel de sporty a femenina</span><input type="range" min="0" max="4" step="1" value="2" aria-valuetext="Cómoda y mona"></label>
      <div class="dl-ends"><span>👟 sporty</span><span>🎀 femenina</span></div>
    </div></div>""")}</div>
</div></section>'''

# se rellena desde web.py (para usar su función win sin importarla en círculo)
win_html = None

# ------------------------------------------------------------------ ARMARIO
def closet(types, yt):
    hangers = ''.join(f'''<a class="hanger" href="{yt}/playlists" target="_blank" rel="noopener" style="--d:{i * 90}ms">
      <svg class="hook" viewBox="0 0 60 34" aria-hidden="true"><path d="M30 2 Q38 2 38 9 Q38 14 30 16 L4 30 H56 L30 16" fill="none" stroke="#2B140C" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/></svg>
      <span class="garm"><span class="th">''' + (f'<img src="/img/{img}" alt="" loading="lazy">' if img else '<span class="sw"><i style="background:var(--fr)"></i><i style="background:var(--co)"></i><i style="background:var(--ma)"></i><i style="background:var(--ch)"></i></span>') + f'''</span><span class="chip">{lst}</span><b>{t}</b><small>{d}</small></span></a>''' for i, (lst, t, d, img) in enumerate(types))
    return f'''<div class="closet">
      <div class="cl-in"><div class="rail" aria-hidden="true"></div><div class="hangers">{hangers}</div></div>
      <div class="cl-door l" aria-hidden="true"><span class="knob"></span><span class="cl-tag">armario</span></div>
      <div class="cl-door r" aria-hidden="true"><span class="knob"></span><span class="cl-tag">del canal</span></div>
    </div>'''

# ------------------------------------------------------------------ ESCRITORIO ESCONDIDO
def desk(top_shorts, ficha_items):
    vids = ''.join(f'<a class="dk-vid" href="{("https://www.instagram.com/reel/Df4_yVToCd5/" if k == "ig" else "https://www.youtube.com/shorts/" + ref)}" target="_blank" rel="noopener"><span>' + (f'<img src="/img/{img}" alt="" loading="lazy">' if img else '<i class="vichy"></i>') + f'</span><b>{t}</b></a>' for k, ref, img, t, m in top_shorts)
    ficha = ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in ficha_items)
    def w(id_, title, body, x, y, wdt):
        return f'<section class="dk-win" id="{id_}" style="--x:{x};--y:{y};--ww:{wdt}" hidden><header class="dk-bar"><button class="dk-x" type="button" aria-label="Cerrar"></button><i></i><i></i><b>{title}</b></header><div class="win-rib"></div><div class="dk-body">{body}</div></section>'
    icons = [('/contenido/', 'rayas', 'Contenido'), ('/estadisticas/', 'mante', 'Estadísticas'), ('/colaboraciones/', 'vichy', 'Colabora')]
    ic = ''.join(f'<a class="dk-ico" href="{h}"><span class="mini-fold {p}"></span><span>{t}</span></a>' for h, p, t in icons)
    ic += '<button class="dk-ico" type="button" data-open="dk-ficha"><span class="dk-file">TXT</span><span>ficha.txt</span></button>'
    ic += '<button class="dk-ico" type="button" data-open="dk-vids"><span class="dk-file vid">▶</span><span>lo más visto</span></button>'
    ic += '<button class="dk-ico" type="button" data-open="dk-trash"><span class="dk-file trash">🗑</span><span>papelera</span></button>'
    return f'''<div class="desk" id="desk" hidden role="dialog" aria-modal="true" aria-label="Escritorio de Patri">
  <div class="dk-top"><b>patri os</b><span>moda como identidad</span><span class="dk-clock"></span><button class="dk-exit" type="button">Salir ✕</button></div>
  <div class="dk-icons">{ic}</div>
  {w('dk-hola', 'hola.txt', '<p class="dk-big T">¡Me has encontrado!</p><p>Bienvenida a mi escritorio. Aquí guardo lo que no cabe en el resto de la web.</p><p class="dk-tip">Abre las carpetas y los archivos de la izquierda, arrastra las ventanas por su barra o cotillea la papelera.</p>', '22%', '16%', '520px')}
  {w('dk-ficha', 'ficha.txt', f'<ul class="dk-ficha">{ficha}</ul>', '8%', '30%', '330px')}
  {w('dk-vids', 'lo más visto', f'<div class="dk-vids">{vids}</div>', '56%', '40%', '360px')}
  {w('dk-trash', 'papelera', '<p class="dk-big T">Tendencias sin filtro</p><p>Aquí acaba lo que no pasa mi filtro: lo 100 % gimnasio y lo que hace sufrir para ir mona. 🗑️</p>', '30%', '52%', '300px')}
</div>'''
