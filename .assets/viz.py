# One explanatory, animated diagram per research domain.
# Elements carry v-* classes and a --i index; sketch.css drives the timing and
# the figure only plays once it scrolls into view (see the inline observer).
A='#2d7a3e'; D='#26262f'; S='#55555f'; R='#c0392b'; L='rgba(38,38,47,.14)'

def wrap(h, title, desc, svg, caption, steps):
    return f'''<section class="viz-band" id="viz">
  <figure class="viz reveal d1" data-steps="{steps}">
    <div class="viz-frame">
      <svg viewBox="0 0 900 {h}" role="img" aria-labelledby="vt vd" class="viz-svg">
        <title id="vt">{title}</title><desc id="vd">{desc}</desc>
{svg}
      </svg>
    </div>
    <div class="viz-foot">
      <figcaption class="viz-cap">{caption}</figcaption>
      <button class="viz-replay" type="button">Replay</button>
    </div>
  </figure>
</section>
'''

def assess():
    stages=[("A1-A3","Product",150),("A4-A5","Construction",70),
            ("B1-B7","Use &amp; maintenance",300),("C1-C4","End of life",110)]
    x=90; out=[]
    for i,(code,name,w) in enumerate(stages):
        out.append(f'<g class="v-stage" style="--i:{i}">'
          f'<rect x="{x}" y="150" width="{w}" height="54" fill="{A}" opacity="{0.40+0.11*i:.2f}" stroke="#fff" stroke-width="2"/>'
          f'<text x="{x+w/2}" y="181" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">{code}</text>'
          f'<text x="{x+w/2}" y="224" text-anchor="middle" font-size="13" fill="{S}">{name}</text></g>')
        x+=w+4
    end=x-4; b6x=90+150+4+70+4+120; b6w=110
    return wrap(330,
      "Building life cycle stages and what is counted",
      "Life cycle stages A1 to C4 appear in turn. A marker highlights the small operational slice most accounting counts, then a bracket spans every stage the lab measures.",
      f'''      <text x="90" y="40" font-size="17" font-weight="800" fill="{D}" class="v-title">Where a building's impact actually comes from</text>
      {''.join(out)}
      <g class="v-b6">
        <rect x="{b6x}" y="150" width="{b6w}" height="54" fill="none" stroke="{R}" stroke-width="2.5" stroke-dasharray="5 4"/>
        <text x="{b6x+b6w/2}" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="{R}">B6 operational energy</text>
        <path class="v-draw" d="M{b6x},118 L{b6x},108 L{b6x+b6w},108 L{b6x+b6w},118" fill="none" stroke="{R}" stroke-width="2"/>
        <text x="{b6x+b6w/2}" y="98" text-anchor="middle" font-size="13" font-weight="700" fill="{R}">most accounting stops here</text>
      </g>
      <g class="v-span">
        <path class="v-draw" d="M90,258 L90,270 L{end},270 L{end},258" fill="none" stroke="{A}" stroke-width="2.5"/>
        <text x="{(90+end)/2}" y="292" text-anchor="middle" font-size="14" font-weight="800" fill="{A}">ENSURE Lab measures every stage, across a 50 to 100 year service life</text>
      </g>''',
      "Conventional practice counts only the energy a building uses while occupied (B6). Embodied impacts in materials, construction, repair and demolition sit outside that boundary, and they are what the LCEEA work quantifies.",
      "stages appear, then the usual boundary, then the full one")

