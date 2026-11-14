const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const S=JSON.parse(process.argv[2]);
for(const [name,qs] of S){ await p.goto('file://'+process.cwd()+(name==='end'?'/end.html':'/bg.html?'+qs)); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(250); await p.screenshot({path:`bg_${name}.png`}); }
await b.close()})()
