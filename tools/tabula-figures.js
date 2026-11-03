/* Tabula figures: cheerful illustrations inside a calm page.
   Every figure gets its own pair of bright colours (a cold one in place of --ether, a warm one in place of --warm),
   fills become dense and flat, lines get thicker and rounder, dots bigger, and the canvas sits on a soft tint
   of its cold colour. The figures' own code is untouched: colours are swapped where they are painted. */
(function(){
  var PAL={blue:['#4F6BFF','#EAEEFF','#2C47D6'],green:['#22B07A','#E0F5EC','#12784F'],violet:['#8A5CFF','#EFE8FF','#5B33C9'],sky:['#1FB2EA','#E0F4FC','#0B7FAD'],
           coral:['#FF6F59','#FFE9E3','#C7402A'],yellow:['#FFC21A','#FFF4CC','#B37F00'],pink:['#FF6BA8','#FFE6F0','#C2306F']};
  var PAIRS=[['blue','coral']]; /* one pair for every figure: the system's cold and warm accents */
  var NAMES={blue:['син','soft'],green:['зелён','hard'],violet:['фиолетов','hard'],sky:['голуб','hardo']};
  var OFF=+(document.documentElement.dataset.palOffset||0);
  function hex(h){h=h.trim();if(h[0]==='#'){if(h.length===4)h='#'+h[1]+h[1]+h[2]+h[2]+h[3]+h[3];return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16),1];}
    var m=h.match(/rgba?\(([^)]+)\)/);if(m){var p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return [p[0],p[1],p[2],p.length>3?p[3]:1];}return null;}
  var root=document.documentElement;
  var base=null,baseTheme=null;
  function tok(n){return getComputedStyle(root).getPropertyValue(n).trim();}
  function dark(){var t=root.getAttribute('data-theme');return t==='dark'||(t!=='light'&&matchMedia('(prefers-color-scheme: dark)').matches);}
  function B(){var th=dark()?'d':'l';if(base&&baseTheme===th)return base;baseTheme=th;
    base={E:hex(tok('--ether')),W:hex(tok('--warm')),Es:hex(tok('--ether-soft')),Ws:hex(tok('--warm-soft')),paper:hex(tok('--paper'))};return base;}
  function eq(a,b){return a&&b&&Math.abs(a[0]-b[0])<3&&Math.abs(a[1]-b[1])<3&&Math.abs(a[2]-b[2])<3;}
  function mix(a,b,t){return [a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t];}
  function css(c,a){return 'rgba('+Math.round(c[0])+','+Math.round(c[1])+','+Math.round(c[2])+','+(+a.toFixed(3))+')';}
  function pairOf(cv){var f=cv&&cv.closest&&cv.closest('figure');if(!f)return null;if(!f._pal)assign(f);return f._pal;}
  function assign(f){var all=[].slice.call(document.querySelectorAll('figure'));var i=all.indexOf(f);var pr=PAIRS[((i+OFF)%PAIRS.length+PAIRS.length)%PAIRS.length];
    var P=PAL[pr[0]],S=PAL[pr[1]];f._pal={p:pr[0],s:pr[1],P:hex(P[0]),Ps:hex(P[1]),Pi:hex(P[2]),S:hex(S[0]),Ss:hex(S[1]),Si:hex(S[2])};
    f.dataset.pal=pr[0]+'-'+pr[1];
  }
  window.TabulaPal={assign:assign,PAIRS:PAIRS,NAMES:NAMES};
  /* map one colour of the old two-accent scheme to the figure's pair */
  var cache=new Map();
  function map(v,cv,fill){if(typeof v!=='string')return v;var pr=pairOf(cv);if(!pr)return v;var k=v+'|'+(fill?1:0)+'|'+pr.p+pr.s+'|'+baseTheme;
    if(cache.has(k))return cache.get(k);var c=hex(v),b=B(),out=v;
    if(c){var a=c[3],boost=function(x){return x>=0.999?1:Math.min(fill?0.95:1,x*1.45+0.14);};
      var dk=dark();var P=dk?mix(pr.P,[255,255,255],0.12):pr.P,S=dk?mix(pr.S,[255,255,255],0.1):pr.S;
      if(eq(c,b.E))out=css(P,boost(a));
      else if(eq(c,b.W))out=css(S,boost(a));
      else if(eq(c,b.Es))out=css(dk?mix(b.paper,P,0.22):pr.Ps,a);
      else if(eq(c,b.Ws))out=css(dk?mix(b.paper,S,0.22):pr.Ss,a);
      else{ /* a mix of the two accents: the same mix of the pair */
        var d=[b.W[0]-b.E[0],b.W[1]-b.E[1],b.W[2]-b.E[2]],L=d[0]*d[0]+d[1]*d[1]+d[2]*d[2],t=((c[0]-b.E[0])*d[0]+(c[1]-b.E[1])*d[1]+(c[2]-b.E[2])*d[2])/L;
        if(t>0.02&&t<0.98){var q=mix(b.E,b.W,t),e=Math.hypot(c[0]-q[0],c[1]-q[1],c[2]-q[2]);if(e<14)out=css(mix(P,S,t),boost(a));}}}
    cache.set(k,out);return out;}
  /* gauges, swatches and SVG drawn by the scripts get their colours inline: those follow the pair too */
  var PROPS=['background','backgroundColor','color','borderColor','borderLeftColor','fill','stroke'];
  function fixEl(el){var f=el.closest&&el.closest('figure[data-pal]');if(!f)return;var st=el.style;
    PROPS.forEach(function(k){var v=st[k];if(!v||v.indexOf('var(')>=0)return;var m=v.replace(/(#[0-9a-fA-F]{3,6}|rgba?\([^)]*\))/g,function(c){return map(c,el,k!=='color'&&k!=='stroke');});if(m!==v)st[k]=m;});
    ['fill','stroke'].forEach(function(k){var v=el.getAttribute&&el.getAttribute(k);if(v&&/^(#|rgb)/.test(v)){var m=map(v,el,k==='fill');if(m!==v)el.setAttribute(k,m);}});}
  new MutationObserver(function(ms){ms.forEach(function(m){if(m.type==='attributes')fixEl(m.target);else m.addedNodes.forEach(function(n){if(n.nodeType===1){fixEl(n);n.querySelectorAll&&[].forEach.call(n.querySelectorAll('[style],[fill],[stroke]'),fixEl);}});});})
    .observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['style','fill','stroke']});
  window.TabulaPal.fixAll=function(){[].forEach.call(document.querySelectorAll('figure[data-pal] [style],figure[data-pal] [fill],figure[data-pal] [stroke]'),fixEl);};
  var C=CanvasRenderingContext2D.prototype;
  function wrapProp(name,fill){var d=Object.getOwnPropertyDescriptor(C,name);Object.defineProperty(C,name,{configurable:true,get:function(){return d.get.call(this);},
    set:function(v){var m=map(v,this.canvas,fill);this['_y'+name]=(m!==v&&/^rgba\((255,194,26)/.test(m));d.set.call(this,m);}});}
  C.__origFill=Object.getOwnPropertyDescriptor(C,'fillStyle');wrapProp('fillStyle',true);wrapProp('strokeStyle',false);
  /* gradients: stops go through the same map */
  ['createLinearGradient','createRadialGradient','createConicGradient'].forEach(function(n){var o=C[n];if(!o)return;C[n]=function(){var g=o.apply(this,arguments),cv=this.canvas,a=g.addColorStop;g.addColorStop=function(s,c){return a.call(g,s,map(c,cv,true));};return g;};});
  /* thicker, rounder lines for the drawing itself; hairlines (axes, grids) stay thin */
  var lw=Object.getOwnPropertyDescriptor(C,'lineWidth');
  Object.defineProperty(C,'lineWidth',{configurable:true,get:function(){return lw.get.call(this);},set:function(v){if(v>=1.6&&pairOf(this.canvas))v=Math.min(6,v*1.4);lw.set.call(this,v);}});
  var st=C.stroke;C.stroke=function(){if(lw.get.call(this)>=2&&pairOf(this.canvas)){this.lineCap='round';this.lineJoin='round';}return st.apply(this,arguments);};
  /* bigger dots */
  var arc=C.arc;C.arc=function(x,y,r,a0,a1,ccw){if(r>1.2&&r<=6&&Math.abs((a1||0)-(a0||0))>6.2&&pairOf(this.canvas))r=r*1.3;return arc.call(this,x,y,r,a0,a1,ccw);};
  /* yellow text is unreadable: text in the yellow accent uses its ink */
  var ft=C.fillText,FD=C.__origFill;C.fillText=function(){if(this._yfillStyle){var pr=pairOf(this.canvas);this.save();FD.set.call(this,css(pr.s==='yellow'?pr.Si:pr.Si,1));var r=ft.apply(this,arguments);this.restore();return r;}
    return ft.apply(this,arguments);};
  /* a soft tint behind the drawing: the full-size paper fill becomes the tint */
  var fr=C.fillRect;C.fillRect=function(x,y,w,h){var cv=this.canvas,pr=pairOf(cv);
    if(pr&&x<=1&&y<=1&&w>=cv.width*0.95&&h>=cv.height*0.95){var c=hex(String(this.fillStyle)),b=B();if(c&&eq(c,b.paper)){var s=this.fillStyle;this.fillStyle=dark()?css(mix(b.paper,pr.P,0.08),1):css(mix(pr.Ps,[255,255,255],0.35),1);var r=fr.apply(this,arguments);this.fillStyle=s;return r;}}
    return fr.apply(this,arguments);};
})();