def optimize():
    import random
    random.seed(11)
    front=[(155,96),(205,150),(275,192),(365,220),(470,240),(600,253),(715,260),(800,264)]
    def fy(x):
        for i in range(len(front)-1):
            (x1,y1),(x2,y2)=front[i],front[i+1]
            if x1<=x<=x2:
                t=(x-x1)/(x2-x1) if x2>x1 else 0
                return y1+(y2-y1)*t
        return front[-1][1]
    cloud=[]; k=0
    while len(cloud)<44:
        ex=random.uniform(170,800); ey=random.uniform(85,265)
        if ey > fy(ex)-16: continue        # only dominated designs
        cloud.append('<circle class="v-cloud" style="--i:%d" cx="%.0f" cy="%.0f" r="4.5" fill="%s"/>'%(k,ex,ey,S)); k+=1
    pts=' '.join('%d,%d'%(x,y) for x,y in front)
    dots=''.join('<circle class="v-fdot" style="--i:%d" cx="%d" cy="%d" r="6" fill="%s"/>'%(i,x,y,A) for i,(x,y) in enumerate(front))
    cx,cy=365,220
    svg = (
      f'      <text x="70" y="34" font-size="17" font-weight="800" fill="{D}" class="v-title">Every design is a trade-off. The front is where the good ones live.</text>\n'
      f'      <g class="v-legend"><circle cx="596" cy="52" r="5" fill="{S}" opacity=".34"/>'
      f'<text x="610" y="57" font-size="12.5" fill="{S}">candidate design</text>'
      f'<circle cx="736" cy="52" r="5" fill="{A}"/>'
      f'<text x="748" y="57" font-size="12.5" font-weight="700" fill="{A}">the Pareto front</text></g>\n'
      f'      <path class="v-draw v-axis" d="M130,76 L130,300 L840,300" fill="none" stroke="{D}" stroke-width="1.5"/>\n'
      f'      <text x="485" y="332" text-anchor="middle" font-size="13" font-weight="600" fill="{S}" class="v-axlab">Embodied energy and carbon (materials, construction, repair) &#8594;</text>\n'
      f'      <text x="-188" y="86" transform="rotate(-90 0 0)" text-anchor="middle" font-size="13" font-weight="600" fill="{S}" class="v-axlab">Operational energy &#8594;</text>\n'
      f'      {"".join(cloud)}\n'
      f'      <polyline class="v-front" points="{pts}" fill="none" stroke="{A}" stroke-width="3"/>\n'
      f'      {dots}\n'
      f'      <g class="v-pick">'
      f'<circle class="v-ring" cx="{cx}" cy="{cy}" r="11.5" fill="none" stroke="{R}" stroke-width="2.5"/>'
      f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="{R}"/>'
      f'<line x1="300" y1="256" x2="{cx-12}" y2="{cy+8}" stroke="{R}" stroke-width="1.4"/>'
      f'<text x="158" y="262" font-size="13" font-weight="700" fill="{R}">a chosen design</text>'
      f'<text x="158" y="280" font-size="12" fill="{S}">balances both, meets the constraints</text></g>\n'
      f'      <g class="v-note"><text x="596" y="118" font-size="12" fill="{S}">designs up here are beaten</text>'
      f'<text x="596" y="136" font-size="12" fill="{S}">on both counts</text></g>')
    return wrap(356,
      "Trade-off between embodied and operational energy",
      "Candidate designs scatter in, the Pareto front draws through the best of them, and one design on the front is selected.",
      svg,
      "Improving one objective usually worsens the other. Every grey design is beaten by some point on the green front, which is why the front is where the choice actually happens. The lab's optimization work finds that front, then selects from it against real project constraints.",
      "candidates scatter, the front draws, one design is chosen")

