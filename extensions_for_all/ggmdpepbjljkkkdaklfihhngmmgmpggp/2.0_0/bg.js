//var bkg = chrome.extension.getBackgroundPage();
var calls = {};

// Shows settings on install.
chrome.runtime.onInstalled.addListener(function(details) {
	if(details.reason && (details.reason === 'install') || (details.reason === 'update')){
		chrome.tabs.create({url: "options.html"});
	}
});
// Show settings when clicking on the icon.
chrome.browserAction.onClicked.addListener(function() {
	chrome.tabs.create({url: "options.html"}, function(tab) {
		console.log('options loaded');
	});
});

/* Notifications */
chrome.notifications.onShowSettings.addListener(function(){
	chrome.tabs.create({url: "options.html"});
});
chrome.notifications.onClicked.addListener(function(id){
	if(id === NOTIFICATION_ID){
		chrome.tabs.create({url: "options.html"});
	}
});

/* Core */
chrome.webRequest.onAuthRequired.addListener(
	function(details) {
	
		var locked = isLocked();
		var idstr = details.requestId.toString();
	
		if(details.isProxy === true && !locked){
		
			console.log('AUTH - ' + details.requestId);
			//console.log(JSON.stringify(details));
			
			if(!(idstr in calls)){
				calls[idstr] = 0;
			}
			calls[idstr] = calls[idstr] + 1;
			
			var retry = parseInt(localStorage["proxy_retry"]) || DEFAULT_RETRY_ATTEMPTS || 5;
			
			if(calls[idstr] >= retry){
				lock();
				chrome.notifications.create(NOTIFICATION_ID, {
					'type': 'basic',
					'iconUrl': 'icon_locked_128.png',
					'title': 'Proxy Auto Auth error',
					'message': 'A lot of Proxy Authentication requests have been detected. There is probably a mistake in your credentials. For your safety, the extension has been temporary locked. To unlock it, click the save button in the options.',
					'isClickable': true,
					'priority': 2
				}, function(id){ 
					//console.log('notification callback'); 
				});
				calls = {};
				return({
					cancel : true
				});
			}
			
			var login = localStorage["proxy_login"];
			var password = localStorage["proxy_password"];
			
			if (login && password && !locked){
				return({
					authCredentials : {
						'username' : login,
						'password' : password
					}
				});
			}
		}
	},
	{urls: ["<all_urls>"]}, 
	["blocking"]
);

/*
chrome.webRequest.onBeforeSendHeaders.addListener(
	function(details) {
		for (var i = 0; i < details.requestHeaders.length; ++i) {
			if (details.requestHeaders[i].name === 'Proxy-Authorization') {
				console.log('Proxy-Authorization is set');
				// details.requestHeaders.splice(i, 1);
				break;
			}
		}
		
		// console.log(JSON.stringify(details));
		console.log(details.requestId + ' - ' + details.url);
		
		// details.requestHeaders.push({
			// 'name': 'X-Proxy-Authorization',
			// 'value': 'Basic MTox'
		// });
		return {requestHeaders: details.requestHeaders};
	},
	{urls: ["<all_urls>"]},
	["blocking", "requestHeaders"]
);
*/