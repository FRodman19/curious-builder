#!/usr/bin/env python3
"""Offline procedural UI sounds and ambient bed. Requires Python 3 + NumPy; no network.
Events JSON: [{"time": 1.2, "sound": "click", "gain": 0.7}].
"""
import argparse, json, math, wave
from pathlib import Path
import numpy as np
SR = 48000
# Short physical transients are intentionally separate from tonal UI accents.
CATALOG = {
 'mouse_down': ('Mouse press', 'At pointer button down', .055),
 'mouse_up': ('Mouse release', 'At pointer button up', .045),
 'click': ('Mouse click', 'A dry mechanical press and release, at activation', .15),
 'double_click': ('Double click', 'Only when two real clicks occur', .31),
 'key': ('Keyboard key', 'At a visible character insertion', .07),
 'typing': ('Typing', 'A demonstration burst; use individual keys for exact text timing', 1.6),
 'enter': ('Enter key', 'At submission by keyboard, never a mouse submit', .095),
 'backspace': ('Backspace', 'At an actual text deletion', .07),
 'toggle': ('Switch', 'At the checked or selected state change', .08),
 'drag': ('Drag pickup', 'Once when grabbing an object', .1),
 'drop': ('Drop', 'Once when the object is released in its destination', .12),
 'snap': ('Snap into place', 'At a visible alignment or snap point', .065),
 'pop': ('Pop or reveal', 'Optional emphasis on a new object appearing, not a mouse click', .19),
 'transition': ('Panel whoosh', 'With a meaningful moving panel or scene transition', .4),
 'loading_start': ('Loading starts', 'At the beginning of an actual waiting state', .25),
 'loading_loop': ('Loading texture', 'Optional quiet loop while visibly loading; stop at resolution', 2.0),
 'complete': ('Success', 'When the result is visible and complete', .65),
 'attention': ('Warning', 'When a recoverable warning appears', .38),
 'error': ('Error', 'When an action actually fails, not when it merely waits', .5),
 'notification': ('Notification', 'At a new notification or incoming message', .36),
 'undo': ('Undo or restore', 'At the visible reversal of the edit', .26),
}
NAMES = tuple(CATALOG)
def fade(t, duration, attack=.002, release=.012):
    return np.minimum(1, t/attack)**2 * np.minimum(1, np.maximum(0, duration-t)/release)**2

def mechanical(duration, seed, keyboard=False, release=False):
    rng=np.random.default_rng(seed);t=np.arange(round(SR*duration))/SR
    noise=rng.normal(size=len(t))
    # Broadband microswitch snap, not a low sine sweep or cartoon bubble.
    high=noise-np.convolve(noise,np.ones(19)/19,mode='same')
    body=np.convolve(noise,np.ones(9)/9,mode='same')
    f=1150 if keyboard else (2600 if release else 2100)
    y=.7*high*np.exp(-t/(.0018 if release else .003))
    y+=.5*body*np.exp(-t/(.012 if keyboard else .005))
    y+=.23*np.sin(2*np.pi*f*t)*np.exp(-t/.0025)
    if keyboard:y+=.32*np.sin(2*np.pi*330*t)*np.exp(-t/.009)
    return y*fade(t,duration,.00035,.008)

def effect(name, seed=19):
    duration=CATALOG[name][2];t=np.arange(round(SR*duration))/SR
    rng=np.random.default_rng(seed);y=np.zeros(len(t))
    def put(v,at,gain=1):
        i=round(at*SR);n=min(len(v),len(y)-i)
        if n>0:y[i:i+n]+=v[:n]*gain
    if name in ('mouse_down','mouse_up','key','enter','backspace','toggle','snap','drag','drop'):
        y=mechanical(duration,seed,keyboard=name in ('key','enter','backspace','drop'),release=name in ('mouse_up','snap'))
        if name=='enter':y+=.25*np.sin(2*np.pi*190*t)*np.exp(-t/.014)*fade(t,duration)
    elif name in ('click','double_click'):
        for at in ([0] if name=='click' else [0,.155]):
            put(mechanical(.055,seed),at);put(mechanical(.045,seed+1,release=True),at+.063,.65)
    elif name=='typing':
        for i,at in enumerate((0,.12,.245,.34,.49,.69,.83,.965,1.08,1.25,1.41)):
            put(mechanical(.07,seed+i,keyboard=True),at,float(rng.uniform(.55,1)))
    elif name=='pop':
        y=np.sin(2*np.pi*(700*t-1400*t*t))*np.exp(-t*30)
    elif name in ('transition','undo'):
        noise=np.convolve(rng.normal(size=len(t)),np.ones(17)/17,mode='same')
        envelope=np.sin(np.pi*t/duration)**2
        y=noise*envelope
    elif name=='loading_loop':
        # Exact periodic waveform/envelope; file endpoints are zero for a clean loop.
        y=.7*np.sin(2*np.pi*440*t)*np.sin(np.pi*t)**6+.3*np.sin(2*np.pi*660*t)*np.sin(np.pi*t)**6
    else:
        notes={'complete':[(0,523.25),(.1,783.99)],'attention':[(0,330),(.12,293.66)],
               'error':[(0,293.66),(.13,220)],'notification':[(0,659.25)],'loading_start':[(0,392)]}[name]
        for start,freq in notes:
            u=np.maximum(0,t-start)
            y+=(np.sin(2*np.pi*freq*u)+.08*np.sin(2*np.pi*freq*2*u))*np.exp(-u*11)*np.minimum(1,u/.005)*(t>=start)
    y*=fade(t,duration,.00035 if name in ('click','double_click','typing') else .001,.008)
    y-=np.mean(y)*fade(t,duration)
    peak=.09 if name=='loading_loop' else .16
    y*=peak/max(np.max(np.abs(y)),1e-10);y[[0,-1]]=0
    return np.column_stack((y,y)).astype(np.float32)