def predict():
    def box(cls,i,x,y,w,h,t,sub,fill='#fff',stroke=D,tc=None):
        tc=tc or D
        return (f'<g class="{cls}" style="--i:{i}">'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>'
                f'<text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" font-size="14" font-weight="700" fill="{tc}">{t}</text>'
                f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" font-size="12" fill="{S}">{sub}</text></g>')
    def arrow(cls,i,x1,y,x2,label,col=A):
        return (f'<g class="{cls}" style="--i:{i}">'
                f'<path class="v-draw" d="M{x1},{y} L{x2-10},{y}" fill="none" stroke="{col}" stroke-width="2.5"/>'
                f'<path d="M{x2-10},{y-6} L{x2},{y} L{x2-10},{y+6}Z" fill="{col}"/>'
                f'<text x="{(x1+x2)/2}" y="{y-12}" text-anchor="middle" font-size="12" font-weight="700" fill="{col}">{label}</text></g>')
    return wrap(340,
      "Forward and inverse prediction",
      "A forward chain runs from design variables through a surrogate model to predicted performance. An inverse chain then runs from performance targets back to designs that meet them.",
      f'''      <text x="60" y="34" font-size="17" font-weight="800" fill="{D}" class="v-title">Two directions, one surrogate</text>
      <text x="60" y="80" font-size="13" font-weight="800" fill="{A}" class="v-row" style="--i:0">FORWARD</text>
      {box("v-row",1,60,96,190,66,"Design variables","envelope, glazing, mass")}
      {arrow("v-row",2,250,129,360,"surrogate")}
      {box("v-row",3,360,96,190,66,"Predicted performance","carbon, energy, comfort")}
      {arrow("v-row",4,550,129,660,"in seconds")}
      {box("v-row",5,660,96,180,66,"Decide now","inside a design session","#f2f7f3",A,A)}
      <text x="60" y="212" font-size="13" font-weight="800" fill="{R}" class="v-row" style="--i:6">INVERSE</text>
      {box("v-row",7,60,228,190,66,"Performance targets","a carbon or comfort goal","#fff",R,R)}
      {arrow("v-row",8,250,261,360,"inverse model",R)}
      {box("v-row",9,360,196,190,44,"Design A","meets the target")}
      {box("v-row",10,360,252,190,44,"Design B","meets it differently")}
      {arrow("v-row",11,550,261,660,"explainable",R)}
      {box("v-row",12,660,228,180,66,"Understand why","which variable drove it","#fdf3f2",R,R)}
      <text x="60" y="322" font-size="12.5" fill="{S}" class="v-row" style="--i:13">High-fidelity simulation can take hours per design. A surrogate learns from those runs and answers in real time.</text>''',
      "Forward prediction replaces slow physics simulation with a learned model, so performance can be estimated while a decision is still open. Inverse prediction runs the other way: state the target, get designs that reach it, plus the reason they work.",
      "the forward chain runs, then the inverse chain")

def transform():
    def dot(i,x,y,lab,col=S,op=.55):
        return (f'<g class="v-dot" style="--i:{i}"><circle cx="{x}" cy="{y}" r="6" fill="{col}" opacity="{op}"/>'
                f'<text x="{x+11}" y="{y+4}" font-size="11.5" fill="{S}">{lab}</text></g>')
    return wrap(360,
      "Sustainability and resilience as one decision",
      "A quadrant of life cycle carbon against durability. Materials appear in turn, and the desirable quadrant of long life and low carbon is highlighted.",
      f'''      <text x="90" y="34" font-size="17" font-weight="800" fill="{D}" class="v-title">A building that cannot endure is not sustainable</text>
      <rect class="v-quad" x="465" y="70" width="355" height="115" fill="{A}" opacity=".10"/>
      <path class="v-draw v-axis" d="M110,60 L110,300 L830,300" fill="none" stroke="{D}" stroke-width="1.5"/>
      <line class="v-grid" x1="465" y1="60" x2="465" y2="300" stroke="{L}" stroke-width="1.5"/>
      <line class="v-grid" x1="110" y1="185" x2="830" y2="185" stroke="{L}" stroke-width="1.5"/>
      <text x="470" y="332" text-anchor="middle" font-size="13" font-weight="600" fill="{S}" class="v-axlab">Durability and service life &#8594;</text>
      <text x="-180" y="80" transform="rotate(-90 0 0)" text-anchor="middle" font-size="13" font-weight="600" fill="{S}" class="v-axlab">&#8592; Lower life cycle carbon</text>
      <g class="v-quadlab" style="--i:0"><text x="643" y="96" text-anchor="middle" font-size="13.5" font-weight="800" fill="{A}">low carbon, long life</text>
      <text x="643" y="116" text-anchor="middle" font-size="12" fill="{A}">what the nexus aims for</text></g>
      <g class="v-quadlab" style="--i:1"><text x="288" y="96" text-anchor="middle" font-size="12.5" font-weight="700" fill="{S}">low carbon, short life</text>
      <text x="288" y="114" text-anchor="middle" font-size="11.5" fill="{S}">replaced sooner, carbon paid again</text></g>
      <g class="v-quadlab" style="--i:2"><text x="288" y="262" text-anchor="middle" font-size="12.5" font-weight="700" fill="{S}">high carbon, short life</text></g>
      <g class="v-quadlab" style="--i:3"><text x="643" y="262" text-anchor="middle" font-size="12.5" font-weight="700" fill="{S}">high carbon, long life</text></g>
      {dot(0,250,130,"bio-based, untested")}
      {dot(1,360,225,"conventional")}
      {dot(2,505,150,"climate-responsive assembly")}
      {dot(3,505,174,"bio-inspired, durable",A,.95)}
      <text x="120" y="352" font-size="12.5" fill="{S}" class="v-axlab">Assessed against hurricanes, floods, wildfire, extreme heat, drought, tornadoes and earthquakes.</text>''',
      "Carbon and resilience are usually judged separately. A low-carbon material that fails early has its carbon paid twice over. Plotting both at once moves the decision into the top right, where a building is both low impact and able to endure.",
      "the quadrants label, then each material lands")

def educate():
    steps=[("LOD 100","massing blocks","simple stacked shapes"),
           ("LOD 200","assembly layers","studs, sheathing, finish"),
           ("LOD 300","connections","fixings and detailing"),
           ("LOD 400","fabrication","reinforced, buildable")]
    out=[]; x=70
    for i,(code,name,sub) in enumerate(steps):
        w=170; cells=[]
        for r in range(i+1):
            for c in range(i+1):
                bw=(w-40)/(i+1); bh=70/(i+1)
                cells.append(f'<rect class="v-cell" style="--j:{r*(i+1)+c}" x="{x+20+c*bw+1:.1f}" y="{150+r*bh+1:.1f}" '
                             f'width="{bw-2:.1f}" height="{bh-2:.1f}" fill="{A}" opacity="{0.22+0.14*i:.2f}"/>')
        out.append(f'<g class="v-panel" style="--i:{i}">'
          f'<rect x="{x}" y="120" width="{w}" height="120" rx="3" fill="#fff" stroke="{D}" stroke-width="1.8"/>'
          f'{"".join(cells)}'
          f'<text x="{x+w/2}" y="142" text-anchor="middle" font-size="12.5" font-weight="800" fill="{A}">{code}</text>'
          f'<text x="{x+w/2}" y="262" text-anchor="middle" font-size="13" font-weight="700" fill="{D}">{name}</text>'
          f'<text x="{x+w/2}" y="280" text-anchor="middle" font-size="11.5" fill="{S}">{sub}</text></g>')
        if i<3:
            ax=x+w+6
            out.append(f'<g class="v-arrow" style="--i:{i}"><path class="v-draw" d="M{ax},180 L{ax+14},180" stroke="{S}" stroke-width="2" fill="none"/>'
                       f'<path d="M{ax+10},175 L{ax+16},180 L{ax+10},185Z" fill="{S}"/></g>')
        x+=w+26
    return wrap(340,
      "Levels of development in the Virtual Construction Lab",
      "Four panels appear in turn, each subdividing further, from simple massing blocks to a fabrication-level assembly.",
      f'''      <text x="70" y="40" font-size="17" font-weight="800" fill="{D}" class="v-title">Build the wall in VR before building it for real</text>
      <text x="70" y="66" font-size="13" fill="{S}" class="v-axlab">Learners progress through levels of development, each adding detail the previous one hid.</text>
      {''.join(out)}
      <text x="70" y="318" font-size="12.5" fill="{S}" class="v-axlab">Mistakes are free here. That is the point: repeat the task until the sequence is understood, then do it on site.</text>''',
      "The Virtual Construction Lab steps from a simplified block model to a fabrication-level assembly. Each level exposes detail the previous one abstracted away, so the sequence of construction is learned by doing rather than read from a drawing.",
      "each level of development builds up in turn")

VIZ={'assess':assess,'optimize':optimize,'predict':predict,'transform':transform,'educate':educate}
