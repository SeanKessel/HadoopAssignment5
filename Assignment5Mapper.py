#!/usr/bin/python
import sys

event_field_list = ['timestamp', 'event_action', 'event_target', 'vin']
vin_field_list = ['condition', 'year', 'make', 'model', 'price', 'mileage']


def read_session(file):
    for line in file:
        # split the line into components: user_id:sessions_type, event_list, in dictionary
        yield line.strip().split('\t')


def main():
    master_dict_list = []

    for line in sys.stdin:
        has_tab = False
        for char in line[:27]:
            if char == "\t":
                has_tab = True
                break
        if not has_tab:
            # If the line does not contain a tab within the first 27 characters, then it is
            # from the impressions dataset
            # otherwise it is from the sessions dataset, and is handled in the "else" statement

            line_array = line.strip().split(",")
            vin = line_array[0]
            V_or_S = line_array[1]

            count = line_array[2]
            if V_or_S == "SRP":
                srp = count
                vdp = 0
            else:
                srp = 0
                vdp = count
            vin_dict = {
                "vin": vin,
                "srp": int(srp),
                "vdp": int(vdp),
                "session_count": 0,
                "click_event_count": 0,
                "contact_form": 0
            }
            master_dict_list.append(vin_dict)
        else:
            '''
            For user sessions, for each VIN the session references, output:
            the session count (1)
            the click event count for that VIN
            whether or not the user performed an event with event_target = "contact form" (0 or 1) for the VIN.
            '''
            line_array = line.strip().split("\t")

            event_list = eval(line_array[1])
            vin_dict = eval(line_array[2])
            for key in vin_dict:
                vin = key
                click_event_count = 0
                contact_form = 0
                for event in event_list:
                    if event["vin"] == vin:
                        if event['event_action'] == 'click':
                            click_event_count = click_event_count + 1
                    if contact_form < 1:
                        if event["event_target"] == "contact form":
                            contact_form = 1
                vin_dict = {
                    "vin": vin,
                    "srp": 0,
                    "vdp": 0,
                    "session_count": 1,
                    "click_event_count": click_event_count,
                    "contact_form": contact_form
                }
                master_dict_list.append(vin_dict)

    master_map_list = []

    for dicti in master_dict_list:
        stri = "{}\t[{},{},{},{},{}]".format(dicti["vin"], dicti["session_count"], dicti["srp"], dicti["vdp"],dicti["click_event_count"], dicti["contact_form"])
        master_map_list.append(stri)


    for i in master_map_list:
        print i


if __name__ == "__main__":
    main()

