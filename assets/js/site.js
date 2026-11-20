/* Patri Barbero · interacciones comunes */
(function(){
  document.documentElement.classList.remove('no-js');
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EN = document.documentElement.lang === 'en';
  function L(es, en){ return EN ? en : es; }

  /* cabecera */
  var top = document.querySelector('.top');
  if (top) addEventListener('scroll', function(){ top.classList.toggle('sc', scrollY > 6); }, {passive:true});
  function hdr(){ if (top) document.documentElement.style.setProperty('--hdr', Math.round(top.getBoundingClientRect().height) + 'px'); }
  hdr(); addEventListener('resize', hdr);

  /* menú móvil */
  var menu = document.querySelector('.menu'), links = document.getElementById('links');
  if (menu && links){
    menu.addEventListener('click', function(){
      var o = links.classList.toggle('open');
      menu.setAttribute('aria-expanded', o); menu.textContent = o ? L('Cerrar', 'Close') : L('Menú', 'Menu');
      document.body.style.overflow = o ? 'hidden' : '';
    });
  }

  /* desplegable «Trabaja conmigo» */
  var dd = document.querySelector('.dd'), sub = document.getElementById('sub');
  if (dd && sub){
    function set(o){ sub.classList.toggle('open', o); dd.setAttribute('aria-expanded', o); }
    dd.addEventListener('click', function(e){ e.stopPropagation(); set(!sub.classList.contains('open')); });
    /* en ordenador se abre al pasar el ratón, sin clicar */
    var li = dd.parentNode, hov = matchMedia('(hover:hover) and (min-width:981px)'), t;
    li.addEventListener('mouseenter', function(){ if (hov.matches){ clearTimeout(t); set(true); } });
    li.addEventListener('mouseleave', function(){ if (hov.matches) t = setTimeout(function(){ set(false); }, 180); });
    li.addEventListener('focusout', function(e){ if (!li.contains(e.relatedTarget)) set(false); });
    document.addEventListener('click', function(e){ if (!sub.contains(e.target)) set(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && sub.classList.contains('open')){ set(false); dd.focus(); } });
  }

  /* aparición suave al hacer scroll */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !RM){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); }, {rootMargin:'0px 0px -6% 0px'});
    rv.forEach(function(el){ io.observe(el); });
  } else rv.forEach(function(el){ el.classList.add('in'); });

  /* pestañas */
  document.querySelectorAll('[role=tablist]').forEach(function(tl){
    var tabs = tl.querySelectorAll('[role=tab]');
    tabs.forEach(function(t){ t.addEventListener('click', function(){
      tabs.forEach(function(x){ var on = x === t; x.setAttribute('aria-selected', on); document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
    }); });
  });

  /* vídeos: se cargan solo al pulsar (YouTube sin cookies) */
  var vd = document.getElementById('vd');
  if (vd){
    var frame = vd.querySelector('.frame');
    document.addEventListener('click', function(e){
      var b = e.target.closest('[data-yt]'); if (!b || !vd.showModal) return;
      e.preventDefault();
      frame.classList.toggle('v', b.dataset.v === '1');
      frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + b.dataset.yt + '?autoplay=1&rel=0&playsinline=1" title="' + (b.dataset.title || L('Vídeo', 'Video')) + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
      vd.showModal();
    });
    vd.querySelector('.x').addEventListener('click', function(){ vd.close(); });
    vd.addEventListener('click', function(e){ if (e.target === vd || e.target.classList.contains('box')) vd.close(); });
    vd.addEventListener('close', function(){ frame.innerHTML = ''; });
  }

  /* imprimir / guardar media kit en PDF */
  document.querySelectorAll('[data-print]').forEach(function(b){ b.addEventListener('click', function(){ window.print(); }); });

  /* formulario de contacto: valida los obligatorios y envía el mensaje al email de Patri */
  var f = document.getElementById('contact');
  if (f){
    var tipo = new URLSearchParams(location.search).get('tipo');
    var map = {colaboracion:'Colabora en mis redes', ugc:'Contenido UGC', redes:'Gestión de redes', otra:'Otra cosa'};
    var sector = f.querySelector('select[name=sector]'), otro = f.querySelector('[data-otro]');
    function sync(){
      var v = (f.querySelector('input[name=tipo]:checked') || {}).value || '';
      f.querySelectorAll('[data-for]').forEach(function(g){ var on = g.dataset.for.split('|').indexOf(v) > -1; g.hidden = !on; g.querySelectorAll('input,select,textarea').forEach(function(i){ i.disabled = !on; }); });
      if (otro){ var o = !sector.disabled && sector.selectedIndex === sector.options.length - 1; otro.hidden = !o; otro.querySelector('input').disabled = !o; }
    }
    if (tipo && map[tipo]){ var r = f.querySelector('input[name=tipo][value="' + map[tipo] + '"]'); if (r) r.checked = true; }
    f.querySelectorAll('input[name=tipo]').forEach(function(r){ r.addEventListener('change', sync); });
    if (sector) sector.addEventListener('change', sync);
    sync();
    var err = f.querySelector('.err'), btn = f.querySelector('[type=submit]'), btnHTML = btn.innerHTML;
    function fields(){ return [].slice.call(f.querySelectorAll('input,select,textarea')).filter(function(i){ return !i.disabled && i.name !== 'web_site'; }); }
    f.addEventListener('input', function(e){ var el = e.target.closest('.fld,.consent,.opts'); if (el) el.classList.remove('bad'); err.textContent = ''; });
    f.addEventListener('change', function(e){ var el = e.target.closest('.fld,.consent'); if (el) el.classList.remove('bad'); });
    function compose(){
      var d = new FormData(f), lines = [], seen = {};
      f.querySelectorAll('[name]').forEach(function(el){
        var n = el.name; if (seen[n] || el.disabled || n === 'web_site' || n === 'acepto') return; seen[n] = 1;
        var v = d.getAll(n).filter(Boolean).join(', ');
        var lab = el.closest('[data-label]'); lines.push({k: lab ? lab.dataset.label : n, v: v || '—'});
      });
      return {d: d, lines: lines, subject: 'Web' + (EN ? ' (EN)' : '') + ' · ' + (d.get('tipo') || 'Contacto') + ' · ' + (d.get('empresa') || d.get('nombre') || '')};
    }
    function fail(m, why){
      if (why && console) console.warn('Formulario:', why);
      var to = f.dataset.to, body = m.lines.map(function(l){ return l.k + ': ' + l.v; }).join('\n');
      var box = document.getElementById('fail'); f.hidden = true; box.hidden = false; box.focus();
      var det = box.querySelector('.why'); if (det) det.textContent = why ? L('Detalle técnico: ', 'Technical detail: ') + why : '';
      box.querySelector('[data-mail]').href = 'mailto:' + to + '?subject=' + encodeURIComponent(m.subject) + '&body=' + encodeURIComponent(body);
      box.querySelector('[data-copy]').onclick = function(){
        var t = L('Para: ', 'To: ') + to + L('\nAsunto: ', '\nSubject: ') + m.subject + '\n\n' + body;
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(function(){ box.querySelector('.note').textContent = L('Copiado. Pégalo en un correo a ', 'Copied. Paste it into an email to ') + to + '.'; });
      };
    }
    f.addEventListener('submit', function(e){
      e.preventDefault(); err.textContent = '';
      if (f.querySelector('.hp input').value) return;              // robot: no se envía
      f.querySelectorAll('.bad').forEach(function(x){ x.classList.remove('bad'); });
      var bad = fields().filter(function(i){ if (i.type === 'text' || i.type === 'email' || i.tagName === 'TEXTAREA') i.value = i.value.trim(); return !i.checkValidity(); });
      var names = {}; bad = bad.filter(function(i){ if (names[i.name]) return false; names[i.name] = 1; return true; });
      if (bad.length){
        bad.forEach(function(i){ var w = i.type === 'radio' ? i.closest('.opts') : i.closest('.fld,.consent'); if (w) w.classList.add('bad'); i.setAttribute('aria-invalid', 'true'); });
        err.textContent = (bad[0].dataset.msg || L('Revisa este campo, por favor.', 'Please check this field.')) + (bad.length > 1 ? L(' Te faltan ', ' ') + bad.length + L(' campos obligatorios.', ' required fields are missing.') : '');
        bad[0].focus(); return;
      }
      fields().forEach(function(i){ i.removeAttribute('aria-invalid'); });
      var m = compose(), payload = {};
      m.lines.forEach(function(l){ payload[l.k] = l.v; });
      payload._subject = m.subject; payload._replyto = m.d.get('email'); payload._template = 'table'; payload._captcha = 'false';
      btn.disabled = true; btn.textContent = L('Enviando…', 'Sending…');
      fetch('https://formsubmit.co/ajax/' + f.dataset.to, {method: 'POST', headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}, body: JSON.stringify(payload)})
        .then(function(r){ return r.json().then(function(j){ return {ok: r.ok, j: j}; }); })
        .then(function(x){
          if (x.ok && String(x.j.success) === 'true'){ var done = document.getElementById('done'); f.hidden = true; done.hidden = false; done.focus(); }
          else fail(m, x.j && x.j.message);
        })
        .catch(function(e){ fail(m, 'conexión: ' + (e && e.message || e)); })
        .then(function(){ btn.disabled = false; btn.innerHTML = btnHTML; });
    });
  }
})();
