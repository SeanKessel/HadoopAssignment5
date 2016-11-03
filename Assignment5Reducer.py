#!/usr/bin/python
import sys

def the_separator():
    impressions_list = []
    sessions_list = []
    for entry in sys.stdin:
        entry_split = entry.strip().split("\t")
        vin = entry_split[0]
        entry_list = eval(entry_split[1])

        if entry_list[0] == 1:
            sessions_list.append(entry)
        else:
            impressions_list.append(entry)
    return [sessions_list, impressions_list]


def master_dictionary_maker():
    sessions_list, impressions_list = the_separator()

    vin_master_dict = {}
    current_session_vin = None
    list_of_lists = []
    for session_number in range(len(sessions_list)):
        session_a_list = sessions_list[session_number].strip().split("\t")
        if current_session_vin != session_a_list[0]:
            vin_master_dict[current_session_vin] = list_of_lists
            # enter here the "commit" step
            current_session_vin = session_a_list[0]
            list_of_lists = []
        list_of_lists.append(eval(session_a_list[1]))

        for impression_number in range(len(impressions_list)):
            impression_a_list = impressions_list[impression_number].strip().split("\t")
            if impression_a_list[0] == current_session_vin:
                list_of_lists.append(eval(impression_a_list[1]))
            elif impression_a_list[0] > current_session_vin:
                break
    return vin_master_dict


def main():
    dictionary = master_dictionary_maker()

    final_dictionary = {}

    for key in dictionary:
        list_of_lists = dictionary[key]
        current_list = [0, 0, 0, 0, 0]
        for sub_list in list_of_lists:
            for position in range(len(sub_list)):
                current_list[position] = current_list[position] + sub_list[position]
        final_dictionary[key] = current_list
    for key in final_dictionary:
        print "{}\t{}".format(key,final_dictionary[key])


if __name__ == "__main__":
    main()


