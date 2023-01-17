function redirect_to(url, alert_text) {
    alert(alert_text);
    location.replace(url);
}

function alert_func(alert_text) {
    alert(alert_text);
}

function set_status(status_value) {
    if (status_value == 'publish') {
        document.getElementById('id_status').value = 'publish';
    } else if (status_value == 'draft') {
        document.getElementById('id_status').value = 'draft';
    } else if (status_value == 'archive') {
        document.getElementById('id_status').value = 'archive';
    }
}

function set_description(description_value) {
    document.getElementById('id_description').innerHTML = description_value;
}

function set_description_in_player(description_in_player_value) {
    document.getElementById('id_description_in_player').innerHTML = description_in_player_value;
}

function set_datetime_type(datetime_type_value, day_0, day_1, day_2, day_3, day_4, day_5, day_6) {
    if (datetime_type_value == 'weekly') {
        document.getElementById('id_datetime_type').value = 'weekly';
        if (day_0 == 'True') {
            document.getElementById("id_day_0").checked = true;
        }
        if (day_1 == 'True') {
            document.getElementById("id_day_1").checked = true;
        }
        if (day_2 == 'True') {
            document.getElementById("id_day_2").checked = true;
        }
        if (day_3 == 'True') {
            document.getElementById("id_day_3").checked = true;
        }
        if (day_4 == 'True') {
            document.getElementById("id_day_4").checked = true;
        }
        if (day_5 == 'True') {
            document.getElementById("id_day_5").checked = true;
        }
        if (day_6 == 'True') {
            document.getElementById("id_day_6").checked = true;
        }
    } else if (datetime_type_value == 'occasional') {
        document.getElementById('id_datetime_type').value = 'occasional';
    } else if (datetime_type_value == 'weekly_occasional') {
        document.getElementById('id_datetime_type').value = 'weekly_occasional';
        if (day_0 == 'True') {
            document.getElementById("id_day_0").checked = true;
        }
        if (day_1 == 'True') {
            document.getElementById("id_day_1").checked = true;
        }
        if (day_2 == 'True') {
            document.getElementById("id_day_2").checked = true;
        }
        if (day_3 == 'True') {
            document.getElementById("id_day_3").checked = true;
        }
        if (day_4 == 'True') {
            document.getElementById("id_day_4").checked = true;
        }
        if (day_5 == 'True') {
            document.getElementById("id_day_5").checked = true;
        }
        if (day_6 == 'True') {
            document.getElementById("id_day_6").checked = true;
        }
    }
}

function show_hide_week_day(id) {
    id = parseInt(id)
    conditions_day = [
        document.getElementById('id_day_0').checked,
        document.getElementById('id_day_1').checked,
        document.getElementById('id_day_2').checked,
        document.getElementById('id_day_3').checked,
        document.getElementById('id_day_4').checked,
        document.getElementById('id_day_5').checked,
        document.getElementById('id_day_6').checked,
    ]
    if (conditions_day[id]) {
        document.getElementById('hr_id_end_weekly_table').style.display = "block";
        document.getElementById('div_id_day_' + id).style.display = "block";
    } else {
        document.getElementById('div_id_day_' + id).style.display = "none";
    }
    if (!(conditions_day[0]) && !(conditions_day[1]) && !(conditions_day[2]) && !(conditions_day[3]) && !(conditions_day[4]) && !(conditions_day[5]) && !(conditions_day[6])) {
        document.getElementById('hr_id_end_weekly_table').style.display = "none";
    }
}

