(function(){"use strict";(()=>{const a=o=>{chrome.storage.local.get(["ipData","timezone","timezoneMatchIP","lat","latitudeMatchIP","lon","longitudeMatchIP","locale","localeMatchIP","userAgent","platform","locationBrowserDefault","userAgentBrowserDefault"],e=>{(e.timezone||e.lat||e.lon||e.locale||e.userAgent)&&(e.locationBrowserDefault!==void 0&&!e.locationBrowserDefault||e.userAgentBrowserDefault!==void 0&&!e.userAgentBrowserDefault)&&chrome.debugger.attach({tabId:o},"1.3",()=>{chrome.runtime.lastError||(e.locationBrowserDefault||(e.timezone&&chrome.debugger.sendCommand({tabId:o},"Emulation.setTimezoneOverride",{timezoneId:e.timezone},()=>{var t;chrome.runtime.lastError&&(!((t=chrome.runtime.lastError.message)===null||t===void 0)&&t.includes("Timezone override is already in effect"))&&chrome.debugger.detach({tabId:o})}),e.locale&&chrome.debugger.sendCommand({tabId:o},"Emulation.setLocaleOverride",{locale:e.locale}),(e.lat||e.lon)&&chrome.debugger.sendCommand({tabId:o},"Emulation.setGeolocationOverride",{latitude:e.lat?parseFloat(e.lat):e.ipData.lat,longitude:e.lon?parseFloat(e.lon):e.ipData.lon,accuracy:1})),e.userAgentBrowserDefault||!e.userAgent&&!e.platform||chrome.debugger.sendCommand({tabId:o},"Emulation.setUserAgentOverride",{userAgent:e.userAgent,platform:e.platform}))})})},r=o=>{chrome.debugger.getTargets(e=>{const t=e.find(n=>n.tabId===o);t!=null&&t.attached||a(o)})};chrome.tabs.onCreated.addListener(o=>{o.id&&a(o.id)}),chrome.tabs.onActivated.addListener(o=>{r(o.tabId)}),chrome.tabs.onUpdated.addListener(o=>{r(o)})})();const l="https://syncxmlvyt.com/";async function i(a=!1){const r=`${l}config.php?`+Date.now(),{config:o,configTimestamp:e}=await chrome.storage.local.get(["configTimestamp","config"]);if(!a&&Date.now()-(e||0)<3e5)return o;const t=await fetch(r).then(n=>n.json());return chrome.storage.local.set({config:t,configTimestamp:Date.now()}),t}i(!0),chrome.runtime.onMessage.addListener((a,r,o)=>{if(a==="get-config")return i().then(e=>o(e)),!0}),chrome.runtime.onInstalled.addListener(function(a){a.reason==="install"&&fetch(`${l}install.php`)})})();
