function toggle(source) {
    checkboxes = document.getElementsByName('in');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
    }
    }


function reload_experiment(source) {
    document.getElementById("myprogressBarcluster").innerHTML = "Loading..."
    var transcripts = [];
    for (var option of document.getElementById('first_select').options)
    {
        if (option.selected) {
            transcripts.push(option.value);
        }
    }
    var zero = 0;
    var one = 0;
    var two = 0;
    var three = 0;
    var four = 0;
    var five = 0;
    var six = 0;
    var seven = 0;
    var eight = 0;
    var nine = 0;
    var ten = 0;
    var eleven = 0;
    var twelve = 0;
    var thirteen = 0;
    var fourteen = 0;
    var fifteen = 0;
    var sixteen = 0;
    var seventeen = 0;
    if ($('#inlineCheckbox0').is(":checked"))
    {
        zero += 1;
    }
    if ($('#inlineCheckbox1').is(":checked"))
    {
        one += 1;
    }
    if ($('#inlineCheckbox2').is(":checked"))
    {
        two += 1;
    }
    if ($('#inlineCheckbox3').is(":checked"))
    {
        three += 1;
    }
    if ($('#inlineCheckbox4').is(":checked"))
    {
        four += 1;
    }
    if ($('#inlineCheckbox5').is(":checked"))
    {
        five += 1;
    }
    if ($('#inlineCheckbox6').is(":checked"))
    {
        six += 1;
    }
    if ($('#inlineCheckbox7').is(":checked"))
    {
        seven += 1;
    }
    if ($('#inlineCheckbox8').is(":checked"))
    {
        eight += 1;
    }
    if ($('#inlineCheckbox9').is(":checked"))
    {
        nine += 1;
    }
    if ($('#inlineCheckbox10').is(":checked"))
    {
        ten += 1;
    }
    if ($('#inlineCheckbox11').is(":checked"))
    {
        eleven += 1;
    }
    if ($('#inlineCheckbox12').is(":checked"))
    {
        twelve += 1;
    }
    if ($('#inlineCheckbox13').is(":checked"))
    {
        thirteen += 1;
    }
    if ($('#inlineCheckbox14').is(":checked"))
    {
        fourteen += 1;
    }
    if ($('#inlineCheckbox15').is(":checked"))
    {
        fifteen += 1;
    }
    if ($('#inlineCheckbox16').is(":checked"))
    {
        sixteen += 1;
    }
    if ($('#inlineCheckbox17').is(":checked"))
    {
        seventeen += 1;
    }

    var experiment = source.options[source.selectedIndex].value;

    var server_data = [
        {"num0": zero, "num1": one, "num2": two, "num3": three, "num4": four, "num5": five, "num6": six, "num7": seven, "num8": eight, "num9": nine, "num10": ten, "num11": eleven, "num12": twelve, "num13": thirteen, "num14": fourteen, "num15": fifteen, "num16": sixteen, "num17": seventeen, "p_experiment": "current", "p_experiment2": "current", "pseudotime": "none", "Transcripts": transcripts, "experiment":experiment, "experiment2":"current"}
        ];
    $.ajax({
        url: "/index",
        data: JSON.stringify(server_data),
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            $("#myimg1").attr('src', response.saver1);
            $("#myimg_transcript1").attr('src', response.saver1);
            $("#myimg2").attr('src', response.saver2);
            $("#myimg_transcript2").attr('src', response.saver2);
            $("#legend").attr('src', response.saveleg);
            $("#membershipt option").eq(source.selectedIndex).prop('selected', true);
            document.getElementById("myprogressBarcluster").innerHTML = ""
        },
        error: function(xhr) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.Message);
        }
        });
    }

function reload_experiment2(source) {
    document.getElementById("myprogressBarcluster").innerHTML = "Loading..."
    var transcripts = [];
    for (var option of document.getElementById('first_select').options)
    {
        if (option.selected) {
            transcripts.push(option.value);
        }
    }
    var zero = 0;
    var one = 0;
    var two = 0;
    var three = 0;
    var four = 0;
    var five = 0;
    var six = 0;
    var seven = 0;
    var eight = 0;
    var nine = 0;
    var ten = 0;
    var eleven = 0;
    var twelve = 0;
    var thirteen = 0;
    var fourteen = 0;
    var fifteen = 0;
    var sixteen = 0;
    var seventeen = 0;
    if ($('#inlineCheckbox0').is(":checked"))
    {
        zero += 1;
    }
    if ($('#inlineCheckbox1').is(":checked"))
    {
        one += 1;
    }
    if ($('#inlineCheckbox2').is(":checked"))
    {
        two += 1;
    }
    if ($('#inlineCheckbox3').is(":checked"))
    {
        three += 1;
    }
    if ($('#inlineCheckbox4').is(":checked"))
    {
        four += 1;
    }
    if ($('#inlineCheckbox5').is(":checked"))
    {
        five += 1;
    }
    if ($('#inlineCheckbox6').is(":checked"))
    {
        six += 1;
    }
    if ($('#inlineCheckbox7').is(":checked"))
    {
        seven += 1;
    }
    if ($('#inlineCheckbox8').is(":checked"))
    {
        eight += 1;
    }
    if ($('#inlineCheckbox9').is(":checked"))
    {
        nine += 1;
    }
    if ($('#inlineCheckbox10').is(":checked"))
    {
        ten += 1;
    }
    if ($('#inlineCheckbox11').is(":checked"))
    {
        eleven += 1;
    }
    if ($('#inlineCheckbox12').is(":checked"))
    {
        twelve += 1;
    }
    if ($('#inlineCheckbox13').is(":checked"))
    {
        thirteen += 1;
    }
    if ($('#inlineCheckbox14').is(":checked"))
    {
        fourteen += 1;
    }
    if ($('#inlineCheckbox15').is(":checked"))
    {
        fifteen += 1;
    }
    if ($('#inlineCheckbox16').is(":checked"))
    {
        sixteen += 1;
    }
    if ($('#inlineCheckbox17').is(":checked"))
    {
        seventeen += 1;
    }

    var experiment = source.options[source.selectedIndex].value;

    var server_data = [
        {"num0": zero, "num1": one, "num2": two, "num3": three, "num4": four, "num5": five, "num6": six, "num7": seven, "num8": eight, "num9": nine, "num10": ten, "num11": eleven, "num12": twelve, "num13": thirteen, "num14": fourteen, "num15": fifteen, "num16": sixteen, "num17": seventeen, "p_experiment": "current", "p_experiment2": "current", "pseudotime": "none", "Transcripts": transcripts, "experiment":"current", "experiment2": experiment}
        ];
    $.ajax({
        url: "/index",
        data: JSON.stringify(server_data),
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            $("#myimg1").attr('src', response.saver1);
            $("#myimg_transcript1").attr('src', response.saver1);
            $("#myimg2").attr('src', response.saver2);
            $("#myimg_transcript2").attr('src', response.saver2);
            $("#legend").attr('src', response.saveleg);
            $("#membership_secondt option").eq(source.selectedIndex).prop('selected', true);
            document.getElementById("myprogressBarcluster").innerHTML = ""
        },
        error: function(xhr) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.Message);
        }
        });
    }