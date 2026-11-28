"""glasskit: tiny design system for the README graphics (Apple-style glass on aurora)."""
import html
from icons_ph import PH

SANS = "-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Inter','Segoe UI',system-ui,'Helvetica Neue',Arial,sans-serif"
MONO = "'SF Mono','JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

PAL = {
 'dark': dict(text='#F5F5F7', muted='#A1A1A6', faint='#6E6E73', acc='#3D9BFF', accg='#7DBBFF', btn='#0A84FF', acc2='#5E5CE6', acc3='#FF375F', teal='#64D2FF',
              ok='#30D158', warn='#FF9F0A', base='#07080C', base2='#10131B', b1='#0A84FF', b2='#5E5CE6', b3='#64D2FF',
              bo=.82, gA=.06, hl=.075, sHi=.40, sMid=.11, sLo=.05, ln='#FFFFFF', lno=.10, sh='#000000', shop=.38, sheen=.16, outline=0,
              card='#171A23', card2='#1D212C', border='#2B3040', dim='#2C3140', chip='#1F2330', white='#FFFFFF'),
 'light': dict(text='#1D1D1F', muted='#515154', faint='#86868B', acc='#0071E3', accg='#0071E3', btn='#0071E3', acc2='#5E5CE6', acc3='#E8265A', teal='#2593C9',
               ok='#1E9B47', warn='#C77700', base='#E9EFFF', base2='#F5EFFF', b1='#79B1FF', b2='#B9A9FF', b3='#9BDFFF',
               bo=.9, gA=.55, hl=.75, sHi=1.0, sMid=.6, sLo=.4, ln='#0B1B3A', lno=.10, sh='#5B6B9A', shop=.20, sheen=.7, outline=.07,
               card='#FFFFFF', card2='#F3F5FA', border='#D9DFEC', dim='#DDE3F0', chip='#EDF1F9', white='#FFFFFF'),
}

def esc(s): return html.escape(str(s), quote=True)
def tw(s, size, mono=False, bold=False):
    return len(s) * size * (0.6 if mono else (0.57 if bold else 0.53))

_n = [0]
def uid():
    _n[0] += 1
    return _n[0]

CSS = ("text{font-family:%s}.m{font-family:%s}"
       "@keyframes in{from{opacity:0;transform:translateY(16px) scale(.985)}to{opacity:1;transform:translateY(0) scale(1)}}"
       "@keyframes blink{0%%,49%%{opacity:1}50%%,100%%{opacity:0}}"
       ".in{opacity:0;transform-box:fill-box;transform-origin:50%% 50%%;animation:in 1s cubic-bezier(.16,1,.3,1) forwards}"
       ".blink{animation:blink 1.05s steps(1) infinite}"
       "@media (prefers-reduced-motion:reduce){.in{animation:none;opacity:1}.blink{animation:none}}") % (SANS, MONO)

def common_defs(P):
    return (
     '<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="%s"/><stop offset=".45" stop-color="#fff" stop-opacity="%s"/><stop offset="1" stop-color="#fff" stop-opacity="%s"/></linearGradient>'
     '<linearGradient id="bdS" x1="0" y1="0" x2="1" y2="1"><animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="7s" repeatCount="indefinite"/>'
     '<stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".25" stop-color="%s" stop-opacity=".95"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset=".75" stop-color="%s" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity=".10"/></linearGradient>'
     '<linearGradient id="hl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="%s"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
     '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity="%s"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
     '<linearGradient id="bgs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
     '<filter id="bl60" x="-60%%" y="-60%%" width="220%%" height="220%%"><feGaussianBlur stdDeviation="60"/></filter>'
     '<filter id="bl30" x="-60%%" y="-60%%" width="220%%" height="220%%"><feGaussianBlur stdDeviation="30"/></filter>'
     '<filter id="glo" x="-300%%" y="-300%%" width="700%%" height="700%%"><feGaussianBlur stdDeviation="6"/></filter>'
     '<filter id="bl14" x="-30%%" y="-40%%" width="160%%" height="190%%"><feGaussianBlur stdDeviation="14"/></filter>'
     '<filter id="gr" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".07"/></feComponentTransfer></filter>'
    ) % (P['sHi'], P['sMid'], P['sLo'], P['acc'], P['acc2'], P['hl'], P['sheen'], P['base'], P['base2'])

