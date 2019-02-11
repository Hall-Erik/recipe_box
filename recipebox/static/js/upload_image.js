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
		
		resizeImage({
			file: file,
			maxSize: 200
		}).then(function (resizedImage) {
			getSignedRequest(resizedImage);
		});
	};
})();

function resizeImage(settings) {
    var file = settings.file;
    var maxSize = settings.maxSize;
    var reader = new FileReader();
    var image = new Image();
    var canvas = document.createElement('canvas');
    var dataURItoBlob = function (dataURI) {
        var bytes = dataURI.split(',')[0].indexOf('base64') >= 0 ?
            atob(dataURI.split(',')[1]) :
            unescape(dataURI.split(',')[1]);
        var mime = dataURI.split(',')[0].split(':')[1].split(';')[0];
        var max = bytes.length;
        var ia = new Uint8Array(max);
        for (var i = 0; i < max; i++)
            ia[i] = bytes.charCodeAt(i);
        return new Blob([ia], { type: mime });
    };
    var resize = function () {
        var width = image.width;
        var height = image.height;
        if (width > height) {
            if (width > maxSize) {
                height *= maxSize / width;
                width = maxSize;
            }
        } else {
            if (height > maxSize) {
                width *= maxSize / height;
                height = maxSize;
            }
        }
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(image, 0, 0, width, height);
        var dataUrl = canvas.toDataURL('image/jpeg');
        return dataURItoBlob(dataUrl);
    };
    return new Promise(function (ok, no) {
        if (!file.type.match(/image.*/)) {
            no(new Error("Not an image"));
            return;
        }
        reader.onload = function (readerEvent) {
            image.onload = function () { return ok(resize()); };
            image.src = readerEvent.target.result;
        };
        reader.readAsDataURL(file);
    });
};

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