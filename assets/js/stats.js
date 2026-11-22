/* Estadísticas: lee window.DATOS (datos.js) y rellena la página. Nunca inventa: si falta un dato, deja «—». */
(function(){
  var D = window.DATOS; if (!D) return;
  var EN = document.documentElement.lang === 'en', LOC = EN ? 'en-GB' : 'es-ES';
  function get(k){ return k.split('.').reduce(function(o, p){ return o == null ? o : o[p]; }, D); }
  var nf = new Intl.NumberFormat(LOC, {useGrouping:'always'});
  function k1(n){ if (n < 1000) return nf.format(n); var v = Math.floor(n / 100) / 10; return EN ? String(v).replace(/\.0$/, '') + 'K' : String(v).replace('.', ',').replace(/,0$/, '') + ' mil'; }
  var F = { int: function(n){ return nf.format(n); }, k1: k1, pct0: function(n){ return Math.round(n) + (EN ? '%' : ' %'); }, pct1: function(n){ return EN ? n + '%' : String(n).replace('.', ',') + ' %'; } };
  function date(s, o){ return s ? new Date(s + 'T12:00:00').toLocaleDateString(LOC, o || {day:'numeric', month:'long', year:'numeric'}) : '—'; }
  /* cifras que suben desde 0 cuando aparecen en pantalla */
  function put(el, v){ el.textContent = (el.dataset.pre || '') + (F[el.dataset.f] || F.int)(v); }
  var cio = 'IntersectionObserver' in window ? new IntersectionObserver(function(es){ es.forEach(function(e){
    if (!e.isIntersecting) return; var el = e.target, v = +el.dataset.v, t0 = null, dec = el.dataset.f === 'pct1'; cio.unobserve(el);
    requestAnimationFrame(function tick(t){ if (t0 === null) t0 = t; var k = Math.min(1, (t - t0) / 1300), ease = 1 - Math.pow(1 - k, 3), n = v * ease;
      put(el, k < 1 ? (dec ? Math.round(n * 10) / 10 : Math.round(n)) : v); if (k < 1) requestAnimationFrame(tick); });
  }); }, {threshold:.5}) : null;
  document.querySelectorAll('[data-n]').forEach(function(el){ var v = get(el.dataset.n); if (v == null) return;
    if (cio && typeof v === 'number' && v > 20){ el.dataset.v = v; put(el, 0); cio.observe(el); } else put(el, v); });
  document.querySelectorAll('[data-txt]').forEach(function(el){ var v = get(el.dataset.txt); if (v != null) el.textContent = v; });
  document.querySelectorAll('[data-date]').forEach(function(el){ el.textContent = date(get(el.dataset.date)); });
  document.querySelectorAll('[data-per]').forEach(function(el){
    var p = el.dataset.per.split('|');
    el.textContent = date(get(p[0]), {day:'numeric', month:'short'}) + ' – ' + date(get(p[1]), {day:'numeric', month:'short', year:'numeric'});
  });
  document.querySelectorAll('[data-w]').forEach(function(el){ var v = get(el.dataset.w); if (v != null) requestAnimationFrame(function(){ el.style.width = v + '%'; }); });
  var NAMES = EN ? {ES:'Spain', MX:'Mexico', AR:'Argentina', CO:'Colombia', US:'USA', CL:'Chile', PE:'Peru'} : {ES:'España', MX:'México', AR:'Argentina', CO:'Colombia', US:'EE. UU.', CL:'Chile', PE:'Perú'};
  document.querySelectorAll('[data-bars]').forEach(function(ul){
    var arr = get(ul.dataset.bars) || [], hi = (ul.dataset.hi || '').split(','), max = Math.max.apply(null, arr.map(function(r){ return r[1]; }));
    ul.innerHTML = arr.map(function(r){
      return '<li' + (hi.indexOf(r[0]) > -1 ? ' class="hi"' : '') + '><span>' + (NAMES[r[0]] || r[0]) + '</span><i style="--w:' + (r[1] / max * 100).toFixed(1) + '%"></i><b>' + (EN ? r[1] + '%' : String(r[1]).replace('.', ',') + ' %') + '</b></li>';
    }).join('');
  });
  document.querySelectorAll('[data-chart]').forEach(function(box){
    var rows = get(box.dataset.chart) || [], idx = +(box.dataset.idx || 2), tip = document.getElementById(box.dataset.tip);
    if (!rows.length){ box.innerHTML = '<p class="note">' + (EN ? 'No data for this period.' : 'Sin datos de este periodo.') + '</p>'; return; }
    var vals = rows.map(function(r){ return r[idx]; }).sort(function(a, b){ return a - b; });
    var n = vals.length, med = n % 2 ? vals[(n - 1) / 2] : (vals[n / 2 - 1] + vals[n / 2]) / 2, max = vals[n - 1] || 1;
    var unit = box.dataset.unit || (EN ? 'views' : 'visualizaciones');
    var big = rows.map(function(r){ return r[idx] > med * 2; });
    box.innerHTML = rows.map(function(r, i){
      var lab = big[i] && !((big[i - 1] && rows[i - 1][idx] > r[idx]) || (big[i + 1] && rows[i + 1][idx] > r[idx]));
      return '<button type="button" class="c' + (big[i] ? ' hi' : '') + '" style="--h:' + Math.max(3, r[idx] / max * 100).toFixed(1) + '%;--d:' + (i * 25) + 'ms" data-i="' + i + '" aria-label="' + r[1] + ': ' + nf.format(r[idx]) + ' ' + unit + '">' + (lab ? '<span class="v">' + k1(r[idx]) + '</span>' : '') + '</button>';
    }).join('') + '<i class="med" style="bottom:' + (med / max * 100).toFixed(1) + '%"></i>';
    function show(i){
      var r = rows[i]; box.querySelectorAll('.c').forEach(function(c){ c.classList.toggle('on', +c.dataset.i === i); });
      if (tip) tip.innerHTML = '<b>' + nf.format(r[idx]) + '</b> ' + unit + ' · «' + r[1] + '» · ' + date(r[0], {day:'numeric', month:'short'});
    }
    ['pointerover', 'focusin', 'click'].forEach(function(ev){ box.addEventListener(ev, function(e){ var c = e.target.closest('.c'); if (c) show(+c.dataset.i); }); });
    if ('IntersectionObserver' in window){ var io = new IntersectionObserver(function(es){ if (es[0].isIntersecting){ box.classList.add('grow'); io.disconnect(); } }, {threshold:.25}); io.observe(box); }
    else box.classList.add('grow');
    var medEl = document.getElementById(box.dataset.med); if (medEl) medEl.textContent = nf.format(Math.round(med));
  });
})();
