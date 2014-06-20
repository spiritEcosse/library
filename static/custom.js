function delete_book() {
	select_id = []

	$('input[name*=\'selected\']:checked').each(function(index, value) {
		select_id[index] = $(this).val();
	});

	if (select_id.length != 0) {
		$.ajax({
			type: "POST",
			url: "/delete_book_list",
			data: 'ids=' + select_id,
			success: function(data) {
				if (data.error) {
					alert(data.error);
					return false;
				}

				window.location.reload(data.redirect);
			}
		});
	}
}

function delete_author() {
	select_id = []

	$('input[name*=\'selected\']:checked').each(function(index, value) {
		select_id[index] = $(this).val();
	});

	if (select_id.length != 0) {
		$.ajax({
			type: "POST",
			url: "/delete_author_list",
			data: 'ids=' + select_id,
			success: function(data) {
				if (data.error) {
					alert(data.error);
					return false;
				}

				window.location.reload(data.redirect);
			}
		});
	}
}