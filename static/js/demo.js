$(document).ready(function() {
    $('#btn_get_rec').click(function() {
        uid_val = $('#ipt-uid').val()
		console.log(uid_val);
        num_val = $('#ipt-num').val()
		console.log(num_val);
        $.ajax({
            url: 'ad-rec',
            type: 'GET',
            data: {
                uid : uid_val,
                num : num_val
            },
            datatype: 'json',
            contentType: 'application/json; charset=UTF-8',
            success: function (returndata) {
                console.log(returndata);
				$('#ipt-uid').val('')
				$('#ipt-num').val('')
				var ad_res = returndata['ad_res']
				var img_html = '<p><font color="red">为用户'+ uid_val +'推荐结果如下：</font></p>'
				$.each(ad_res, function(i, r) {
					img_html += '<div class="row text-center">'
					img_html += '<p style="padding-top:10px">' + 'No.' + (i+1) + '  ' + r['ad_title'] + ' <font color="red">' + parseFloat(r['score']).toFixed(2) + '分</font></p>' 
					//img_html += '<p class="col-sm-3">' + r['ad_title'] + '</p>' 
					//img_html += '<p class="col-sm-2">' + r['ad_cates'] + '</p>' 
					//img_html += '<p class="col-sm-2">' + r['score'] + '</p>' 
					img_html += '</div>'
					img_html += '<img src="' + r['ad_img'] + '" class="img-responsive center-block" alt="Responsive image">';
					console.log(i, r);
				});
				//$('#show_rec_imgs').append($('<th></th>').text(col));$
				$('#show_rec_imgs').html(img_html);
            },
        });
    });
});
