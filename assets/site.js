/* Patri Barbero · interacciones comunes */
(function(){
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EMAIL = 'patribarberoinfo@gmail.com';

  /* header */
  var top = document.querySelector('.top');
  if (top) addEventListener('scroll', function(){ top.classList.toggle('sc', scrollY > 8); }, {passive:true});
  var burger = document.querySelector('.burger'), nav = document.querySelector('.nav');
  if (burger && nav){
    burger.addEventListener('click', function(){
      var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o); burger.textContent = o ? 'Cerrar' : 'Menú';
    });
    nav.addEventListener('click', function(e){ if (e.target.closest('a')){ nav.classList.remove('open'); burger.setAttribute('aria-expanded', false); burger.textContent = 'Menú'; } });
  }

  /* reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !RM){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); }, {rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(el){ io.observe(el); });
  } else rv.forEach(function(el){ el.classList.add('in'); });

  /* etiquetas colgantes: péndulo que reacciona al movimiento del cursor (o al scroll en móvil) */
  var tags = [].slice.call(document.querySelectorAll('.tag'));
  if (tags.length && !RM){
    var st = tags.map(function(){ return {a:0, v:0}; });
    var lastX = null, lastT = 0, lastY = scrollY;
    function kick(i, f){ st[i].v += f; }
    addEventListener('pointermove', function(e){
      if (e.pointerType !== 'mouse') return;
      var now = performance.now();
      if (lastX !== null){
        var vx = (e.clientX - lastX) / Math.max(16, now - lastT);
        tags.forEach(function(t, i){
          var r = t.getBoundingClientRect();
          if (e.clientY > r.top - 40 && e.clientY < r.bottom && e.clientX > r.left - 30 && e.clientX < r.right + 30) kick(i, vx * 0.9);
        });
      }
      lastX = e.clientX; lastT = now;
    }, {passive:true});
    addEventListener('scroll', function(){
      var d = scrollY - lastY; lastY = scrollY;
      if (innerWidth < 861) tags.forEach(function(t, i){ kick(i, d * 0.012 * (i % 2 ? -1 : 1)); });
    }, {passive:true});
    tags.forEach(function(t, i){ setTimeout(function(){ kick(i, (i - 1) * 0.9 + 0.6); }, 300 + i * 140); });
    (function loop(){
      tags.forEach(function(t, i){
        var s = st[i], hov = t.matches(':hover');
        s.v += -s.a * 0.035; s.v *= hov ? 0.82 : 0.955; s.a += s.v;
        if (hov) s.a *= 0.9;
        s.a = Math.max(-9, Math.min(9, s.a));
        t.style.setProperty('--rot', s.a.toFixed(2) + 'deg');
      });
      requestAnimationFrame(loop);
    })();
  }

  /* diálogo de vídeo (YouTube nocookie) */
  var vd = document.getElementById('vd');
  if (vd){
    var frame = vd.querySelector('.frame');
    document.addEventListener('click', function(e){
      var b = e.target.closest('[data-yt]'); if (!b || !vd.showModal) return;
      e.preventDefault();
      frame.classList.toggle('wide', b.dataset.wide === '1');
      frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + b.dataset.yt + '?autoplay=1&rel=0&playsinline=1" title="' + (b.dataset.title || 'Vídeo') + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
      vd.showModal();
    });
    function close(){ vd.close(); }
    vd.querySelector('.x').addEventListener('click', close);
    vd.addEventListener('click', function(e){ if (e.target === vd || e.target.classList.contains('box')) close(); });
    vd.addEventListener('close', function(){ frame.innerHTML = ''; });
  }

  /* formularios: hoja de encargo por pasos.
     Mientras no haya servidor de envío, el formulario prepara el correo completo
     y lo abre en el gestor de correo de la persona (o permite copiarlo). */
  document.querySelectorAll('form.brief').forEach(function(f){
    var sets = [].slice.call(f.querySelectorAll('fieldset')), steps = f.querySelectorAll('.steps i');
    var cur = 0, err = f.querySelector('.err');
    function show(n){
      cur = n;
      sets.forEach(function(s, i){ s.hidden = i !== n; });
      steps.forEach(function(s, i){ s.classList.toggle('on', i <= n); });
      f.querySelector('[data-back]').hidden = n === 0;
      f.querySelector('[data-next]').hidden = n === sets.length - 1;
      f.querySelector('[data-send]').hidden = n !== sets.length - 1;
      err.textContent = '';
    }
    function valid(){
      var s = sets[cur], bad = null;
      s.querySelectorAll('input,select,textarea').forEach(function(el){ if (!bad && !el.checkValidity()) bad = el; });
      s.querySelectorAll('[data-req-group]').forEach(function(g){ if (!bad && !g.querySelector('input:checked')) bad = g.querySelector('input'); });
      if (bad){ err.textContent = bad.dataset.msg || 'Revisa este campo para continuar.'; bad.focus(); return false; }
      return true;
    }
    f.querySelector('[data-next]').addEventListener('click', function(){ if (valid()) show(cur + 1); });
    f.querySelector('[data-back]').addEventListener('click', function(){ show(cur - 1); });
    f.addEventListener('submit', function(e){
      e.preventDefault();
      if (!valid()) return;
      if (f.querySelector('.hp input').value) return; // antispam
      var lines = [], data = new FormData(f), seen = {};
      f.querySelectorAll('[name]').forEach(function(el){
        var n = el.name; if (seen[n] || n === 'web_site') return; seen[n] = 1;
        var v = data.getAll(n).filter(Boolean).join(', ');
        var lab = el.closest('[data-label]') ? el.closest('[data-label]').dataset.label : n;
        if (v && n !== 'acepto') lines.push(lab + ': ' + v);
      });
      var subject = f.dataset.subject + ' · ' + (data.get('empresa') || data.get('nombre') || '');
      var body = lines.join('\n');
      var href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var done = f.parentNode.querySelector('.done');
      f.hidden = true; done.hidden = false;
      done.querySelector('[data-mail]').href = href;
      done.querySelector('[data-copy]').addEventListener('click', function(){
        var t = 'Para: ' + EMAIL + '\nAsunto: ' + subject + '\n\n' + body;
        (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function(){ done.querySelector('.note').textContent = 'Copiado. Pégalo en un correo a ' + EMAIL + '.'; }, function(){});
      });
      location.href = href;
    });
    show(0);
  });

  var y = document.getElementById('y'); if (y) y.textContent = new Date().getFullYear();
})();
