$(document).ready(function() {
    $('#btn_get_rec').click(function() {
        uid_val = $('#ipt-uid').val()
		console.log(uid_val);
        num_val = $('#ipt-num').val()
		console.log(num_val);
        $.ajax({
            //url: 'ad-rec',
            url: 'ad-rec-v2',
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
                var html = ''
                if ('history' in returndata) {
                    var history = returndata['history']
                    hist_html = '<p><font color="red">用户'+ uid_val +'最近一次浏览商品：</font></p>'
                    hist_html += '<p>' + history['ad_title'] + '</p>'
                    hist_html += '<div class="row text-center">'
                    hist_html += '<img src="' + history['ad_img'] + '" class="img-responsive center-block" width="300" height="300">';
                    hist_html += '</div>'
                    hist_html += '<p style="padding-top:5px">' + '详情：' + history['ad_cate'] + '</p>'
                } else {
                    hist_html = '<p><font color="red">用户'+ uid_val +'为系统新用户，使用热门+随机推荐</font></p>'
                }
                    
                $('#show_hist').html(hist_html);

				var ad_res = returndata['ad_res']
				var img_html = '<p style="padding-top:10px"><font color="red">系统为用户'+ uid_val +'推荐如下商品：</font></p>'
				$.each(ad_res, function(i, r) {
					img_html += '<div class="row text-center">'
					img_html += '<p style="padding-top:10px">' + 'No.' + (i+1) + '  ' + r['ad_title'] + ' <font color="red">' + parseFloat(r['score']).toFixed(2) + '分</font></p>' 
					//img_html += '<p class="col-sm-3">' + r['ad_title'] + '</p>' 
					//img_html += '<p class="col-sm-2">' + r['ad_cates'] + '</p>' 
					//img_html += '<p class="col-sm-2">' + r['score'] + '</p>' 
					img_html += '</div>'
					img_html += '<img src="' + r['ad_img'] + '" class="img-responsive center-block" width="300" height="300">';
                    img_html += '<p style="padding-top:5px">' + '详情：' + r['ad_cate'] + '</p>'
					console.log(i, r);
				});
				//$('#show_rec_imgs').append($('<th></th>').text(col));$
				$('#show_rec_imgs').html(img_html);
            },
        });
    });
});
