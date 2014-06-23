var sign_up_form = $("#signup_form");
sign_up_form.submit(function(event) {
	user = $("#username");
	pwd = $("#password");
	repwd = $("#repassword");

	if (user[0].willValidate && pwd[0].willValidate && repwd[0].willValidate) {
		if (repwd.val() != pwd.val()) {
			vali = $("#validate_2");
			if (vali.attr('class') != 'has-error') {
				vali.attr('class', 'has-error');
				$('<label/>', {
					'class' : 'control-label',
					'for' : 'username',
					'id' : 'message',
					text : 'Two password must be the same'
				}).appendTo("#label_location_2");
			}
		} else {
			repwd[0].setCustomValidity('');
			pwd.val(md5(pwd.val()));
			repwd.val(pwd.val());
			$.ajax({
				type: sign_up_form.attr('method'),
				url: sign_up_form.attr('action'),
				data: sign_up_form.serialize(),
				success: function(data) {
					if (data['status'] == 'ok') {
						window.location.replace(data['redirect']);
					} else if (data['status'] == 'alert') {
						vali = $("#validate_" + data['index']);
						alert(data['message']);
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
						repwd.val('');
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
		}

		event.preventDefault();
	} else {
		event.preventDefault();
	}
})
