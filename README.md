# AP-Downloader
ap.lk downloader

## How to use
1. Copy the following script
2. Navigate to video watching page
2. Type 'j' in search bar and paste the script
3. Press enter and required data will be copied to clipboard automatically!

This code (apdl.py) only download .ts file. Use any video converting app or ffmpeg to convert if you want

Code:
```
avascript:(function(){
    fetch(window.location.href).then(r=>r.text()).then(r=>{
        VideoStreamer=null;
    var u=r.match(/(https?:\/\/.+?\/stream\/[0-9a-f-]+)/g)[0],
        s=r.match(/'([0-9a-f-]+)'/g)[0],s=s.slice(1,s.length-1),
        t=document.title;
        navigator.clipboard.writeText(`python apdl.py ${u} ${s} "${t}.ts"`)
    .then(()=>{
            alert('apdl command copied');
        }).catch(e=>{
            alert('Copy error: '+e.message);
        })
    }).catch(e=>{
        alert('Error: '+e.message);
    })
})();
```