def ambience(duration, style="warm", gain_db=4):
    # Sparse warm pad, four related voicings; crossfades, no beat or melody.
    chords=((164.81,246.94,311.13,369.99),(138.59,207.65,246.94,329.63),
            (146.83,220,277.18,329.63),(123.47,185,246.94,329.63))
    if style=="focus":
        chords=((130.81,196,246.94,293.66),(146.83,220,261.63,329.63),(164.81,246.94,293.66,392),(130.81,196,261.63,329.63))
    elif style!="warm": raise ValueError("Unknown ambience style")
    out=np.zeros((round(duration*SR),2),np.float32)
    for offset in range(0,len(out),SR*4):
        count=min(SR*4,len(out)-offset); t=(np.arange(count)+offset)/SR
        pos=t/(12 if style=="focus" else 16); k=np.floor(pos).astype(int)%4; x=pos%1
        blend=(.5-.5*np.cos(np.pi*np.clip((x-.65)/.35,0,1)))
        for ch,notes in enumerate(chords):
            weight=(k==ch)*(1-blend)+((k+1)%4==ch)*blend
            if not weight.any(): continue
            for voice,f in enumerate(notes):
                breath=.8+.2*np.sin(2*np.pi*(.031+voice*.007)*t+voice)
                for side in range(2):
                    detune=1+(side*2-1)*.0006
                    tone=np.sin(2*np.pi*f*detune*t+voice*.4)+ .09*np.sin(2*np.pi*f*2*t)
                    if style=="focus": tone*=.8+.2*np.cos(2*np.pi*.6*t+voice*.55)
                    out[offset:offset+count,side]+=(tone*weight*breath*.016).astype(np.float32)
        out[offset:offset+count]*=fade(t,duration,.18,min(1.2,duration/3))[:,None]
    out*=10**(gain_db/20)
    out[[0,-1]]=0
    return out

