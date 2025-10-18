<!DOCTYPE raycast.com/?via=Auraecosystem>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Aura++ Docs — Voice Reactive Intelligence</title>

  <link rel="stylesheet" href="//unpkg.com/prismjs/themes/prism-tomorrow.css" />

  <style>
    :root {
      --aura-glow: 0.5;
      --aura-light: hsl(190, 100%, 65%);
      --aura-dark: hsl(270, 100%, 70%);
    }

    body {
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg, #0d0d0d);
      color: var(--fg, #fff);
      transition: background 0.4s, color 0.4s;
      overflow-x: hidden;
    }

    #app {
      position: relative;
      z-index: 2;
      padding: 2rem;
    }

    #aura-overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none;
      z-index: 1;
      background: transparent;
    }

    .glow-text {
      text-shadow: 0 0 calc(20px * var(--aura-glow)) var(--aura-light),
                   0 0 calc(40px * var(--aura-glow)) var(--aura-dark);
      transition: text-shadow 0.2s ease-in-out;
    }
  </style>
</head>

<body>
  <div id="aura-overlay"></div>
  <div id="app">🎧 Loading Aura++ Docs...</div>

  <!-- Docsify -->
  <script src="//unpkg.com/docsify/lib/docsify.min.js"></script>
  <script src="//unpkg.com/docsify/lib/plugins/search.min.js"></script>
  <script src="//unpkg.com/docsify/lib/plugins/emoji.min.js"></script>

  <!-- Prism -->
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-typescript.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-javascript.min.js"></script>

  <!-- Aura / WebXR Scripts -->
  <script src="/resources/testharness.js"></script>
  <script src="/resources/testdriver.js"></script>
  <script src="/resources/testdriver-vendor.js"></script>

  <script>
    // === THEME ADAPTATION ===
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.body.style.setProperty('--bg', prefersDark ? '#0d0d0d' : '#f7f7f7');
    document.body.style.setProperty('--fg', prefersDark ? '#fff' : '#111');
    if (!prefersDark) {
      document.documentElement.style.setProperty('--aura-light', 'hsl(45, 100%, 60%)');
      document.documentElement.style.setProperty('--aura-dark', 'hsl(210, 100%, 60%)');
    }

    // === CANVAS AURA ===
    const canvas = document.getElementById('aura-overlay');
    const ctx = canvas.getContext('2d');
    canvas.width = innerWidth;
    canvas.height = innerHeight;

    let particles = Array.from({ length: 75 }, () => ({
      x: Math.random() * innerWidth,
      y: Math.random() * innerHeight,
      r: Math.random() * 2 + 1,
      dx: (Math.random() - 0.5) * 1.2,
      dy: (Math.random() - 0.5) * 1.2,
      color: `hsl(${Math.random() * 360}, 100%, 70%)`
    }));

    function drawParticles(intensity = 0.5) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const p of particles) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r + intensity * 3, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = 0.6 + intensity * 0.4;
        ctx.fill();
        p.x += p.dx * (1 + intensity);
        p.y += p.dy * (1 + intensity);
        if (p.x < 0 || p.x > innerWidth) p.dx *= -1;
        if (p.y < 0 || p.y > innerHeight) p.dy *= -1;
      }
      requestAnimationFrame(() => drawParticles(currentGlow));
    }

    // === VOICE REACTIVE GLOW ===
    let currentGlow = 0.5;
    function startAudioReactiveAura() {
      navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        const audioCtx = new AudioContext();
        const src = audioCtx.createMediaStreamSource(stream);
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        src.connect(analyser);

        const data = new Uint8Array(analyser.frequencyBinCount);
        function updateGlow() {
          analyser.getByteFrequencyData(data);
          const avg = data.reduce((a, b) => a + b) / data.length;
          currentGlow = Math.min(1, avg / 120);
          document.documentElement.style.setProperty('--aura-glow', currentGlow);
          requestAnimationFrame(updateGlow);
        }
        updateGlow();
      }).catch(err => console.warn("Audio permission denied:", err));
    }
    startAudioReactiveAura();
    drawParticles();

    // === DOCSIFY CONFIG ===
    const keywords = ["AI", "Quantum", "Neural", "Data", "Blockchain", "Discovery"];
    window.$docsify = {
      name: "Aura++ Docs",
      repo: "",
      loadSidebar: true,
      subMaxLevel: 3,
      search: "auto",
      markdown: {
        renderer: {
          code: function(code, lang) {
            const glow = keywords.some(k => code.includes(k)) ? "glow-text" : "";
            return `<pre class="language-${lang} ${glow}"><code>${Prism.highlight(code, Prism.languages[lang] || Prism.languages.markup, lang)}</code></pre>`;
          }
        }
      }
    };
    
    <picture>
  <source media="(min-width: 800px)" srcset="large.jpg 1x, larger.jpg 2x">
  <img src="image.png" loading="lazy" alt="…" style="height:200px; width:200px;">
      <img src="image.png" loading="lazy" alt="…" width="200" height="200">
      <img src="photo.jpg" loading="lazy">
</picture>

    // === RESIZE HANDLER ===
    window.addEventListener("resize", () => {
      canvas.width = innerWidth;
      canvas.height = innerHeight;
    });
    // <!-- Let's load this in-viewport image normally -->
<img src="hero.jpg" alt="…">

<!-- Let's lazy-load the rest of these images -->
<img data-src="unicorn.jpg" alt="…" loading="lazy" class="lazyload">
<img data-src="cats.jpg" alt="…" loading="lazy" class="lazyload">
<img data-src="dogs.jpg" alt="…" loading="lazy" class="lazyload">

<script>
  if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
      img.src = img.dataset.src;
    });
  } else {
    // Dynamically import the LazySizes library
    const script = document.createElement('script');
    script.src =
      'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.1.2/lazysizes.min.js';
    document.body.appendChild(script);
  if ('loading' in HTMLImageElement.prototype) {
  // supported in browser
} 
  else {
  // fetch polyfill/third-party library
<!-- visible in the viewport -->
<img src="product-1.jpg" alt="..." width="200" height="200">
<img src="product-2.jpg" alt="..." width="200" height="200">
<img src="product-3.jpg" alt="..." width="200" height="200">

<!-- offscreen images -->
<img src="product-4.jpg" loading="lazy" alt="..." width="200" height="200">
<img src="product-5.jpg" loading="lazy" alt="..." width="200" height="200">
<img src="product-6.jpg" loading="lazy" alt="..." width="200" height="200">
  }
  
</script>
</body>
</html>
