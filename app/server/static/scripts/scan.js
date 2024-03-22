$(document).ready(function(){
    var textarea1 = document.getElementById("sechead");
    var textarea2 = document.getElementById("missing_sec");
    var textarea3 = document.getElementById("listing");
    var textarea4 = document.getElementById("webinfo");
    $("#scanText").click(function(){
        $(".result_value").addClass("common-none")
        textarea1.value= ""
        textarea2.value= ""
        textarea3.value = ""
        textarea4.value = ""
        var url_entered = $('#textInput').val();
        console.log(url_entered)
        $.ajax({
            url: "/url_scan",
            type: "POST",
            data: {value: url_entered},
            success: function(response) {
                var value1 = response['data_value1']
                var value2 = response['data_value2']
                var value3 = response['data_value3']
                var value4 = response['data_value4']
                for (var header in value1)
                 {
                    textarea1.value += `${header}: ${value1[header]}` + "\n"
                }

                for (var item1 of value2)
                    {
                       textarea2.value += item1 + "\n"
                    }
                for (var item2 of value3)
                    {
                       textarea3.value += item2 + "\n"
                    }
                for (var item3 of value4)
                    {
                       textarea4.value += item3 + "\n"
                    }
                $(".result_value").removeClass("common-none")

            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    });
});
