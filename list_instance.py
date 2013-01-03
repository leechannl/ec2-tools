#! /usr/bin/env python

from operator import itemgetter

from boto.ec2.connection import EC2Connection
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


conn = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

reservations = conn.get_all_instances()

# get the instance list
instances = [res.instances[0] for res in reservations]

# get the instance detail list
dict_keys = ['id', 'name', 'group', 'ip',
            'private_ip', 'flavor', 'image', 'ssh_key' 'status']

list_info = [[x.id, x.tags['Name'], x.groups[0].name,
                                   x.ip_address,
                                   x.private_ip_address,
                                   x.instance_type,
                                   x.image_id,
                                   x.key_name,
                                   x.state] for x in instances]

dict_info = [dict(zip(dict_keys, [x.id,
                                  x.tags['Name'],
                                  x.groups[0].name,
                                  x.ip_address,
                                  x.private_ip_address,
                                  x.instance_type,
                                  x.image_id,
                                  x.key_name,
                                  x.state])) for x in instances]


# transform a list to a 'table' structure
def format_as_table(data,
                    keys,
                    header=None,
                    sort_by_key=None,
                    sort_order_reverse=False):
    """Takes a list of dict, formats the data, and returns
    the formated data as a text table.

    Required parameters:
        @data - Data to process (list of dicts). (Type: List)
        @keys - List of keys in the dict. (Type: List)

    Optional parameters:
        @header - The table header. (Type: List)
        @sort_by_key - The key to sort by. (Type: String)
        @sort_order_reverse - defaut is ascending. (Type: Boolean)
    """
    if sort_by_key:
        data = sorted(data,
                      key=itemgetter(sort_by_key),
                      reverse=sort_order_reverse)

    if header:
        header_divider = []
        for name in header:
            header_divider.append('-' * len(name))

        header_divider = dict(zip(keys, header_divider))
        data.insert(0, header_divider)
        header = dict(zip(keys, header))
        data.insert(0, header)

    column_widths = []
    for key in keys:
        column_widths.append(max(len(str(column[key])) for column in
            data))

    key_width_pair = zip(keys, column_widths)

    format = ('%-*s ' * len(keys)).strip() + '\n'
    formatted_data = ''
    for element in data:
        data_to_format = []
        for pair in key_width_pair:
            data_to_format.append(pair[1])
            data_to_format.append(element[pair[0]])
        formatted_data += format % tuple(data_to_format)

    return formatted_data


# pretty print the list in a colored table
def pprint_table(out, table):
    """
    Print a table of data, padded for alignment
    @param out: output stream, file-like object
    @param table: a table structure object
    """
    pass

if __name__ == "__main__":
    print format_as_table(dict_info, dict_keys, header=dict_keys,
            sort_by_key='group')