function show_hide_datetime_type() {
    let get_datetime_type = document.getElementById("id_datetime_type");
    let datetime_type_selected = get_datetime_type.options[get_datetime_type.selectedIndex].text;
    if (datetime_type_selected == '---------') {
        // Hide weekly
        weekly = document.getElementById("div_id_weekly");
        weekly.style.display = "none";
        // Hide specified_date
        specified_date = document.getElementById("div_id_occasional");
        specified_date.style.display = "none";
        // Hide hr_between_weekly_specified_date
        hr_between_weekly_specified_date = document.getElementById("hr_id_between_weekly_specified_date");
        hr_between_weekly_specified_date.style.display = "none";
    } else if (datetime_type_selected == 'هفتگی') {
        // Show weekly
        weekly = document.getElementById("div_id_weekly");
        weekly.style.display = "block";
        // Hide specified_date
        specified_date = document.getElementById("div_id_occasional");
        specified_date.style.display = "none";
        // Show hr_between_weekly_specified_date
        hr_between_weekly_specified_date = document.getElementById("hr_id_between_weekly_specified_date");
        hr_between_weekly_specified_date.style.display = "block";
    } else if (datetime_type_selected == 'مناسبتی') {
        // Show specified_date
        specified_date = document.getElementById("div_id_occasional");
        specified_date.style.display = "block";
        // Hide weekly
        weekly = document.getElementById("div_id_weekly");
        weekly.style.display = "none";
        // Hide hr_between_weekly_specified_date
        hr_between_weekly_specified_date = document.getElementById("hr_id_between_weekly_specified_date");
        hr_between_weekly_specified_date.style.display = "none";
    } else if (datetime_type_selected == 'هفتگی - مناسبتی') {
        // Show weekly
        weekly = document.getElementById("div_id_weekly");
        weekly.style.display = "block";
        // Show specified_date
        specified_date = document.getElementById("div_id_occasional");
        specified_date.style.display = "block";
        // Hide hr_between_weekly_specified_date
        hr_between_weekly_specified_date = document.getElementById("hr_id_between_weekly_specified_date");
        hr_between_weekly_specified_date.style.display = "none";
    }
}

function use_flatpickr() {
    config = {
        dateFormat: "Y-m-d",
    }
    flatpickr("input[type=date]", config);
    config = {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:S",
    }
    flatpickr("input[type=time]", config);
}

function set_stream_type(stream_type_value, audio_platform_type_value) {
    if (stream_type_value == 'audio') {
        document.getElementById('id_stream_type').value = 'audio';

        // audio_platform_type
        if (audio_platform_type_value == 'shoutcast') {
            document.getElementById('id_audio_platform_type').value = 'shoutcast';
        } else if (audio_platform_type_value == 'wowza') {
            document.getElementById('id_audio_platform_type').value = 'wowza';
        }
    } else if (stream_type_value == 'video') {
        document.getElementById('id_stream_type').value = 'video';

        // video_platform_type
        document.getElementById('id_video_platform_type').value = 'wowza';
    } else if (stream_type_value == 'audio_video') {
        document.getElementById('id_stream_type').value = 'audio_video';

        // audio_platform_type
        if (audio_platform_type_value == 'shoutcast') {
            document.getElementById('id_audio_platform_type').value = 'shoutcast';
        } else if (audio_platform_type_value == 'wowza') {
            document.getElementById('id_audio_platform_type').value = 'wowza';
        }

        // video_platform_type
        document.getElementById('id_video_platform_type').value = 'wowza';
    }
}

function show_hide_stream_type() {
    let get_stream_type = document.getElementById("id_stream_type");
    let stream_type_selected = get_stream_type.options[get_stream_type.selectedIndex].text;
    if (stream_type_selected == '---------') {
        // Hide audio
        audio = document.getElementById("div_id_audio");
        audio.style.display = "none";
        // Hide video
        video = document.getElementById("div_id_video");
        video.style.display = "none";
    } else if (stream_type_selected == 'صوتی') {
        // Show audio
        audio = document.getElementById("div_id_audio");
        audio.style.display = "block";
        // Hide video
        video = document.getElementById("div_id_video");
        video.style.display = "none";
    } else if (stream_type_selected == 'تصویری') {
        // Show video
        video = document.getElementById("div_id_video");
        video.style.display = "block";
        // Hide audio
        audio = document.getElementById("div_id_audio");
        audio.style.display = "none";
    } else if (stream_type_selected == 'صوتی و تصویری') {
        // Show audio
        audio = document.getElementById("div_id_audio");
        audio.style.display = "block";
        // Show video
        video = document.getElementById("div_id_video");
        video.style.display = "block";
    }
}

