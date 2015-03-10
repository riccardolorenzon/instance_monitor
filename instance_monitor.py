# todo unittests

#todo use namedvalue instead

from collections import namedtuple
import os

class instance_detail():
    def __init__(self, type_name):
        self.type_name = type_name
        self.empty_hosts = 0
        self.full_hosts = 0
        self.min_free_slots_number_per_host = -1
        self.hosts_with_min_free_slots_number = 0

def process_record(number_occupied_slots, slot_number, instance_type_count_dict ):
    if number_occupied_slots == 0:
        instance_type_count_dict.empty_hosts += 1
    if number_occupied_slots == slot_number:
        instance_type_count_dict.full_hosts += 1
    instance_type_count_dict.occupied_slots = number_occupied_slots
    if instance_type_count_dict.min_free_slots_number_per_host == -1 or \
        instance_type_count_dict.min_free_slots_number_per_host < slot_number - number_occupied_slots:
        instance_type_count_dict.min_free_slots_number_per_host, instance_type_count_dict.hosts_with_min_free_slots_number = slot_number - number_occupied_slots, 1
    elif instance_type_count_dict.min_free_slots_number_per_host == slot_number - number_occupied_slots:
        instance_type_count_dict.hosts_with_min_free_slots_number += 1

def analyze_records(fr, write_func):
    instance_count_dict = {}

    instance_count_dict['M1'] = instance_detail('M1')
    instance_count_dict['M2'] = instance_detail('M2')
    instance_count_dict['M3'] = instance_detail('M3')

    for host_line in fr:
        host_array = host_line.strip().split(',')
        # check array length
        if len(host_array) < 4 and len(host_array) > 0:
            raise ValueError("too few values for host ID: {0} ".format(host_array[0]))
        elif len(host_array) < 0:
            raise ValueError("one record corrupted, check FleetState.txt")
        instance_type, slot_number= host_array[1], int(host_array[2])
        try:
            number_occupied_slots = host_array[3:].count('1')
        except ValueError:
            raise ValueError("check values for host ID: {0} ".format(host_array[0]))
        process_record(number_occupied_slots, slot_number, instance_count_dict[instance_type] )

    string_empty = "EMPTY: M1={0}; M2={1}; M3={2};\n".format(
        instance_count_dict['M1'].empty_hosts,
        instance_count_dict['M2'].empty_hosts,
        instance_count_dict['M3'].empty_hosts)

    string_full = "FULL: M1={0}; M2={1}; M3={2};\n".format(
        instance_count_dict['M1'].full_hosts,
        instance_count_dict['M2'].full_hosts,
        instance_count_dict['M3'].full_hosts
    )

    string_most_filled = "MOST FILLED: M1={0},{1}; M2={2},{3}; M3={4},{5};\n".format(
        instance_count_dict['M1'].hosts_with_min_free_slots_number,
        instance_count_dict['M1'].min_free_slots_number_per_host,
        instance_count_dict['M2'].hosts_with_min_free_slots_number,
        instance_count_dict['M2'].min_free_slots_number_per_host,
        instance_count_dict['M3'].hosts_with_min_free_slots_number,
        instance_count_dict['M3'].min_free_slots_number_per_host
    )
    write_func([string_empty, string_full, string_most_filled])

    print 'completed!'

def make_stats(file_input_path, file_output_path):
    if not os.path.exists("./{0}".format(file_input_path)):
        raise IOError("input file {0} missing".format(file_input_path))
    if not os.path.exists("./{0}".format(file_output_path)):
        raise IOError("output file {0} missing".format(file_output_path))

    with open(file_input_path, 'r') as fr:
        with open(file_output_path, 'w') as fa:
            analyze_records(fr, lambda x : fa.writelines(x))
            fa.close()
        fr.close()
    pass

if __name__ == '__main__':
    make_stats('./FleetState.txt', './Statistics.txt')
