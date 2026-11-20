/* Patri Barbero · interacciones comunes */
(function(){
  document.documentElement.classList.remove('no-js');
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* cabecera */
  var top = document.querySelector('.top');
  if (top) addEventListener('scroll', function(){ top.classList.toggle('sc', scrollY > 6); }, {passive:true});

  /* menú móvil */
  var menu = document.querySelector('.menu'), links = document.getElementById('links');
  if (menu && links){
    menu.addEventListener('click', function(){
      var o = links.classList.toggle('open');
      menu.setAttribute('aria-expanded', o); menu.textContent = o ? 'Cerrar' : 'Menú';
      document.body.style.overflow = o ? 'hidden' : '';
    });
  }

  /* desplegable «Trabaja conmigo» */
  var dd = document.querySelector('.dd'), sub = document.getElementById('sub');
  if (dd && sub){
    function set(o){ sub.classList.toggle('open', o); dd.setAttribute('aria-expanded', o); }
    dd.addEventListener('click', function(e){ e.stopPropagation(); set(!sub.classList.contains('open')); });
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
      frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + b.dataset.yt + '?autoplay=1&rel=0&playsinline=1" title="' + (b.dataset.title || 'Vídeo') + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
      vd.showModal();
    });
    vd.querySelector('.x').addEventListener('click', function(){ vd.close(); });
    vd.addEventListener('click', function(e){ if (e.target === vd || e.target.classList.contains('box')) vd.close(); });
    vd.addEventListener('close', function(){ frame.innerHTML = ''; });
  }

  /* imprimir / guardar media kit en PDF */
  document.querySelectorAll('[data-print]').forEach(function(b){ b.addEventListener('click', function(){ window.print(); }); });

  /* formulario de contacto */
  var f = document.getElementById('contact');
  if (f){
    var tipo = new URLSearchParams(location.search).get('tipo');
    var map = {colaboracion:'Colabora en mis redes', ugc:'Contenido UGC', redes:'Gestión de redes'};
    function showGroups(){
      var v = (f.querySelector('input[name=tipo]:checked') || {}).value || '';
      f.querySelectorAll('[data-for]').forEach(function(g){ var on = g.dataset.for.split('|').indexOf(v) > -1; g.hidden = !on; g.querySelectorAll('input,select,textarea').forEach(function(i){ i.disabled = !on; }); });
    }
    if (tipo && map[tipo]){ var r = f.querySelector('input[name=tipo][value="' + map[tipo] + '"]'); if (r) r.checked = true; }
    f.querySelectorAll('input[name=tipo]').forEach(function(r){ r.addEventListener('change', showGroups); });
    showGroups();
    var err = f.querySelector('.err');
    f.addEventListener('submit', function(e){
      e.preventDefault(); err.textContent = '';
      if (f.querySelector('.hp input').value) return;
      var bad = [].slice.call(f.querySelectorAll('input,select,textarea')).filter(function(i){ return !i.disabled && !i.checkValidity(); })[0];
      if (!f.querySelector('input[name=tipo]:checked')) bad = f.querySelector('input[name=tipo]');
      if (bad){ err.textContent = bad.dataset.msg || 'Revisa este campo, por favor.'; bad.focus(); return; }
      var d = new FormData(f), lines = [], seen = {};
      f.querySelectorAll('[name]').forEach(function(el){
        var n = el.name; if (seen[n] || el.disabled || n === 'web_site' || n === 'acepto') return; seen[n] = 1;
        var v = d.getAll(n).filter(Boolean).join(', ');
        var lab = el.closest('[data-label]'); if (v) lines.push((lab ? lab.dataset.label : n) + ': ' + v);
      });
      var to = f.dataset.to, subject = (d.get('tipo') || 'Contacto') + ' · ' + (d.get('empresa') || d.get('nombre') || '');
      var body = lines.join('\n'), href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var done = document.getElementById('done');
      f.hidden = true; done.hidden = false;
      done.querySelector('[data-mail]').href = href;
      done.querySelector('[data-copy]').onclick = function(){
        var t = 'Para: ' + to + '\nAsunto: ' + subject + '\n\n' + body;
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(function(){ done.querySelector('.note').textContent = 'Copiado. Pégalo en un correo a ' + to + '.'; });
      };
      location.href = href;
    });
  }
})();
