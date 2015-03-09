class instance_detail():
    def __init__(self):
        self.empty_hosts = 0
        self.full_hosts = 0
        self.min_free_slots_number_per_host = -1
        self.hosts_with_min_free_slots_number = 0

def make_stats(file_input_path, file_output_path):
    instance_count_dict = {}
    # [number zeros, number ones]
    instance_count_dict['M1'] = instance_detail()
    instance_count_dict['M2'] = instance_detail()
    instance_count_dict['M3'] = instance_detail()

    min_number_free_slots = -1
    number_hosts_with_min_number_free_slots = 0
    with open(file_input_path, 'r') as fr:
        for host_line in fr:
            host_array = host_line.strip().split(',')
            virtual_host_id = host_array[0]
            instance_type = host_array[1]
            slot_number = int(host_array[2])
            number_occupied_slots = sum(map(int, host_array[3:]))
            if number_occupied_slots == 0:
                instance_count_dict[instance_type].empty_hosts += 1
            if number_occupied_slots == slot_number:
                instance_count_dict[instance_type].full_hosts += 1
            instance_count_dict[instance_type].occupied_slots = number_occupied_slots
            if instance_count_dict[instance_type].min_free_slots_number_per_host == -1 or \
                instance_count_dict[instance_type].min_free_slots_number_per_host < slot_number - number_occupied_slots:
                instance_count_dict[instance_type].min_free_slots_number_per_host = slot_number - number_occupied_slots
                instance_count_dict[instance_type].hosts_with_min_free_slots_number = 0
            elif instance_count_dict[instance_type].min_free_slots_number_per_host == slot_number - number_occupied_slots:
                instance_count_dict[instance_type].hosts_with_min_free_slots_number += 1

            print number_occupied_slots.__str__()
        fr.close()

    with open(file_output_path, 'w') as fa:
        """
        EMPTY: M1=<count>; M2=<count>; M3=<count>;
        FULL: M1=<count>; M2=<count>; M3=<count>;
        MOST FILLED: M1=<count>,<empty slots>; M2=<count>,<empty slots>; M3=<count>,<empty slots>;
        """
        string_empty = "EMPTY:M1=" + instance_count_dict['M1'].empty_hosts.__str__() + ";M2=" + instance_count_dict['M2'].empty_hosts.__str__() + ";M3=" + \
            instance_count_dict['M3'].empty_hosts.__str__() + ';\n'

        string_full = "FULL:M1=" + instance_count_dict['M1'].full_hosts.__str__() + ";M2=" + instance_count_dict['M2'].full_hosts.__str__() + ";M3=" + \
            instance_count_dict['M3'].full_hosts.__str__() + ';\n'

        string_most_filled = "MOST FILLED: M1=" + instance_count_dict['M1'].hosts_with_min_free_slots_number.__str__() + "," + instance_count_dict['M1'].min_free_slots_number_per_host.__str__() + ";" + \
             "M2=" + instance_count_dict['M2'].hosts_with_min_free_slots_number.__str__() + "," + instance_count_dict['M2'].min_free_slots_number_per_host.__str__() + ";" + \
             "M3=" + instance_count_dict['M3'].hosts_with_min_free_slots_number.__str__() + "," + instance_count_dict['M3'].min_free_slots_number_per_host.__str__() + ';\n'
        fa.writelines([string_empty, string_full, string_most_filled])
        fa.close()

if __name__ == '__main__':
    make_stats('./FleetState.txt', './Statistics.txt')