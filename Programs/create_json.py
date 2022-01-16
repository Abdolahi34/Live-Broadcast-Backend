import json
from . import models


programs_obj = models.Program.objects.all()
programs_dict = {}

for program in programs_obj:
    programs_dict[program.id-1] = {}
    programs_dict[program.id-1]['title'] = program.title
    programs_dict[program.id-1]['title_slug'] = program.slug
    programs_dict[program.id-1]['stream_slug'] = program.stream_slug
    programs_dict[program.id-1]['duration'] = program.duration
    programs_dict[program.id-1]['date'] = program.date
    programs_dict[program.id-1]['time_start'] = program.time_start
    programs_dict[program.id-1]['time_end'] = program.time_end
    programs_dict[program.id-1]['link'] = program.link
    programs_dict[program.id-1]['video_link'] = program.video_link
    programs_dict[program.id-1]['voice_link'] = program.voice_link
    programs_dict[program.id-1]['is_active'] = program.is_active
    programs_dict[program.id-1]['is_voice'] = program.is_voice
    programs_dict[program.id-1]['logo_path'] = program.logo_path


json_file = open('programs.json', 'w+')

json.dump(programs_dict, json_file)

