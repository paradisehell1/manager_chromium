const tabs = {};
chrome.runtime.onMessage.addListener(async (e) => {
  if ('offscreen' !== e.target) {
    return;
  }
  switch (e.name) {
    case 'startRecording': {
      const a = e.streamId,
        t = e.tabId,
        n = e.value;
      await captureTab(a, t);
      tabs[t].gainNode.gain.value = n;
      chrome.runtime.sendMessage({
        name: 'updateVolume',
        target: 'background',
        tabId: t,
        value: n,
      });
      break;
    }
    case 'setVolume': {
      const t = e.tabId,
        n = e.value;
      tabs[t].gainNode.gain.value = n;
      chrome.runtime.sendMessage({
        name: 'updateVolume',
        target: 'background',
        tabId: t,
        value: n,
      });
      break;
    }
    case 'disposeTab': {
      const t = e.tabId;
      tabs[t].audioContext.close();
      delete tabs[t];
      chrome.runtime.sendMessage({
        name: 'disposeTab',
        target: 'background',
        tabId: t,
      });
      break;
    }
  }
});
const captureTab = async (e, a) => {
    const t = await navigator.mediaDevices.getUserMedia({
        audio: {
          mandatory: { chromeMediaSource: 'tab', chromeMediaSourceId: e },
        },
      }),
      n = new AudioContext(),
      o = n.createMediaStreamSource(t),
      r = n.createGain();
    o.connect(r),
      r.connect(n.destination),
      (tabs[a] = { audioContext: n, gainNode: r });
  }