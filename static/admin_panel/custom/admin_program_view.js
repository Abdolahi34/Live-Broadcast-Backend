function set_datetime_type(datetime_type_value, day_0, day_1, day_2, day_3, day_4, day_5, day_6) {
    function set_week_days(day_0, day_1, day_2, day_3, day_4, day_5, day_6) {
        if (day_0 === 'True') {
            document.getElementById("day_0").checked = true;
            document.getElementById("div_id_day_0").style.display = "block";
        }
        if (day_1 === 'True') {
            document.getElementById("day_1").checked = true;
            document.getElementById("div_id_day_1").style.display = "block";
        }
        if (day_2 === 'True') {
            document.getElementById("day_2").checked = true;
            document.getElementById("div_id_day_2").style.display = "block";
        }
        if (day_3 === 'True') {
            document.getElementById("day_3").checked = true;
            document.getElementById("div_id_day_3").style.display = "block";
        }
        if (day_4 === 'True') {
            document.getElementById("day_4").checked = true;
            document.getElementById("div_id_day_4").style.display = "block";
        }
        if (day_5 === 'True') {
            document.getElementById("day_5").checked = true;
            document.getElementById("div_id_day_5").style.display = "block";
        }
        if (day_6 === 'True') {
            document.getElementById("day_6").checked = true;
            document.getElementById("div_id_day_6").style.display = "block";
        }
    }

    if (datetime_type_value === 'weekly') {
        // Show weekly
        weekly = document.getElementById("div_weekly");
        weekly.style.display = "block";
        set_week_days(day_0, day_1, day_2, day_3, day_4, day_5, day_6);
    } else if (datetime_type_value === 'occasional') {
        // Show occasional
        occasional = document.getElementById("div_occasional");
        occasional.style.display = "block";
    } else if (datetime_type_value === 'weekly_occasional') {
        // Show weekly
        weekly = document.getElementById("div_weekly");
        weekly.style.display = "block";
        set_week_days(day_0, day_1, day_2, day_3, day_4, day_5, day_6);
        // Show occasional
        occasional = document.getElementById("div_occasional");
        occasional.style.display = "block";
    }
}

function set_stream_type() {
    if (stream_type_value === 'audio') {
        // Show audio
        audio = document.getElementById("div_audio");
        audio.style.display = "block";
    } else if (stream_type_value === 'video') {
        // Show video
        video = document.getElementById("div_video");
        video.style.display = "block";
    } else {
        // Show audio
        audio = document.getElementById("div_audio");
        audio.style.display = "block";
        // Show video
        video = document.getElementById("div_video");
        video.style.display = "block";
    }
}