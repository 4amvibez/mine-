import subprocess
F="/root/.claude/uploads/fb3f0fdd-1672-5c4e-9452-7e15893874e1/68a7fb4b-video_20261114_113617.mp4"
X=0.3
T={'A':0,'B':3.5,'C':4.92,'D':11.22,'E':15.70,'F':19.22,'G':23.42,'H':30.28,'END':36.3}
order=['A','B','C','D','E','F','G','H']
L={k:T[order[i+1] if i+1<len(order) else 'END']-T[k]+(X if i+1<len(order) else 0) for i,k in enumerate(order)}
clips={'B':[(125.6,2.0,1)],'C':[(0.5,3.3,1),(16.5,3.4,1)],'D':[(22.0,4.0,1)],'E':[(44.5,4.0,1)],'F':[(60.0,2.2,1),(68.0,2.4,1)],'G':[(121.0,2.6,0.7)]}
def run(a): subprocess.run(['ffmpeg','-loglevel','error','-y']+a,check=True)
for k in ['A','H']:
    d='fr_intro' if k=='A' else 'fr_end'
    run(['-framerate','30','-i',f'{d}/%04d.jpg','-vf',f'trim=duration={L[k]},setpts=PTS-STARTPTS,fps=30,format=yuv420p','-c:v','libx264','-crf','18','-an',f'sc_{k}.mp4'])
for k,cl in clips.items():
    D=L[k]; ins=[]; f=[]
    for i,(st,ln,sp) in enumerate(cl):
        ins+=['-ss',str(st),'-t',str(ln),'-i',F]
        f.append(f'[{i}:v]setpts=(PTS-STARTPTS)/{sp},fps=30,scale=1080:-2,setsar=1[c{i}]')
    f.append(''.join(f'[c{i}]' for i in range(len(cl)))+f'concat=n={len(cl)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=10,trim=duration={D},setpts=PTS-STARTPTS[s]')
    f.append(f"[s]scale=w='trunc(1080*(1+0.07*t/{D})/2)*2':h=-2:eval=frame,crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,setsar=1[z]")
    f.append(f'[{len(cl)}:v]format=rgba,fade=in:st=0.2:d=0.35:alpha=1[cp]')
    f.append('[z][cp]overlay=0:0:shortest=1,fps=30,format=yuv420p[v]')
    run(ins+['-loop','1','-framerate','30','-t',str(D),'-i',f'cap_{k}.png','-filter_complex',';'.join(f),'-map','[v]','-c:v','libx264','-crf','18','-t',str(D),'-an',f'sc_{k}.mp4'])
# chain with crossfades
ins=[]; 
for k in order: ins+=['-i',f'sc_{k}.mp4']
f=[]; prev='[0:v]'
for i in range(1,len(order)):
    out=f'[x{i}]'; f.append(f"{prev}[{i}:v]xfade=transition={'fadewhite' if i==1 else 'fade'}:duration={X}:offset={T[order[i]]}{out}"); prev=out
run(ins+['-filter_complex',';'.join(f),'-map',prev,'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','30','video2_noaudio.mp4'])
print({k:round(v,2) for k,v in L.items()})
