(async function() {const BOOL = true;while (BOOL) {$('#time').text(new Date().toLocaleTimeString());await new Promise(r => setTimeout(r, 500))}})()
