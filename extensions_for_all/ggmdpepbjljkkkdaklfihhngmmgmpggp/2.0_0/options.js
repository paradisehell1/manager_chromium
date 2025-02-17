function flash_message(text){
	var message = document.getElementById("message");
	
	message.innerHTML = text;
	message.style.display = "block";
	
	setTimeout(function() {
		message.style.display = "none";
		message.innerHTML = "";
	}, 2000);
}

function show_error(message){
	document.getElementById('blockError').innerHTML = message;
	document.getElementById('blockError').style.display = 'block';
}
function hide_error(){
	document.getElementById('blockError').style.display = 'none';
}

// Saves options to localStorage.
function save_options() {

	var inputLogin = document.getElementById("login");
	var inputPassword = document.getElementById("password");
	var inputRetry = document.getElementById("retry");
	
	localStorage["proxy_login"] = inputLogin.value;
	localStorage["proxy_password"] = inputPassword.value;
	
	var retry = parseInt(inputRetry.value);
	if(retry !== NaN && retry >= 2){
		localStorage["proxy_retry"] = retry;
	} else{
		localStorage["proxy_retry"] = DEFAULT_RETRY_ATTEMPTS;
		document.getElementById("retry").value = DEFAULT_RETRY_ATTEMPTS;
	}
	
	unlock();
	hide_error();

	// Update message to let user know options were saved.
	flash_message('Credentials saved !');
}

function reset(){
	var inputLogin = document.getElementById("login");
	var inputPassword = document.getElementById("password");
	var inputRetry = document.getElementById("retry");
	
	inputLogin.value = '';
	inputPassword.value = '';
	inputRetry.value = DEFAULT_RETRY_ATTEMPTS;
	
	localStorage["proxy_login"] = '';
	localStorage["proxy_password"] = '';
	localStorage["proxy_retry"] = DEFAULT_RETRY_ATTEMPTS;
	unlock();
	hide_error();
}

// Restores options to saved value from localStorage.
function restore_options() {
  var login = localStorage["proxy_login"] || "";
  var password = localStorage["proxy_password"] || "";
  var retry = localStorage["proxy_retry"] || DEFAULT_RETRY_ATTEMPTS || 5;
  // If locked, display alert.
  if(typeof localStorage["proxy_locked"] === 'string' && localStorage["proxy_locked"] === 'true'){
	show_error('The extension is locked because too many authentication attempts were done.<br/>This is to avoid you to be locked by the proxy server settings.<br/>To unlock the application, enter your credentials again.');
  }
  
  var inputLogin = document.getElementById("login");
  var inputPassword = document.getElementById("password");
  var inputRetry = document.getElementById("retry");
  
  inputLogin.value = login;
  inputPassword.value = password;
  inputRetry.value = retry;
}
document.addEventListener('DOMContentLoaded', restore_options);
document.querySelector('#save').addEventListener('click', save_options);
document.querySelector('#reset').addEventListener('click', reset);
document.querySelector('#version').innerHTML = chrome.runtime.getManifest().name + " v" + chrome.runtime.getManifest().version;