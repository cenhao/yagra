var sign_in_form = $("#signin_form");
sign_in_form.submit(function(event) {
	user = $("#username");
	pwd = $("#password");
	if (user[0].willValidate && pwd[0].willValidate) {
		pwd.val(md5(pwd.val()));
		$.ajax({
			type: sign_in_form.attr('method'),
			url: sign_in_form.attr('action'),
			data: sign_in_form.serialize(),
			success: function(data) {
				if (data['status'] == 'ok') {
					window.location.replace(data['redirect']);
				} else if (data['status'] == 'alert') {
					vali = $("#validate");
					if (vali.attr('class') != 'has-error') {
						vali.attr('class', 'has-error');
						$('<label/>', {
							'class' : 'control-label',
							'for' : 'username',
							'id' : 'message',
							text : data['message']
						}).appendTo("#label_location");
					}
					pwd.val('');
				} else if (data['status'] == 'error') {
					window.location.replace(data['redirect']);
				}

				event.preventDefault();
			},
			error: function(data) {
				window.location.replace('http://cenhao.chinacloudapp.cn/error.html');
				event.preventDefault();
			}
		});

		event.preventDefault();
	} else {
		event.preventDefault();
	}
})
