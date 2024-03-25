# AP-Downloader
ap.lk downloader

## How to use
1. Copy one of the following scripts accoording to your system
2. Navigate to video watching page
2. Type 'j' in search bar and paste the script
3. Press enter and required data will be copied to clipboard automatically!

For windows:
```
avascript:(function(){
    fetch(window.location.href).then(r=>r.text()).then(r=>{
        VideoStreamer=null;
		var u=r.match(/(https?:\/\/.+?\/stream\/[0-9a-f-]+)/g)[0],t=document.title;
        navigator.clipboard.writeText(`ffmpeg -i ${u} -c copy "${t}.mp4"`)
		.then(()=>{
            alert('ffmpeg command copied');
        }).catch(e=>{
            alert('Copy error: '+e.message);
        })
    }).catch(e=>{
        alert('Error: '+e.message);
    })
})();
```

For android
```
avascript:(function(){
    fetch(window.location.href).then(r=>r.text()).then(r=>{
        VideoStreamer=null;
		var u=r.match(/(https?:\/\/.+?\/stream\/[0-9a-f-]+)/g)[0],t=document.title;
        navigator.clipboard.writeText(u)
		.then(()=>{
            alert('URL copied, use 1DM app to download');
        }).catch(e=>{
            alert('Copy error: '+e.message);
        })
    }).catch(e=>{
        alert('Error: '+e.message);
    })
})();
```