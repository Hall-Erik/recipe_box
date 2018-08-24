(function() {
	document.getElementById('file_input').onchange = function() {
		var files = document.getElementById('file_input').files;
		var file = files[0];
		if(!file){
			return alert("No file selected.");
		}
		var progress = document.getElementById('progress');
		progress.className = 'progress';
		var progressBar = document.getElementById('progress-bar');
		progressBar.setAttribute("style", "width: 33%;");
		getSignedRequest(file);
	};
})();

function getSignedRequest(file){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				var progressBar = document.getElementById('progress-bar');
				progressBar.setAttribute("style", "width: 66%;");
				uploadFile(file, response.data, response.url);
			}
			else{
				var progress = document.getElementById('progress');
				progress.className = 'd-none';
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}

function uploadFile(file, s3Data, url){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", s3Data.url);

	var postData = new FormData();
	for(key in s3Data.fields){
		postData.append(key, s3Data.fields[key]);
	}
	postData.append('file', file);

	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200 || xhr.status === 204){
				document.getElementById('preview').src = url;
				document.getElementById('image_url').value = url;
			}
			else{
				alert("Could not upload file.");
			}
			var progress = document.getElementById('progress');
			progress.className = 'd-none';
		}
	};
	xhr.send(postData);
}