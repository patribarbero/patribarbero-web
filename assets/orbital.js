/* Texto orbital 3D · Patri Barbero (RIBETE 1.3)
   Uso: <div class="orb" data-phrase="Moda como identidad" data-reps="2">… (ver index) */
(function(){
  var stage = document.querySelector('.orb'); if (!stage) return;
  var F = stage.querySelector('.ring-f'), B = stage.querySelector('.ring-b');
  var phrase = stage.dataset.phrase || 'Moda como identidad', reps = +(stage.dataset.reps || 2);
  var ctx = document.createElement('canvas').getContext('2d');
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function build(){
    var H = stage.getBoundingClientRect().height, em = H / 100, R = 31 * em, circ = 2 * Math.PI * R;
    var one = phrase.toUpperCase() + '  ·  ', txt = ''; for (var r = 0; r < reps; r++) txt += one;
    var fs = 11 * em; ctx.font = '400 ' + fs + 'px Anton';
    var track = .06 * fs, total = ctx.measureText(txt).width + track * txt.length;
    var k = Math.max(.5, Math.min(1.3, circ / total)); fs *= k; track *= k; ctx.font = '400 ' + fs + 'px Anton';
    var w = [].map.call(txt, function(c){ return ctx.measureText(c).width + track; });
    var sum = w.reduce(function(a, b){ return a + b; }, 0), sc = circ / sum, acc = 0, html = '';
    stage.style.setProperty('--fs', fs + 'px');
    for (var i = 0; i < txt.length; i++){
      var a = (acc + w[i] * sc / 2) / circ * 360; acc += w[i] * sc;
      html += '<span class="l" style="transform:rotateY(' + a.toFixed(2) + 'deg) translateZ(' + R.toFixed(1) + 'px)"><i>' + (txt[i] === ' ' ? ' ' : txt[i]) + '</i></span>';
    }
    F.innerHTML = html; B.innerHTML = html;
  }
  var angle = 0, dur = +(stage.dataset.dur || 26), last = null, paused = false, visible = true;
  function frame(t){
    if (last !== null && !paused && visible && !reduce && !document.hidden) angle -= 360 * ((t - last) / 1000) / dur;
    last = t; var tr = 'rotateY(' + (reduce ? 20 : angle).toFixed(3) + 'deg)'; F.style.transform = tr; B.style.transform = tr;
    requestAnimationFrame(frame);
  }
  document.fonts.load('400 40px Anton').then(function(){ build(); new ResizeObserver(build).observe(stage); requestAnimationFrame(frame); });
  var btn = document.querySelector('.orb-pause');
  if (btn){
    if (reduce) btn.hidden = true;
    btn.addEventListener('click', function(){ paused = !paused; btn.setAttribute('aria-pressed', paused); btn.textContent = paused ? '▶ Reanudar' : '❚❚ Pausar'; });
  }
  if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ visible = es[0].isIntersecting; }).observe(stage);
  setTimeout(function(){ visible = true; }, 400);
})();