function add_occasional_elements(element, value = "") {
    let div = document.createElement("div");
    let input = document.createElement("input");
    let span = document.createElement("span");
    let i = document.createElement("i");
    let name_occasional;
    let remove_occasional_input;
    let input_placeholder;
    if (element == "specified_date") {
        name_occasional = element + count_specified_date;
        remove_occasional_input = count_specified_date;
        input_placeholder = count_specified_date + 1;
        input.setAttribute("type", "date");
        input.setAttribute("placeholder", "تاریخ " + input_placeholder);
    } else if (element == "specified_start_time") {
        name_occasional = element + count_specified_start_time;
        remove_occasional_input = count_specified_start_time;
        input_placeholder = count_specified_start_time + 1;
        input.setAttribute("type", "time");
        input.setAttribute("placeholder", "ساعت شروع " + input_placeholder);
    } else {
        name_occasional = element + count_specified_end_time;
        remove_occasional_input = count_specified_end_time;
        input_placeholder = count_specified_end_time + 1;
        input.setAttribute("type", "time");
        input.setAttribute("placeholder", "ساعت پایان " + input_placeholder);
    }
    div.setAttribute("id", "div_id_" + name_occasional);
    div.setAttribute("class", "input-group");
    div.setAttribute("style", "margin-top: 5px");
    document.getElementById("div_id_" + element + "_add").appendChild(div);
    input.setAttribute("id", name_occasional);
    input.setAttribute("name", name_occasional);
    input.setAttribute("class", "form-control");
    input.setAttribute("value", value);
    document.getElementById("div_id_" + name_occasional).appendChild(input);
    div = document.createElement("div");
    div.setAttribute("id", "div_div_id_" + name_occasional);
    div.setAttribute("class", "input-group-append");
    document.getElementById("div_id_" + name_occasional).appendChild(div);
    span.setAttribute("class", "input-group-text btn btn-danger btn-sm");
    span.setAttribute("onclick", "remove_occasional(" + JSON.stringify(remove_occasional_input) + ")");
    i.setAttribute("class", "fas fa-times");
    i.setAttribute("aria-hidden", "true");
    span.appendChild(i);
    document.getElementById("div_div_id_" + name_occasional).appendChild(span);
    let list;
    if (element == "specified_date") {
        count_specified_date++;
        list = document.getElementById("id_list_specified_date").value;
        document.getElementById("id_list_specified_date").value = list + "," + name_occasional;
    } else if (element == "specified_start_time") {
        count_specified_start_time++;
        list = document.getElementById("id_list_specified_start_time").value;
        document.getElementById("id_list_specified_start_time").value = list + "," + name_occasional;
    } else {
        count_specified_end_time++;
        list = document.getElementById("id_list_specified_end_time").value;
        document.getElementById("id_list_specified_end_time").value = list + "," + name_occasional;
    }
    use_flatpickr();
}

function add_occasional() {
    add_occasional_elements("specified_date");
    add_occasional_elements("specified_start_time");
    add_occasional_elements("specified_end_time");
}

function remove_occasional(id) {
    let my_element = document.getElementById("div_id_specified_date" + id);
    my_element.remove();
    let specified_date_removed_old = document.getElementById("id_list_specified_date_removed").value;
    if (specified_date_removed_old == "") {
        document.getElementById("id_list_specified_date_removed").value = "specified_date" + id;
    } else {
        document.getElementById("id_list_specified_date_removed").value = specified_date_removed_old + ",specified_date" + id;
    }

    my_element = document.getElementById("div_id_specified_start_time" + id);
    my_element.remove();
    let specified_start_time_removed_old = document.getElementById("id_list_specified_start_time_removed").value;
    if (specified_start_time_removed_old == "") {
        document.getElementById("id_list_specified_start_time_removed").value = "specified_start_time" + id;
    } else {
        document.getElementById("id_list_specified_start_time_removed").value = specified_start_time_removed_old + ",specified_start_time" + id;
    }

    my_element = document.getElementById("div_id_specified_end_time" + id);
    my_element.remove();
    let specified_end_time_removed_old = document.getElementById("id_list_specified_end_time_removed").value;
    if (specified_end_time_removed_old == "") {
        document.getElementById("id_list_specified_end_time_removed").value = "specified_end_time" + id;
    } else {
        document.getElementById("id_list_specified_end_time_removed").value = specified_end_time_removed_old + ",specified_end_time" + id;
    }
}