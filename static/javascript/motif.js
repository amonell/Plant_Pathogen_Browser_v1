function display_motif() {
    document.getElementById("myprogressBarmotif").innerHTML = "        Loading..."
    var transcripts = [];
    for (var option of document.getElementById('first_select3').options)
    {
        if (option.selected) {
            transcripts.push(option.value);
        }
    }
    var server_data = [
        {"experiment": "0 hr Avrrpt", "gene": transcripts, "holder": "button", "secondholder": "motif"}
    ];
    $.ajax({
    url: "/index",
    data: JSON.stringify(server_data),
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(response) {
        $("#myimg_motif1").attr('src', response.saver1);
        $("#myimg_motif2").attr('src', response.saver2);
        document.getElementById("myprogressBarmotif").innerHTML = ""
    },
    error: function(xhr) {
        var err = eval("(" + xhr.responseText + ")");
        alert(err.Message);
        // $.ajax({
        //     url: "{{ url_for ('show_index') }}",
        //     type: "GET",
        //     success: function(response) {
        //         $("#myimg").attr('src', 'static/images/plot2.png');
        //     },
        //     error: function(xhr) {
        //         $("#myimg").attr('src', 'static/images/plot2.png');
        //     }
        //     });
            //location.reload(true)
    }
    
    });

};

function reload_experiment_motif(source) {
    document.getElementById("myprogressBarmotif").innerHTML = "Loading..."
    var experiment = source.options[source.selectedIndex].value;
    var transcripts = [];
    for (var option of document.getElementById('first_select3').options)
    {
        if (option.selected) {
            transcripts.push(option.value);
        }
    }
    var server_data = [
        {"experiment": experiment, "gene": transcripts, "holder": "motif", "secondholder": "motif"}
    ];
    $.ajax({
    url: "/index",
    data: JSON.stringify(server_data),
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(response) {
        $("#myimg_motif1").attr('src', response.saver1);
        $("#myimg_motif2").attr('src', response.saver2);
        document.getElementById("myprogressBarmotif").innerHTML = ""
    },
    error: function(xhr) {
        var err = eval("(" + xhr.responseText + ")");
        alert(err.Message); 
    }
    });

};