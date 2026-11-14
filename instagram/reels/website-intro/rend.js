const {chromium}=require('playwright');const fs=require('fs');(async()=>{const [mode,out]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
if(mode==='caps'){const C=JSON.parse(fs.readFileSync('caps.json'));for(const [n,qs] of C){await p.goto('file://'+process.cwd()+'/cap.html?'+qs);await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:`cap_${n}.png`,omitBackground:true});}}
else{fs.mkdirSync(out,{recursive:true});await p.goto('file://'+process.cwd()+'/prof.html?m='+mode);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
const T=await p.evaluate(()=>window.TOTAL);const n=Math.round(T*30);for(let i=0;i<n;i++){await p.evaluate(t=>window.render(t),i/30);await p.screenshot({path:`${out}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}}
await b.close()})()
