"""Pure-python SVG artwork for the login page (factory + live ANOMATRIX monitoring cards)."""

FACTORY_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400" width="1280" height="800">
<style>
.smoke{animation:smoke 4.5s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes smoke{0%{transform:translateY(0) scale(.6);opacity:.55}100%{transform:translateY(-80px) scale(2.2);opacity:0}}
.box{animation:belt 9s linear infinite}
@keyframes belt{from{transform:translateX(-90px)}to{transform:translateX(700px)}}
.ping{animation:ping 2.2s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes ping{0%{transform:scale(.4);opacity:.9}100%{transform:scale(2.8);opacity:0}}
.float{animation:float 4.5s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.win{animation:flick 3.2s ease-in-out infinite}
@keyframes flick{0%,100%{opacity:1}50%{opacity:.5}}
.arm{animation:arm 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:0% 100%}
@keyframes arm{0%,100%{transform:rotate(0deg)}50%{transform:rotate(-9deg)}}
text{font-family:Arial,Helvetica,sans-serif}
</style>
<defs>
  <linearGradient id="bld" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2F6EA3"/><stop offset="1" stop-color="#1B4468"/></linearGradient>
  <linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E2A44"/><stop offset="1" stop-color="#08192B"/></linearGradient>
</defs>

<!-- ground -->
<rect x="0" y="330" width="640" height="70" fill="url(#gnd)"/>
<rect x="0" y="330" width="640" height="2" fill="#3FA0E0" opacity=".5"/>

<!-- smoke -->
<circle class="smoke" cx="131" cy="118" r="11" fill="#FFFFFF"/>
<circle class="smoke" style="animation-delay:-1.5s" cx="133" cy="118" r="11" fill="#FFFFFF"/>
<circle class="smoke" style="animation-delay:-3s" cx="129" cy="118" r="11" fill="#FFFFFF"/>
<circle class="smoke" style="animation-delay:-.8s" cx="241" cy="132" r="10" fill="#FFFFFF"/>
<circle class="smoke" style="animation-delay:-2.4s" cx="243" cy="132" r="10" fill="#FFFFFF"/>

<!-- chimneys -->
<rect x="120" y="125" width="22" height="75" fill="#2A6394"/><rect x="120" y="125" width="22" height="9" fill="#E65D70"/>
<rect x="230" y="140" width="22" height="60" fill="#2A6394"/><rect x="230" y="140" width="22" height="9" fill="#E65D70"/>

<!-- main hall -->
<path d="M90 200 L90 168 L150 200 L150 168 L210 200 L210 168 L270 200 L270 168 L330 200 L330 168 L390 200 Z" fill="#3A7AB0"/>
<rect x="90" y="200" width="300" height="130" fill="url(#bld)"/>
<g fill="#FFD27A">
  <rect class="win" x="108" y="228" width="34" height="22" rx="3"/>
  <rect class="win" style="animation-delay:-.7s" x="158" y="228" width="34" height="22" rx="3"/>
  <rect class="win" style="animation-delay:-1.4s" x="208" y="228" width="34" height="22" rx="3"/>
  <rect class="win" style="animation-delay:-2.1s" x="258" y="228" width="34" height="22" rx="3"/>
  <rect class="win" style="animation-delay:-2.8s" x="308" y="228" width="34" height="22" rx="3"/>
</g>
<rect x="344" y="272" width="36" height="58" rx="3" fill="#0F2F4E"/>
<rect x="108" y="268" width="226" height="6" fill="#0F2F4E" opacity=".35"/>

<!-- warehouse + tank -->
<rect x="410" y="262" width="120" height="68" fill="url(#bld)"/>
<rect x="404" y="252" width="132" height="12" rx="3" fill="#3A7AB0"/>
<rect x="430" y="284" width="30" height="46" fill="#0F2F4E"/><rect x="470" y="284" width="30" height="46" fill="#0F2F4E"/>
<rect x="552" y="236" width="48" height="94" rx="14" fill="#2F6EA3"/>
<rect x="552" y="262" width="48" height="5" fill="#9DC3E3" opacity=".6"/><rect x="552" y="290" width="48" height="5" fill="#9DC3E3" opacity=".6"/>

<!-- robot arm -->
<rect x="22" y="296" width="36" height="34" rx="5" fill="#9DB3C6"/>
<g class="arm"><path d="M40 298 L66 258 L104 276" stroke="#DCEBF7" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<circle cx="104" cy="276" r="6" fill="#E5A04B"/></g>
<circle cx="40" cy="298" r="8" fill="#183B5B"/><circle cx="66" cy="258" r="6" fill="#183B5B"/>

<!-- conveyor + moving crates -->
<rect x="0" y="346" width="640" height="14" rx="7" fill="#3B5F80"/>
<g fill="#183B5B"><circle cx="30" cy="353" r="3"/><circle cx="100" cy="353" r="3"/><circle cx="170" cy="353" r="3"/><circle cx="240" cy="353" r="3"/><circle cx="310" cy="353" r="3"/><circle cx="380" cy="353" r="3"/><circle cx="450" cy="353" r="3"/><circle cx="520" cy="353" r="3"/><circle cx="590" cy="353" r="3"/></g>
<g class="box"><rect x="0" y="324" width="30" height="22" rx="3" fill="#E5A04B"/><rect x="0" y="333" width="30" height="3" fill="#B97A2C"/></g>
<g class="box" style="animation-delay:-3s"><rect x="0" y="324" width="30" height="22" rx="3" fill="#E5A04B"/><rect x="0" y="333" width="30" height="3" fill="#B97A2C"/></g>
<g class="box" style="animation-delay:-6s"><rect x="0" y="324" width="30" height="22" rx="3" fill="#E5A04B"/><rect x="0" y="333" width="30" height="3" fill="#B97A2C"/></g>

<!-- sensor pings -->
<g>
  <circle class="ping" cx="300" cy="289" r="10" fill="#E65D70"/><circle cx="300" cy="289" r="5" fill="#E65D70" stroke="#fff" stroke-width="2"/>
  <circle class="ping" style="animation-delay:-.9s" cx="475" cy="300" r="10" fill="#20A77A"/><circle cx="475" cy="300" r="5" fill="#20A77A" stroke="#fff" stroke-width="2"/>
  <circle class="ping" style="animation-delay:-1.5s" cx="576" cy="270" r="10" fill="#20A77A"/><circle cx="576" cy="270" r="5" fill="#20A77A" stroke="#fff" stroke-width="2"/>
  <circle class="ping" style="animation-delay:-.4s" cx="66" cy="258" r="10" fill="#E5A04B"/><circle cx="66" cy="258" r="5" fill="#E5A04B" stroke="#fff" stroke-width="2"/>
</g>
<path d="M300 289 L300 190 L262 108" stroke="#E65D70" stroke-width="1.5" stroke-dasharray="4 4" fill="none" opacity=".8"/>
<path d="M576 270 L576 160 L560 120" stroke="#20A77A" stroke-width="1.5" stroke-dasharray="4 4" fill="none" opacity=".8"/>

<!-- floating monitoring cards -->
<g class="float">
  <rect x="150" y="22" width="190" height="66" rx="12" fill="#FFFFFF" opacity=".97"/>
  <rect x="150" y="22" width="5" height="66" rx="2" fill="#E65D70"/>
  <text x="166" y="42" font-size="9" fill="#6F8496" letter-spacing="1.5" font-weight="700">M-07 · AIR COMPRESSOR</text>
  <text x="166" y="64" font-size="16" fill="#C23A4F" font-weight="800">2.5 days to limit</text>
  <text x="166" y="79" font-size="9.5" fill="#5B6F7E">Bearing wear detected · Risk 92/100</text>
</g>
<g class="float" style="animation-delay:-2s">
  <rect x="420" y="38" width="200" height="82" rx="12" fill="#FFFFFF" opacity=".97"/>
  <text x="436" y="58" font-size="9" fill="#6F8496" letter-spacing="1.5" font-weight="700">VIBRATION · LIVE</text>
  <text x="436" y="80" font-size="17" fill="#14273A" font-weight="800">8.2 <tspan font-size="10" fill="#7A8791">mm/s</tspan></text>
  <polyline points="436,106 458,100 478,104 498,92 518,97 538,84 558,90 578,76 604,70" fill="none" stroke="#E65D70" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<g class="float" style="animation-delay:-1s">
  <rect x="18" y="126" width="150" height="58" rx="12" fill="#FFFFFF" opacity=".97"/>
  <text x="32" y="146" font-size="9" fill="#6F8496" letter-spacing="1.5" font-weight="700">PLANT HEALTH INDEX</text>
  <text x="32" y="168" font-size="17" fill="#20A77A" font-weight="800">84%</text>
  <rect x="78" y="160" width="76" height="7" rx="3.5" fill="#E6EAF0"/><rect x="78" y="160" width="64" height="7" rx="3.5" fill="#20A77A"/>
</g>
</svg>
"""