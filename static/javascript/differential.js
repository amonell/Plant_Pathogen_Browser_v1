
function display_differential() {
    var server_data = [
        {"first_cluster": document.getElementById("first_dropdown").value, "second_cluster": document.getElementById("second_dropdown").value}
    ];
    document.getElementById("dynamic_label").innerHTML = "Cluster " + document.getElementById("first_dropdown").value + " (Blue) vs. Cluster "+document.getElementById("second_dropdown").value+" (Orange)"
    document.getElementById("myprogressBar").innerHTML = "Loading..."
    $.ajax({
    url: "/index",
    data: JSON.stringify(server_data),
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(response) {
        $("#df").attr('src', response.saver1);
        document.getElementById("myprogressBar").innerHTML = ""
    },
    error: function(xhr) {
        var err = eval("(" + xhr.responseText + ")");
        alert(err.Message);
    }
    }); 
};
