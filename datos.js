/*
  DATOS DEL MEDIA KIT DE PATRI BARBERO
  ------------------------------------
  Único archivo que hay que cambiar para actualizar las estadísticas.
  - Números sin puntos ni comas de miles (13952, no 13.952). Decimales con punto (4.1).
  - Fechas en formato AAAA-MM-DD.
  - La web los muestra sola en español o en inglés con el formato de cada idioma.
  - No borres comas, comillas ni llaves { }.
*/
window.DATOS = {
  actualizado: "2026-11-10",
  periodo: { desde: "2026-10-13", hasta: "2026-11-09" },   // últimos 28 días

  youtube: {
    suscriptores: 13952,          // YouTube Studio, tiempo real, 10 nov
    netos: 1700,                  // suscriptores netos en el periodo (Studio: +1,7 mil)
    vis: 119881,                  // visualizaciones del canal en el periodo
    horas: 818,                   // tiempo de visualización (horas)
    shorts: 105700,               // visualizaciones de Shorts
    largos: 14200,                // visualizaciones de vídeos largos
    ctr_largos: 5.1,              // % clics en miniaturas (vídeos largos)
    duracion_largos: "3:06",      // duración media de visualización (vídeos largos)
    shorts_feed_pct: 91.5,        // % de visualizaciones de Shorts que llega desde el feed de Shorts
    shorts_periodo: {             // Shorts PUBLICADOS en el periodo (YouTube Studio, visualizaciones a 10 nov)
      publicados: 20, vistas: 100132, mediana: 1517, top: 35764,
      por_short: [
        ["2026-10-16", "Tu ropa habla de ti", 3855],
        ["2026-10-17", "Mi método para comprar ropa", 1815],
        ["2026-10-20", "Oversized y femenina", 35764],
        ["2026-10-21", "¿Qué quieres transmitir con tu outfit?", 8475],
        ["2026-10-22", "1 pañuelo, 4 versiones de ti", 2107],
        ["2026-10-23", "Vuelven los broches", 19872],
        ["2026-10-24", "El encaje según cómo lo mezcles", 1469],
        ["2026-10-26", "Vuelven los bolsos XXL", 1470],
        ["2026-10-27", "Vuelven los cinturones XXL", 1584],
        ["2026-10-28", "Elige A, B o C", 1204],
        ["2026-10-29", "Halloween a nuestro estilo", 3774],
        ["2026-10-31", "Las medias, protagonistas", 1464],
        ["2026-11-01", "Puedes amar una tendencia y no llevarla", 8076],
        ["2026-11-02", "El estampado bambi", 1564],
        ["2026-11-03", "Oversize y autoestima", 1151],
        ["2026-11-04", "Rojo tomate o burdeos", 1399],
        ["2026-11-05", "Lo más deseado de la moda", 1245],
        ["2026-11-06", "Zapatillas de montaña con falda", 1443],
        ["2026-11-08", "Marrón con azul cobalto", 1200],
        ["2026-11-09", "El toque que hace mono tu chándal", 1201]
      ]
    },
    top_shorts: [
      ["Oversized y femenina a la vez", 35764],
      ["Vuelven los broches", 19872],
      ["¿Qué quieres transmitir con tu outfit?", 8473],
      ["Puedes amar una tendencia y no llevarla", 8071]
    ],
    audiencia: {                  // vidIQ / YouTube Studio, espectadores con sesión iniciada
      desde: "2026-07-31", hasta: "2026-10-28",
      mujeres: 86.3,
      edad: [["13–17", 11.2], ["18–24", 6.9], ["25–34", 26.1], ["35–44", 15.6], ["45–54", 18.9], ["55–64", 13.1], ["65+", 8.2]],
      paises: [["ES", 56.0], ["MX", 8.4], ["AR", 5.3], ["CO", 3.5]]
    }
  },

  instagram: {
    seguidores: 1266,
    reels: 21,
    reproducciones: 76093,
    mediana: 2165,
    alcance: 59773,               // suma del alcance de cada Reel
    interaccion: 4.1,             // % interacciones / alcance
    guardados: 276,
    compartidos: 75,
    por_reel: [
      ["2026-10-13", "Mi método para comprar ropa", 2165],
      ["2026-10-15", "Oversized y femenina", 8944],
      ["2026-10-16", "¿Qué quieres transmitir con tu outfit?", 2101],
      ["2026-10-20", "Vuelven los broches", 13018],
      ["2026-10-20", "1 pañuelo, 4 versiones de ti", 1662],
      ["2026-10-22", "Vuelven los bolsos XXL", 2320],
      ["2026-10-24", "El encaje según cómo lo mezcles", 2193],
      ["2026-10-26", "Vuelven los cinturones XXL", 2210],
      ["2026-10-27", "Las medias, protagonistas", 3414],
      ["2026-10-28", "Elige A, B o C", 13562],
      ["2026-10-28", "Halloween a nuestro estilo", 2048],
      ["2026-10-30", "Zapatillas de skate con tacón", 2054],
      ["2026-10-31", "Puedes amar una tendencia y no llevarla", 2448],
      ["2026-11-01", "El estampado bambi", 2112],
      ["2026-11-02", "Oversize y autoestima", 2664],
      ["2026-11-03", "Rojo tomate o burdeos", 1515],
      ["2026-11-04", "Lo más deseado de la moda", 1498],
      ["2026-11-05", "Zapatillas de montaña con falda", 1887],
      ["2026-11-08", "Marrón con azul cobalto", 1483],
      ["2026-11-08", "El toque que hace mono tu chándal", 5375],
      ["2026-11-09", "¿Zapatilla o bailarina?", 1420]
    ],   // [fecha, título, reproducciones] de cada Reel del periodo
    audiencia: {                  // seguidores, Metricool
      fecha: "2026-11-04",
      edad: [["13–17", 0.8], ["18–24", 35.9], ["25–34", 40.0], ["35–44", 10.9], ["45–54", 7.9], ["55–64", 3.2], ["65+", 1.3]],
      paises: [["ES", 69.9], ["AR", 5.7], ["MX", 4.6], ["US", 2.0], ["CL", 1.8]]
    }
  },

  tiktok: {
    seguidores: 1311,
    videos: 21,
    vistas: 13357,
    mediana: 324,
    top: 6655,
    por_video: [
      ["2026-10-16", "Cómo elegir la sudadera perfecta", 363],
      ["2026-10-16", "Tu ropa habla de ti", 344],
      ["2026-10-17", "Mi método para comprar ropa", 387],
      ["2026-10-18", "Oversized y femenina", 6655],
      ["2026-10-19", "¿Qué quieres transmitir con tu outfit?", 357],
      ["2026-10-21", "1 pañuelo, 4 versiones de ti", 336],
      ["2026-10-24", "Vuelven los broches", 467],
      ["2026-10-26", "Vuelven los bolsos XXL", 288],
      ["2026-10-27", "El encaje según cómo lo mezcles", 349],
      ["2026-10-27", "Vuelven los cinturones XXL", 287],
      ["2026-10-27", "Broches y maximalismo", 304],
      ["2026-10-28", "Las medias, protagonistas", 438],
      ["2026-10-29", "Halloween a nuestro estilo", 315],
      ["2026-10-31", "Elige A, B o C", 307],
      ["2026-10-31", "Zapatillas de skate con tacón", 324],
      ["2026-11-01", "Puedes amar una tendencia y no llevarla", 384],
      ["2026-11-02", "El estampado bambi", 275],
      ["2026-11-03", "Oversize y autoestima", 274],
      ["2026-11-04", "Rojo tomate o burdeos", 297],
      ["2026-11-05", "Lo más deseado de la moda", 295],
      ["2026-11-06", "Zapatillas de montaña con falda", 311]
    ]   // [fecha, título, vistas] de cada vídeo del periodo
  },

  // Reel más visto (fuera del periodo de 28 días). Metricool, a la espera de la lectura directa de Instagram
  destacado: {
    plataforma: "Instagram",
    titulo: "¿Vuelven las Nike Shox?",
    fecha: "2026-11-18",
    medido: "2026-11-20",
    horas: 52,
    vistas: 168234,
    url: "https://www.instagram.com/reel/Df4_yVToCd5/"
  },

  // Cifras acumuladas de los trabajos seleccionados (orgánicas)
  trabajos: {
    fecha: "2026-11-10",
    oversized_youtube: 35764, oversized_instagram: 8944, oversized_tiktok: 6655,
    broches_youtube: 19872, broches_instagram: 13018,
    abc_instagram: 13562
  }
};
