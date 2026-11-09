import os
import json, sys, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pairs.py')).read())
from playwright.sync_api import sync_playwright
from urllib.parse import quote
import os
HERE=os.path.dirname(os.path.abspath(__file__))
BASE='file://'+os.path.abspath(os.path.join(HERE,'..'))+'/'
OUT=os.path.join(HERE,'data.json')
data=json.load(open(OUT)) if os.path.exists(OUT) else {}
JS="""()=>{const q=s=>document.querySelector(s);
 const steps=[...document.querySelectorAll('ol.steps li')].map(li=>{const t=li.querySelector('.st-t');const m=li.querySelector('.st-m');
   const title=t?[...t.childNodes].filter(n=>n!==m).map(n=>n.textContent).join('').trim():'';
   const s=li.querySelector('.st-s'); const warns=[...li.querySelectorAll('.warn')].map(w=>w.textContent.trim());
   return {t:title,m:m?m.textContent.trim():'',s:s?s.textContent.trim():'',w:warns,end:li.classList.contains('end')};});
 const warnTop=[...document.querySelectorAll('#sheet > .warn, #sheet p.warn')].map(w=>w.textContent.trim());
 return {eta:q('.eta-n')?.textContent.trim()||null, sub:q('.eta-s')?.textContent.trim()||null, steps, alt:[...document.querySelectorAll('.altnote')].map(a=>a.textContent.trim()), warnTop};}"""
def run(pg,lang,a,c,f,by,fp):
    path=('' if lang=='en' else lang+'/')+'index.html'
    pg.goto(BASE+path+f'#from={quote(a)}&to={quote(c)}&f={f}&by={by}'+('&fp=1' if fp else '')); pg.reload(); pg.wait_for_timeout(550)
    return pg.evaluate(JS)
other={'horde':'alliance','alliance':'horde'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900})
    pg.route('**/*',lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    for s,a,c,f,g in PAIRS:
        if s in data: continue
        d={'a':a,'b':c,'f':f,'g':g,'en':{},'fr':{},'es':{},'de':{}}
        for by in ['foot','form','m60','m100']: d['en'][by]=run(pg,'en',a,c,f,by,False)
        d['en']['fly']=run(pg,'en',a,c,f,'m100',True)
        d['en']['rev_foot']=run(pg,'en',c,a,f,'foot',False)
        d['en']['rev_fly']=run(pg,'en',c,a,f,'m100',True)
        d['en']['other']=run(pg,'en',a,c,other[f],'foot',False)
        for L in ['fr','es','de']:
            d[L]['foot']=run(pg,L,a,c,f,'foot',False)
            d[L]['fly']=run(pg,L,a,c,f,'m100',True)
            d[L]['other']=run(pg,L,a,c,other[f],'foot',False)
        data[s]=d; json.dump(data,open(OUT,'w'),ensure_ascii=False)
        print(s,d['en']['foot']['eta'],d['en']['fly']['eta'],d['en']['other']['eta'],flush=True)
    b.close()
