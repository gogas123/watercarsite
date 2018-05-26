$(function(){
	var flag = false;
	$("#duplcheck").on("click",function(){
		$.ajax({
			url: "/duplcheck",
    	type: 'POST',
    	data: {
						"csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val(),
        		'username': $("#username").val()
    	},
			dataType: 'json',
    	success: function (data) {
        	// TODO: do something.
					if (data.is_taken) {
            alert("이미 존재하는 ID입니다.");
          }
					else{
						alert("사용하실 수 있는 ID입니다.");
						flag = true;
					}
    	},
    	error: function (request, status, error) {
					alert("code: " + request.status + "\n" + "error:" + error);
    	}
		});
		return false;
	});
	$("#username").on("focusout",function(){
		if(flag){
			flag=false;
		}
	});
	$('#signup').on('submit',function(e){
		if(!flag){
			e.preventDefault();
			alert("ID 중복확인 해주세요.");
		}
	});
});