def svg(w, h, body, defs='', P=None):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" fill="none">'
            '<style>%s</style><defs>%s%s</defs>%s</svg>') % (w, h, w, h, CSS, common_defs(P) if P else '', defs, body)

def fade(content, delay=0, x=0, y=0):
    return '<g transform="translate(%s %s)"><g class="in" style="animation-delay:%.2fs">%s</g></g>' % (x, y, delay, content)

def glass(x, y, w, h, P, r=20, shadow=True, sweep=False, spin=False, fill=None, fop=None):
    n = uid(); g = ''
    if shadow:
        g += ('<mask id="m%d" maskUnits="userSpaceOnUse" x="%d" y="%d" width="%d" height="%d"><rect x="%d" y="%d" width="%d" height="%d" fill="#fff"/><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#000"/></mask>'
              '<g mask="url(#m%d)"><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s" filter="url(#bl14)"/></g>'
              ) % (n, x - 70, y - 60, w + 140, h + 150, x - 70, y - 60, w + 140, h + 150, x, y, w, h, r, n, x + 6, y + 14, w - 12, h - 6, r, P['sh'], P['shop'])
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" fill-opacity="%s"/>' % (x, y, w, h, r, fill or '#fff', P['gA'] if fop is None else fop)
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="url(#hl)"/>' % (x, y, w, h, r)
    if sweep:
        g += ('<clipPath id="c%d"><rect x="%s" y="%s" width="%s" height="%s" rx="%s"/></clipPath><g clip-path="url(#c%d)"><rect x="%s" y="%s" width="110" height="%s" fill="url(#sheen)" transform="skewX(-20)">'
              '<animate attributeName="x" values="%s;%s;%s" keyTimes="0;.35;1" dur="8s" repeatCount="indefinite"/></rect></g>'
              ) % (n, x, y, w, h, r, n, x - 260, y - 10, h + 20, x - 260, x + w + 160, x + w + 160)
    if P['outline']:
        g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" stroke="%s" stroke-opacity="%s"/>' % (x - .5, y - .5, w + 1, h + 1, r + .5, P['ln'], P['outline'])
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" stroke="url(#%s)" stroke-width="1.2"/>' % (x + .5, y + .5, w - 1, h - 1, r - .5, 'bdS' if spin else 'bd')
    return g

def page(wi, hi, P, body, blobs=None, pad=20, r=28, defs=''):
    W, H = wi + 2 * pad, hi + 2 * pad
    blobs = blobs or [(140, 70, 190, 'b1', .40, 70, 40, 17), (W - 130, H - 40, 210, 'b2', .36, -70, -30, 21)]
    bl = ''
    for (cx, cy, rad, c, op, dx, dy, dur) in blobs:
        bl += ('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s" filter="url(#bl60)">'
               '<animate attributeName="cx" values="%s;%s;%s" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="%ss" repeatCount="indefinite"/>'
               '<animate attributeName="cy" values="%s;%s;%s" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="%ss" repeatCount="indefinite"/></circle>'
               ) % (cx, cy, rad, P.get(c, c), round(op * P.get('bo', 1), 3), cx, cx + dx, cx, dur, cy, cy + dy, cy, dur + 3)
    out = ('<clipPath id="slab"><rect width="%d" height="%d" rx="%d"/></clipPath><g clip-path="url(#slab)"><rect width="%d" height="%d" fill="url(#bgs)"/>%s'
           '<rect width="%d" height="%d" filter="url(#gr)"/></g><rect x=".5" y=".5" width="%d" height="%d" rx="%d" stroke="%s" stroke-opacity=".14"/>'
           '<g transform="translate(%d %d)">%s</g>') % (W, H, r, W, H, bl, W, H, W - 1, H - 1, r, P['ln'], pad, pad, body)
    return svg(W, H, out, defs, P)

def odometer(digit, x, y, size, color, delay=0.4, weight=700):
    n = uid(); lh = size * 1.3
    col = ''.join('<text x="0" y="%.1f" font-size="%s" font-weight="%s" fill="%s" letter-spacing="-1">%d</text>' % (i * lh, size, weight, color, i) for i in range(10))
    return ('<clipPath id="o%d"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath><g clip-path="url(#o%d)"><g transform="translate(%s %s)"><g>'
            '<animateTransform attributeName="transform" type="translate" from="0 0" to="0 %.1f" dur="1.9s" begin="%ss" fill="freeze" calcMode="spline" keySplines=".16 1 .3 1" keyTimes="0;1"/>%s</g></g></g>'
            ) % (n, x - 2, y - size * .85, size * .66, size * 1.05, n, x, y, -digit * lh, delay, col)

def odo_number(text, x, y, size, color, delay=0.4):
    out = ''; cx = x; dw = size * .6
    for ch in str(text):
        if ch.isdigit():
            out += odometer(int(ch), cx, y, size, color, delay); cx += dw
        else:
            out += '<text x="%s" y="%s" font-size="%s" font-weight="700" fill="%s">%s</text>' % (cx, y, size, color, esc(ch)); cx += size * .34
    return out, cx - x

# 24x24 stroke glyphs --------------------------------------------------------
GLYPHS = {
 'api': '<path d="M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4"/>',
 'shield': '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
 'gauge': '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/>',
 'responsive': '<rect x="3" y="5" width="13" height="10" rx="1.8"/><path d="M1.5 19h16"/><rect x="15" y="9" width="6.5" height="11" rx="1.8"/>',
 'server': '<rect x="4" y="4" width="16" height="6" rx="2"/><rect x="4" y="14" width="16" height="6" rx="2"/><path d="M8 7h.01M8 17h.01"/>',
 'state': '<circle cx="6" cy="6" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="12" cy="18" r="2.6"/><path d="M8.3 7.3L11 15.5M15.7 7.3L13 15.5M8.7 6h6.6"/>',
 'sparkle': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17v4M17 19h4"/>',
 'agile': '<path d="M20 12a8 8 0 0 0-14-5.3M4 4v4h4M4 12a8 8 0 0 0 14 5.3M20 20v-4h-4"/>',
 'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l3 3M14 9l2 2"/>',
 'db': '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>',
 'cap': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-4.5"/>',
 'flame': '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 .3 1.2 1 1.8 1.8 2C10.5 8 11 5.5 12 3z"/>',
 'trophy': '<path d="M7 4h10v5a5 5 0 0 1-10 0zM7 6H3.5A3.5 3.5 0 0 0 7 10M17 6h3.5A3.5 3.5 0 0 1 17 10M12 14v4M8 20h8"/>',
 'bars': '<path d="M5 20V12M12 20V5M19 20v-6"/>',
 'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5.5a3 3 0 0 1 0 5.8M18 14.5c1.8.8 3 2.5 3 5.5"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="3.8" ry="9"/><path d="M3 12h18"/>',
 'code': '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
 'bolt': '<path d="M13 2L5 13h6l-1 9 8-11h-6z"/>',
 'layers': '<path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5"/>',
 'cube': '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12L4 7.5M12 12v9"/>',
 'plane': '<path d="M21 4L3 11l6 2 2 6 3-5 7-10z"/>',
 'dumbbell': '<path d="M6.5 6.5v11M17.5 6.5v11M3.5 9v6M20.5 9v6M6.5 12h11"/>',
 'palette': '<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-1 1.5-2.2-.5-1.2.3-2.3 1.6-2.3H17a4 4 0 0 0 4-4c0-5-4-9.5-9-9.5z"/><path d="M7.5 11h.01M10 7.5h.01M14.5 7.5h.01"/>',
 'waves': '<path d="M2 9c2.5-2.5 5-2.5 7.5 0s5 2.5 7.5 0M2 15c2.5-2.5 5-2.5 7.5 0s5 2.5 7.5 0M17 9c1.5 1.4 3 1.4 5 0M17 15c1.5 1.4 3 1.4 5 0"/>',
 'camera': '<path d="M4 8h3l1.6-2.5h6.8L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.8"/>',
 'paddle': '<circle cx="12" cy="9" r="6.5"/><rect x="10.3" y="15.6" width="3.4" height="6" rx="1.4"/><circle cx="19.5" cy="18.5" r="1.7"/>',
 'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
 'pin': '<path d="M12 21s-6.5-5.7-6.5-11a6.5 6.5 0 0 1 13 0c0 5.3-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'arrow': '<path d="M7 17L17 7M9 7h8v8"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'award': '<circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.5L7 21l5-2.5 5 2.5-1.5-7.5"/>',
 'package': '<path d="M12 3l8 4v10l-8 4-8-4V7zM4 7l8 4 8-4M12 11v10"/>',
}
GLYPH_MAP = {'api': 'arrows-left-right', 'shield': 'shield-check', 'gauge': 'gauge', 'responsive': 'devices', 'server': 'hard-drives', 'state': 'graph',
 'sparkle': 'sparkle', 'agile': 'arrows-clockwise', 'key': 'key', 'db': 'database', 'cap': 'graduation-cap', 'flame': 'flame', 'trophy': 'trophy',
 'bars': 'chart-bar', 'heart': 'heart', 'users': 'users-three', 'globe': 'globe-hemisphere-east', 'code': 'code', 'bolt': 'lightning', 'layers': 'stack',
 'cube': 'cube', 'plane': 'airplane-tilt', 'dumbbell': 'barbell', 'palette': 'palette', 'waves': 'waves', 'camera': 'camera', 'paddle': 'ping-pong',
 'mic': 'microphone-stage', 'pin': 'map-pin', 'check': 'check-circle', 'arrow': 'arrow-up-right', 'clock': 'clock', 'award': 'certificate',
 'package': 'package', 'briefcase': 'briefcase', 'rocket': 'rocket-launch', 'medal': 'medal', 'star': 'star', 'seal': 'seal-check', 'send': 'paper-plane-tilt', 'coffee': 'coffee', 'terminal': 'terminal-window', 'branch': 'git-branch', 'merge': 'git-merge'}

def glyph(name, x, y, size, color, sw=1.8):
    inner = PH[GLYPH_MAP.get(name, name)].replace('opacity="0.2"', 'opacity="0.4"')
    return '<svg x="%s" y="%s" width="%s" height="%s" viewBox="0 0 256 256" fill="%s">%s</svg>' % (x, y, size, size, color, inner)

def squircle_icon(x, y, size, name, color, P, delay=0):
    """Frosted glass tile with a duotone glyph. Accent glyphs use the brighter glyph blue so they stay readable on dark; gold is kept for earned items."""
    n = uid(); r = size * .3; light = P['gA'] > .3
    c = P['warn'] if color == P['warn'] else (P['accg'] if color == P['acc'] else P['muted'])
    g = '<clipPath id="tl%d"><rect x="%s" y="%s" width="%s" height="%s" rx="%s"/></clipPath>' % (n, x, y, size, size, r)
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#fff" fill-opacity="%s"/>' % (x, y, size, size, r, .85 if light else .10)
    g += '<g clip-path="url(#tl%d)"><circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/><rect x="%s" y="%s" width="%s" height="%s" fill="url(#hl)"/></g>' % (n, x + size * .3, y + size * .15, size * .8, c, .16 if light else .36, x, y, size, size)
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" stroke="%s" stroke-opacity="%s"/>' % (x + .5, y + .5, size - 1, size - 1, r, c, .5 if light else .7)
    g += glyph(name, x + size * .21, y + size * .21, size * .58, c)
    return g
