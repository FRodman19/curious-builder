#!/usr/bin/env python3
"""Assemble existing keyframe images into a labeled, aspect-preserving review sheet."""
import argparse, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

def wrapped(text,font,width,draw):
    lines=[]
    for para in str(text).splitlines() or ['']:
        line=''
        for word in para.split():
            if draw.textlength(word,font=font)>width:
                raise ValueError('Label contains a word too long for the tile')
            candidate=(line+' '+word).strip()
            if line and draw.textlength(candidate,font=font)>width:lines.append(line);line=word
            else:line=candidate
        lines.append(line)
    return lines

def build(manifest,output):
    manifest=Path(manifest).resolve();m=json.loads(manifest.read_text());root=manifest.parent
    frames=m.get('frames',[])
    if not frames:raise ValueError('At least one frame is required')
    cols=int(m.get('columns',3));w=int(m.get('tile_width',420));h=int(m.get('tile_height',300))
    if not 1<=cols<=8 or min(w,h)<100:raise ValueError('Invalid sheet dimensions')
    if output.exists():raise ValueError('Output already exists; choose a new review revision')
    fallback=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    fontpath=(root/m['font']).resolve() if m.get('font') else fallback
    if not fontpath.is_file():raise ValueError('Supply a usable TTF/OTF font path in the manifest')
    font=ImageFont.truetype(str(fontpath),19);small=ImageFont.truetype(str(fontpath),15);titlefont=ImageFont.truetype(str(fontpath),30)
    measure=ImageDraw.Draw(Image.new('RGB',(1,1)));gap=24;pad=28
    width=2*pad+cols*w+(cols-1)*gap
    titlelines=wrapped(m.get('title','Contact sheet'),titlefont,width-2*pad,measure)
    top=pad+len(titlelines)*38+gap;cells=[]
    for f in frames:
        path=(root/f['file']).resolve()
        with Image.open(path) as im:
            image=ImageOps.exif_transpose(im).convert('RGB');image.thumbnail((w,h),Image.Resampling.LANCZOS)
        labels=wrapped(f.get('label',path.stem),font,w,measure)
        notes=wrapped(f.get('note',''),small,w,measure)
        cells.append((image,labels,notes))
    rows=[cells[i:i+cols] for i in range(0,len(cells),cols)]
    heights=[h+12+max(len(c[1])*25+len(c[2])*21 for c in row)+gap for row in rows]
    sheet=Image.new('RGB',(width,top+sum(heights)+pad),m.get('background','#EAE6E0'));d=ImageDraw.Draw(sheet)
    for i,line in enumerate(titlelines):d.text((pad,pad+i*38),line,font=titlefont,fill='#24211E')
    y=top
    for row,rh in zip(rows,heights):
        for j,(im,labels,notes) in enumerate(row):
            x=pad+j*(w+gap);sheet.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2));ty=y+h+12
            for line in labels:d.text((x,ty),line,font=font,fill='#24211E');ty+=25
            for line in notes:d.text((x,ty),line,font=small,fill='#665F56');ty+=21
        y+=rh
    output.parent.mkdir(parents=True,exist_ok=True);sheet.save(output)
    return {'frames':len(frames),'width':sheet.width,'height':sheet.height,'output':str(output)}

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:print(json.dumps(build(a.manifest,a.output)))
    except (ValueError,KeyError,OSError) as e:p.exit(1,f'{e}\n')
if __name__=='__main__':main()
