/* Texto orbital 3D · Patri Barbero (RIBETE 1.3)
   - Gira con JavaScript (igual en todos los navegadores).
   - Con «reducir movimiento» activado, se queda quieto con la frase leíble de frente.
   - Las letras se reparten según su ancho real ya ampliado por la perspectiva, para que no se monten. */
(function(){
  var stage = document.querySelector('.orb'); if (!stage) return;
  var F = stage.querySelector('.ring-f'), B = stage.querySelector('.ring-b');
  var phrase = stage.dataset.phrase || 'Moda como identidad', reps = +(stage.dataset.reps || 2);
  var ctx = document.createElement('canvas').getContext('2d');
  var mq = matchMedia('(prefers-reduced-motion: reduce)'), reduce = mq.matches;
  var still = 0;                      // ángulo en el que la primera frase queda centrada delante
  var PERSP = 3.2, RADIUS = 31;       // en % de la altura de la escena (coinciden con el CSS)

  function build(){
    var H = stage.getBoundingClientRect().height; if (!H) return;
    var em = H / 100, R = RADIUS * em, circ = 2 * Math.PI * R;
    var grow = PERSP / (PERSP - RADIUS / 100);        // cuánto crece una letra al pasar por delante
    var one = phrase.toUpperCase() + ' · ', txt = '';
    for (var r = 0; r < reps; r++) txt += one;
    // 1) pinta las letras sin girar y mide su ancho REAL en pantalla (misma fuente que se ve)
    function measure(size){
      stage.style.setProperty('--fs', size + 'px');
      F.innerHTML = [].map.call(txt, function(c){ return '<span class="l"><i>' + (c === ' ' ? '\u00a0' : c) + '</i></span>'; }).join('');
      return [].map.call(F.querySelectorAll('.l>i'), function(el){ return el.offsetWidth; });
    }
    var fs = 11 * em, raw = measure(fs);
    function slots(rw, size){ return rw.map(function(x){ return x * grow + size * .07; }); }
    var w = slots(raw, fs), sum = w.reduce(function(a, b){ return a + b; }, 0);
    var k = Math.max(.5, Math.min(1.35, circ / sum)); fs *= k;
    raw = measure(fs); w = slots(raw, fs); sum = w.reduce(function(a, b){ return a + b; }, 0);
    var sc = circ / sum, acc = 0, html = '', firstEnd = one.length;
    for (var i = 0; i < txt.length; i++){
      var a = (acc + w[i] * sc / 2) / circ * 360; acc += w[i] * sc;
      html += '<span class="l" style="transform:rotateY(' + a.toFixed(2) + 'deg) translateZ(' + R.toFixed(1) + 'px)"><i>' + (txt[i] === ' ' ? '\u00a0' : txt[i]) + '</i></span>';
    }
    F.innerHTML = html; B.innerHTML = html;
    // centro exacto de la primera frase (sin el separador)
    var acc2 = 0, start = 0, end = 0;
    for (var j = 0; j < firstEnd - 3; j++){ acc2 += w[j] * sc; end = acc2; }
    still = -((start + end) / 2) / circ * 360;
    if (angle === null) angle = still;                // empieza siempre con la frase leíble
  }

  var angle = null, dur = +(stage.dataset.dur || 26), last = null, paused = false, visible = true;
  function frame(t){
    if (angle !== null){
      if (last !== null && !paused && visible && !reduce && !document.hidden) angle -= 360 * ((t - last) / 1000) / dur;
      var tr = 'rotateY(' + (reduce ? still : angle).toFixed(3) + 'deg)';
      F.style.transform = tr; B.style.transform = tr;
    }
    last = t; requestAnimationFrame(frame);
  }
  (document.fonts && document.fonts.load ? document.fonts.load('400 40px Anton') : Promise.resolve()).then(function(){
    build(); if ('ResizeObserver' in window) new ResizeObserver(build).observe(stage); requestAnimationFrame(frame);
  });

  var btn = document.querySelector('.orb-pause');
  function syncBtn(){ if (btn) btn.hidden = reduce; }
  if (mq.addEventListener) mq.addEventListener('change', function(){ reduce = mq.matches; syncBtn(); });
  syncBtn();
  if (btn) btn.addEventListener('click', function(){ paused = !paused; btn.setAttribute('aria-pressed', paused); var en = document.documentElement.lang === 'en'; btn.textContent = paused ? (en ? '▶ Play' : '▶ Reanudar') : (en ? '❚❚ Pause' : '❚❚ Pausar'); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ visible = es[0].isIntersecting; }).observe(stage);
  setTimeout(function(){ visible = true; }, 500);
})();
