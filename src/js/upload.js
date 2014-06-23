function show_error(message) {
	$(".alert").alert('close');
	loc = $("#alert");
	loc.append('<div class="alert alert-danger fade in">' +
			'<button type="button" class="close"' +
			'data-dismiss="alert" aria-hidden="true">' +
			'&times;</button>' + message + '</div>');
}

function show_info(message) {
	$(".alert").alert('close');
	loc = $("#alert");
	loc.append('<div class="alert alert-success fade in">' +
			'<button type="button" class="close"' +
			'data-dismiss="alert" aria-hidden="true">' +
			'&times;</button>' + message + '</div>');
}

var upload_form = $("#upload_form");
upload_form.submit(function(ev) {
	ev.preventDefault();

	filename = $('#upload_new').val();
	if (filename != '') {
		var parts = filename.split('.');
		var type = parts[parts.length-1].toLowerCase();
		if (type == 'jpg' || type == 'jpeg' ||
			type == 'png' || type == 'png') {
			if ($('#upload_new')[0].files[0].size <= 1 * 1024 * 1024) {
				var form_data = new FormData(this);
				show_info('Uploading, please wait... :)');

				$.ajax({
					type: upload_form.attr('method'),
					url: upload_form.attr('action'),
					data: form_data,
					cache:false,
					contentType: false,
					processData: false,
					success: function(data) {
						if (data['status'] == 'ok') {
							show_info('Your new avatar has been uploaded :)')
							$('#avatar').attr('src',
									'/yagra/api/?key='+data['api']+'&nouse='+Math.random())
						} else if (data['status'] == 'invalid') {
							show_error(data['message']);
						} else if (data['status'] == 'error') {
							window.location.replace(data['redirect']);
						}
					},
					error: function(data) {
						console.log('error');
						console.log(data);
					}
				});
			} else {
					show_error('Your image is too large.. Sorry :(');
			}
		} else {
			show_error('Your ' + type + ' file type is not supported :(');
		}
	} else {
		show_error('Please select a image first :)');
	}
})
