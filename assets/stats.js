/* Estadísticas: lee window.DATOS (datos.js) y rellena la página */
(function(){
  var D = window.DATOS; if (!D) return;
  function get(k){ return k.split('.').reduce(function(o, p){ return o == null ? o : o[p]; }, D); }
  var nf = new Intl.NumberFormat('es-ES', {useGrouping:'always'});
  function k1(n){ if (n < 1000) return nf.format(n); var v = Math.floor(n / 100) / 10; return String(v).replace('.', ',').replace(/,0$/, '') + ' mil'; }
  var F = {
    int: function(n){ return nf.format(n); },
    k1: k1,
    pct0: function(n){ return Math.round(n) + ' %'; },
    pct1: function(n){ return String(n).replace('.', ',') + ' %'; }
  };
  function date(s, short){
    if (!s) return '–'; var d = new Date(s + 'T12:00:00');
    return d.toLocaleDateString('es-ES', short ? {month:'short', year:'numeric'} : {day:'numeric', month:'long', year:'numeric'});
  }
  document.querySelectorAll('[data-n]').forEach(function(el){
    var v = get(el.dataset.n); if (v == null) return;
    el.textContent = (el.dataset.pre || '') + (F[el.dataset.f] || F.int)(v);
  });
  document.querySelectorAll('[data-date]').forEach(function(el){ el.textContent = date(get(el.dataset.date), el.dataset.fmt === 'short'); });
  document.querySelectorAll('[data-per]').forEach(function(el){
    var p = el.dataset.per.split('|'), a = new Date(get(p[0]) + 'T12:00:00'), b = new Date(get(p[1]) + 'T12:00:00');
    el.textContent = a.toLocaleDateString('es-ES', {day:'numeric', month:'short'}) + ' – ' + b.toLocaleDateString('es-ES', {day:'numeric', month:'short', year:'numeric'});
  });
  document.querySelectorAll('[data-w]').forEach(function(el){ var v = get(el.dataset.w); requestAnimationFrame(function(){ el.style.width = v + '%'; }); });
  var NAMES = {ES:'España', MX:'México', AR:'Argentina', CO:'Colombia', US:'EE. UU.', CL:'Chile', PE:'Perú'};
  document.querySelectorAll('[data-bars]').forEach(function(ul){
    var arr = get(ul.dataset.bars) || [], hi = (ul.dataset.hi || '').split(','), max = Math.max.apply(null, arr.map(function(r){ return r[1]; }));
    ul.innerHTML = arr.map(function(r){
      return '<li' + (hi.indexOf(r[0]) > -1 ? ' class="hi"' : '') + '><span>' + (NAMES[r[0]] || r[0]) + '</span><i style="--w:' + (r[1] / max * 100).toFixed(1) + '%"></i><b>' + String(r[1]).replace('.', ',') + ' %</b></li>';
    }).join('');
  });

  /* gráfico de columnas: visualizaciones de cada Short */
  var box = document.getElementById('c-shorts'), tip = document.getElementById('c-tip');
  if (box){
    var rows = get('youtube.shorts_periodo.por_short') || [];
    var vals = rows.map(function(r){ return r[2]; }).sort(function(a, b){ return a - b; });
    var med = vals.length ? (vals.length % 2 ? vals[(vals.length - 1) / 2] : (vals[vals.length / 2 - 1] + vals[vals.length / 2]) / 2) : 0;
    var max = vals[vals.length - 1] || 1;
    box.innerHTML = rows.map(function(r, i){
      var h = Math.max(3, r[2] / max * 100), big = r[2] > med * 2;
      return '<button type="button" class="c' + (big ? ' hi' : '') + '" style="--h:' + h.toFixed(1) + '%;--d:' + (i * 30) + 'ms" data-i="' + i + '" aria-label="' + r[1] + ': ' + nf.format(r[2]) + ' visualizaciones">' + (big ? '<span class="v">' + k1(r[2]) + '</span>' : '') + '</button>';
    }).join('') + '<i class="med" style="bottom:' + (med / max * 100).toFixed(1) + '%"></i>';
    function show(i){
      var r = rows[i]; box.querySelectorAll('.c').forEach(function(c){ c.classList.toggle('on', +c.dataset.i === i); });
      tip.innerHTML = '<b>' + nf.format(r[2]) + '</b> visualizaciones · «' + r[1] + '» · ' + new Date(r[0] + 'T12:00:00').toLocaleDateString('es-ES', {day:'numeric', month:'short'});
    }
    box.addEventListener('pointerover', function(e){ var c = e.target.closest('.c'); if (c) show(+c.dataset.i); });
    box.addEventListener('focusin', function(e){ var c = e.target.closest('.c'); if (c) show(+c.dataset.i); });
    box.addEventListener('click', function(e){ var c = e.target.closest('.c'); if (c) show(+c.dataset.i); });
    if ('IntersectionObserver' in window){
      var io = new IntersectionObserver(function(es){ if (es[0].isIntersecting){ box.classList.add('grow'); io.disconnect(); } }, {threshold:.3}); io.observe(box);
    } else box.classList.add('grow');
  }

  /* lista de colaboraciones: miniatura que sigue al cursor */
  var list = document.querySelector('.clist'), fl = document.querySelector('.cfloat');
  if (list && fl && matchMedia('(hover:hover)').matches){
    var img = fl.querySelector('img'), wrap = list.parentNode;
    list.addEventListener('pointerover', function(e){ var b = e.target.closest('[data-img]'); if (b){ img.src = b.dataset.img; fl.classList.add('on'); } });
    list.addEventListener('pointerleave', function(){ fl.classList.remove('on'); });
    wrap.addEventListener('pointermove', function(e){ var r = wrap.getBoundingClientRect(); fl.style.transform = 'translate(' + (e.clientX - r.left + 24) + 'px,' + (e.clientY - r.top - 80) + 'px) rotate(-4deg)'; });
  }
})();
