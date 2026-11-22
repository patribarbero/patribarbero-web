/* Piezas interactivas: muñequita sporty ↔ femenina · armario del canal · escritorio escondido */
(function(){
  var EN = document.documentElement.lang === 'en';

  /* ---------- muñequita ---------- */
  var dl = document.querySelector('.dl');
  if (dl){
    var stage = dl.querySelector('.dl-stage'), range = dl.querySelector('input[type=range]'), steps = dl.querySelectorAll('.dl-step'), touched = false;
    function set(i){
      i = +i; stage.dataset.step = i;
      stage.querySelectorAll('.pz').forEach(function(g){ g.classList.toggle('on', g.dataset.s.split(' ').indexOf(String(i)) > -1); });
      steps.forEach(function(s){ s.hidden = +s.dataset.i !== i; });
      range.value = i; range.setAttribute('aria-valuetext', steps[i].querySelector('h3').textContent);
      range.style.setProperty('--p', (i / 4 * 100) + '%');
      stage.classList.remove('pop'); void stage.offsetWidth; stage.classList.add('pop');
    }
    range.addEventListener('input', function(){ touched = true; set(range.value); });
    set(2);
    // demostración: al aparecer recorre de un extremo a otro para que se vea que se puede tocar
    if ('IntersectionObserver' in window){
      var io = new IntersectionObserver(function(es){
        if (!es[0].isIntersecting) return; io.disconnect();
        var seq = [2, 1, 0, 1, 2, 3, 4, 3, 2], k = 0;
        (function next(){ if (touched || k >= seq.length) return; set(seq[k++]); setTimeout(next, 750); })();
      }, {threshold:.5});
      io.observe(dl);
    }
  }

  /* ---------- armario ---------- */
  var cl = document.querySelector('.closet');
  if (cl){
    function openCl(){ cl.classList.add('open'); }
    if ('IntersectionObserver' in window){
      var co = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting && e.target.offsetParent){ setTimeout(openCl, 250); co.disconnect(); } }); }, {threshold:.45});
      co.observe(cl);
      // si el armario estaba en una pestaña oculta, se abre al mostrarla
      document.querySelectorAll('[role=tab]').forEach(function(t){ t.addEventListener('click', function(){ setTimeout(function(){ if (cl.offsetParent) setTimeout(openCl, 250); }, 50); }); });
    } else openCl();
    cl.querySelectorAll('.cl-door').forEach(function(d){ d.addEventListener('click', openCl); });
  }

  /* ---------- escritorio escondido: doble clic (o doble toque) en el nombre ---------- */
  var desk = document.getElementById('desk'), logo = document.querySelector('.top .logo');
  if (desk && logo){
    var timer = null, z = 10;
    logo.style.touchAction = 'manipulation';
    logo.addEventListener('click', function(e){
      e.preventDefault();
      var href = logo.getAttribute('href');
      if (timer){ clearTimeout(timer); timer = null; openDesk(); return; }
      timer = setTimeout(function(){ timer = null; location.href = href; }, 280);
    });
    function front(w){ w.style.zIndex = ++z; }
    var small = matchMedia('(max-width:760px)');
    function openWin(id){ var w = document.getElementById(id); if (!w) return;
      if (small.matches) desk.querySelectorAll('.dk-win').forEach(function(o){ if (o !== w) o.hidden = true; });   // en móvil, una ventana cada vez
      w.hidden = false; front(w); w.classList.remove('pop'); void w.offsetWidth; w.classList.add('pop'); }
    function openDesk(){
      desk.hidden = false; document.body.style.overflow = 'hidden';
      setTimeout(function(){ openWin('dk-hola'); }, 150);   // al entrar solo se abre la bienvenida
      tick();
    }
    function closeDesk(){ desk.hidden = true; document.body.style.overflow = ''; desk.querySelectorAll('.dk-win').forEach(function(w){ w.hidden = true; }); }
    desk.querySelector('.dk-exit').addEventListener('click', closeDesk);
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && !desk.hidden) closeDesk(); });
    desk.querySelectorAll('[data-open]').forEach(function(b){ b.addEventListener('click', function(){ openWin(b.dataset.open); }); });
    desk.querySelectorAll('.dk-x').forEach(function(b){ b.addEventListener('click', function(){ b.closest('.dk-win').hidden = true; }); });
    // arrastrar ventanas por la barra
    desk.querySelectorAll('.dk-win').forEach(function(w){
      var bar = w.querySelector('.dk-bar');
      w.addEventListener('pointerdown', function(){ front(w); });
      bar.addEventListener('pointerdown', function(e){
        if (e.target.closest('button')) return;
        var r = w.getBoundingClientRect(), dx = e.clientX - r.left, dy = e.clientY - r.top;
        bar.setPointerCapture(e.pointerId); w.classList.add('drag');
        function mv(ev){ var x = Math.max(-r.width + 80, Math.min(innerWidth - 80, ev.clientX - dx)), y = Math.max(44, Math.min(innerHeight - 40, ev.clientY - dy)); w.style.left = x + 'px'; w.style.top = y + 'px'; w.style.transform = 'none'; }
        function up(){ bar.removeEventListener('pointermove', mv); bar.removeEventListener('pointerup', up); w.classList.remove('drag'); }
        bar.addEventListener('pointermove', mv); bar.addEventListener('pointerup', up);
      });
    });
    var clock = desk.querySelector('.dk-clock');
    function tick(){ if (desk.hidden) return; clock.textContent = new Date().toLocaleTimeString(EN ? 'en-GB' : 'es-ES', {hour:'2-digit', minute:'2-digit'}); setTimeout(tick, 20000); }
  }
})();
