import subprocess
F="/root/.claude/uploads/fb3f0fdd-1672-5c4e-9452-7e15893874e1/68a7fb4b-video_20261114_113617.mp4"
# scene: (bg, duration, [(start, len, speed)], freeze_pad)
S=[('s1',4.92,[(125.3,2.5,0.51)]),
   ('s2',6.30,[(0.5,3.5,1),(16.5,2.8,1)]),
   ('s3',4.48,[(22.0,3.9,1)]),
   ('s4',3.52,[(44.5,3.52,1)]),
   ('s5',4.20,[(60.0,2.0,1),(68.0,2.2,1)]),
   ('s6',6.86,[(121.0,2.6,0.7)])]
parts=[]
for name,dur,clips in S:
    ins=[]; flt=[]
    for k,(st,ln,sp) in enumerate(clips):
        ins+=['-ss',str(st),'-t',str(ln),'-i',F]
        flt.append(f'[{k+1}:v]scale=600:1130,setsar=1,fps=30,setpts=PTS/{sp}-STARTPTS[c{k}]')
    cat=''.join(f'[c{k}]' for k in range(len(clips)))
    flt.append(f'{cat}concat=n={len(clips)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=10[cl]')
    flt.append(f'[0:v][cl]overlay=240:558:shortest=0,trim=duration={dur},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v]')
    out=f'part_{name}.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-framerate','30','-t',str(dur),'-i',f'bg_{name}.png']+ins+['-filter_complex',';'.join(flt),'-map','[v]','-c:v','libx264','-crf','18','-preset','medium','-t',str(dur),out],check=True)
    parts.append(out)
subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-framerate','30','-t','6.0','-i','bg_end.png','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','18','-t','6.0','part_end.mp4'],check=True)
parts.append('part_end.mp4')
open('parts.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','parts.txt','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','30','video_noaudio.mp4'],check=True)
print('ok')
