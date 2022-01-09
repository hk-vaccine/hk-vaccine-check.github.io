import requests
import json

bnt_centers = {
       36: {
           'center_name_tc': '香港中文大學醫院社區疫苗接種中心',
           'center_name_en': 'Community Vaccination Centre, CUHK Medical Centre'
       },
       42: {
           'center_name_tc': '香港大學駐港怡醫院社區疫苗接種中心',
           'center_name_en': 'Community Vaccination Centre, HKU at Gleneagles Hospital Hong Kong'
       },
       28: {
           'center_name_tc': '西灣河體育館社區疫苗接種中心',
           'center_name_en': 'Community Vaccination Centre, Sai Wan Ho Sports Centre CVC'
       },
       46: {
           'center_name_tc': '曉光街體育館社區疫苗接種中心',
           'center_name_en': 'Community Vaccination Centre, Hiu Kwong Street Sports Centre'
       },
       37: {
           'center_name_tc': '荔枝角公園體育館社區疫苗接種中心',
           'center_name_en': 'Community Vaccination Centre, Lai Chi Kok Park Sports Centre'
       },
       142: {
           'center_name_tc': '(復必泰)林士德體育館社區疫苗接種中心',
           'center_name_en': '(BioNTech) Osman Ramju Sadick Memorial Sports Centre CVC'
       },
       27: {
           'center_name_tc': '元朗體育館社區疫苗接種中心',
           'center_name_en': 'Community Vaccination Centre, Yuen Long Sports Centre'
       }
    }


# a function for calling API to get vaccine availability
def api_call(center_id):
    url = "https://bookingform.covidvaccine.gov.hk/forms/api_center"
    payload='center_id={center_id}&cv_ctc_type=CVC&cv_name=BioNTech%2FFosun'.format(center_id = center_id)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response

# printing available time
def check_and_print_available_time(center_id, api_response):
    available_timeslots = api_response['avalible_timeslots'] # the API response has typo
    have_slot = False
    bnt_centers[center_id]['time_slots'] = {}

    # loop every day
    for time_slot in available_timeslots:
        time_slots_in_a_day = time_slot['timeslots']
        # loop every timeslot within a day
        for time_slot_in_a_day in time_slots_in_a_day:
            if time_slot_in_a_day['value'] > 0:
                date = time_slot_in_a_day['datetime'].split()[0]
                time = time_slot_in_a_day['datetime'].split()[1]

                if date not in bnt_centers[center_id]['time_slots']:
                    bnt_centers[center_id]['time_slots'][date] = [time]
                else:
                    bnt_centers[center_id]['time_slots'][date].append(time)

                have_slot = True

    if not have_slot:
        print(u'\U0000274C {center_tc} | 冇得打!'.format(center_tc=bnt_centers[center_id]['center_name_tc']))
    else:
        print(u'\U00002705 {center_tc} | 有得打!'.format(center_tc=bnt_centers[center_id]['center_name_tc']))
    
out_file = open("bnt_center_availability.json", "w")

# dictionary for exporting to json
# example:
# {
#     36: {
#         'center_name_tc': '香港中文大學醫院社區疫苗接種中心',
#         'center_name_en': 'Community Vaccination Centre, CUHK Medical Centre',
#         'time_slots': {
#             '2022-01-20': ['08:30', '09:00'],
#             '2022-01-27': ['14:30', '18:00']
#         }
#     },
# }

# loop different centers
for bnt_center_key in bnt_centers:
    api_response = api_call(bnt_center_key)
    check_and_print_available_time(bnt_center_key, api_response)

# dump dict to json file
json.dump(bnt_centers, out_file, indent = 6)
out_file.close()
        

