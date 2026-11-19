/* Perchero UGC: arrastrar para deslizar con el ratón; en móvil es scroll nativo */
(function(){
  var rack = document.querySelector('.rack-x'); if (!rack) return;
  var down = false, sx = 0, sl = 0, moved = false;
  rack.addEventListener('pointerdown', function(e){ if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = rack.scrollLeft; rack.classList.add('drag'); });
  addEventListener('pointermove', function(e){ if (!down) return; var d = e.clientX - sx; if (Math.abs(d) > 4) moved = true; rack.scrollLeft = sl - d; });
  addEventListener('pointerup', function(){ down = false; rack.classList.remove('drag'); });
  rack.addEventListener('click', function(e){ if (moved){ e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  /* las perchas se balancean un poco al desplazar */
  var last = rack.scrollLeft, sw = 0;
  rack.addEventListener('scroll', function(){ sw += (rack.scrollLeft - last) * 0.08; last = rack.scrollLeft; }, {passive:true});
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) (function loop(){
    sw *= 0.9; rack.style.setProperty('--sw', Math.max(-6, Math.min(6, -sw)).toFixed(2) + 'deg'); requestAnimationFrame(loop);
  })();
})();