def write(path, y):
    peak=float(np.max(np.abs(y))); rms=float(np.sqrt(np.mean(y.astype(np.float64)**2)))
    if not np.isfinite(y).all() or peak>=.98: raise ValueError(f'Invalid/clipping audio: {path}')
    with wave.open(str(path),'wb') as w:
        w.setparams((2,2,SR,0,'NONE','not compressed'))
        w.writeframes((np.clip(y,-1,1)*32767).astype('<i2').tobytes())
    return dict(file=path.name,duration=len(y)/SR,peak_dbfs=round(20*math.log10(max(peak,1e-9)),2),rms_dbfs=round(20*math.log10(max(rms,1e-9)),2))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--duration',type=float,default=30)
    p.add_argument('--events',type=Path);p.add_argument('--seed',type=int,default=19)
    p.add_argument('--library',action='store_true',help='Write an auditionable WAV/MP3 library and HTML catalog')
    p.add_argument('--no-ambience',action='store_true',help='Mix effects against silence')
    p.add_argument('--ambience',choices=['warm','focus'],default='warm')
    p.add_argument('--mix-profile',choices=['no-voiceover','narrated'],default='no-voiceover')
    a=p.parse_args()
    sfx_gain=10**((3 if a.mix_profile=='no-voiceover' else -2)/20)
    bed_db=4 if a.mix_profile=='no-voiceover' else -5
    if not 1<=a.duration<=3600: p.error('duration must be 1 to 3600 seconds')
    events=json.loads(a.events.read_text()) if a.events else []
    for e in events:
        if e['sound'] not in NAMES or not 0<=e['time']<a.duration or not 0<=e.get('gain',.65)<=2:
            p.error(f'Invalid event: {e}')
    a.out.mkdir(parents=True,exist_ok=True)
    sounds={n:effect(n,a.seed+i)*sfx_gain for i,n in enumerate(NAMES)}
    assets=[write(a.out/(n+'.wav'),v) for n,v in sounds.items()]
    bed=ambience(a.duration,a.ambience,bed_db);assets.append(write(a.out/'ambience.wav',bed))
    if a.library:
        for style in ('focus',):
            assets.append(write(a.out/('ambience-'+style+'.wav'),ambience(a.duration,style,bed_db)))
    if a.no_ambience: bed[:]=0
    for e in events:
        v=(effect(e['sound'],int(e['seed']))*sfx_gain if 'seed' in e else sounds[e['sound']])*e.get('gain',.65)
        if 'duration' in e:
            size=round(e['duration']*SR)
            if e['sound']!='loading_loop' or size<=0: p.error('Only loading_loop supports a positive duration; schedule individual keys for typing')
            v=np.tile(v,(int(np.ceil(size/len(v))),1))[:size]
            edge=min(round(SR*.035),len(v)//2);v[:edge]*=np.linspace(0,1,edge)[:,None];v[-edge:]*=np.linspace(1,0,edge)[:,None]
        start=round(e['time']*SR)
        end=min(len(bed),start+len(v));bed[start:end]+=v[:end-start]
    # Closing fade also covers any late events.
    tail=min(SR,len(bed));bed[-tail:]*=np.linspace(1,0,tail)[:,None]
    assets.append(write(a.out/'soundtrack.wav',bed))
    preview=ambience(len(NAMES)*2.5+2,a.ambience,bed_db)
    for i,name in enumerate(NAMES):
        v=sounds[name]*.7;start=int((1+i*2.5)*SR);preview[start:start+len(v)]+=v
    assets.append(write(a.out/'preview.wav',preview))
    meta=dict(generator='local_audio.py',method='Procedural oscillators and seeded noise; no API, downloaded samples or model',seed=a.seed,mix_profile=a.mix_profile,ambience_style=a.ambience,sfx_gain_db=3 if a.mix_profile=='no-voiceover' else -2,ambience_gain_db=bed_db,ambient_attack_s=.18,sample_rate=SR,channels=2,events=events,assets=assets)
    (a.out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
    if a.library:
        import subprocess, shutil, html
        if not shutil.which('ffmpeg'): p.error('--library requires local ffmpeg for MP3 copies')
        for item in assets:
            source=a.out/item['file']
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-codec:a','libmp3lame','-q:a','3',str(source.with_suffix('.mp3'))],check=True)
        catalog=[dict(id=n,title=CATALOG[n][0],use=CATALOG[n][1],wav=n+'.wav',mp3=n+'.mp3',provenance='Locally synthesized approximation, not a hardware recording') for n in NAMES]
        (a.out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
        cards=''.join('<article><h2>'+html.escape(x['title'])+'</h2><p>'+html.escape(x['use'])+'</p><audio controls preload="none" src="'+x['mp3']+'"></audio><a download href="'+x['wav']+'">WAV</a> · <a download href="'+x['mp3']+'">MP3</a></article>' for x in catalog)
        page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UI sound library</title><style>*{box-sizing:border-box}body{margin:0;background:#f6f3ef;color:#28231f;font:16px/1.5 system-ui}main{max-width:1100px;margin:auto;padding:40px 20px}h1{font-size:38px;letter-spacing:-1px;margin:0}h2{font-size:19px;margin:0}p{color:#675e55}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px}article{padding:22px;background:#fffdfa;border:1px solid #ded8d0;border-radius:16px}article p{min-height:48px;font-size:14px}audio{display:block;width:100%;margin:16px 0}a{color:#6949a4}.intro{max-width:730px;margin-bottom:30px}</style><main><h1>Sounds that follow the action</h1><p class="intro">21 reusable UI sounds and two ambient backgrounds, generated entirely locally. Mechanical clicks are separate from pops. These are synthesized presentation sounds, not recordings of a particular device.</p><article><h2>Warm</h2><p>Rounded chords with a gentle stereo drift · starts in 0.18 seconds</p><audio controls preload="none" src="ambience.mp3"></audio><a download href="ambience.wav">WAV</a> · <a download href="ambience.mp3">MP3</a></article><p>Play any sound below to compare</p><section>'+cards+'</section></main></html>'
        ambient_cards=''.join('<article><h2>'+title+'</h2><p>'+description+' · starts in 0.18 seconds</p><audio controls preload="none" src="ambience-'+style+'.mp3"></audio><a download href="ambience-'+style+'.wav">WAV</a> · <a download href="ambience-'+style+'.mp3">MP3</a></article>' for style,title,description in [('focus','Focus','A lower, softly pulsing bed for detailed work')])
        page=page.replace('<p>Play any sound below to compare</p>',ambient_cards+'<p>Play any sound below to compare · mixed a little louder for demos without voiceover</p>')
        (a.out/'index.html').write_text(page)
    print(json.dumps(assets,indent=2))
if __name__=='__main__':main()
