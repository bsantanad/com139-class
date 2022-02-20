from analysis.analyzer import *
from simulation.config import *
from assets.status import Status

import matplotlib.pyplot  as plt

# TODO: Create report of multiple executions


def report_all_by_field_obj(my_objs: list, my_field: str, 
                            w_filter: bool = False, val: float = 0.0) -> None:

    # this will iterate thru all the report fields, waiting time etc
    print('\n === Report for %s field ===' % my_field)
    total_cust = len(my_objs)
    print(f'total number of customers {total_cust}')

    is_status = isinstance(getattr(my_objs[0], my_field), Status)
    if not is_status:
        max_time = get_max_obj(my_objs, my_field, w_filter, val)
        min_time = get_min_obj(my_objs, my_field, w_filter, val)
        print('Max %s: %5.3f by %s' %
            (
                my_field, 
                max_time, 
                objects_as_str(
                    get_matching_value_obj(my_objs, my_field, max_time)
                )
            )
        )
        print('Min %s: %5.3f by %s' %
            (
                my_field, 
                min_time, 
                objects_as_str(
                    get_matching_value_obj(my_objs, my_field, min_time)
                )
            )
        )
        print('Mean %s: %5.3f' % 
            (
                my_field, 
                get_mean_obj(my_objs, my_field, w_filter, val)
            )
        )
        print('Median %s: %5.3f' % 
            (
                my_field, 
                get_median_obj(my_objs, my_field, w_filter, val)
            )
        )

        try:
            print('Mode %s: %5.3f' % 
                (
                    my_field, 
                    get_mode_obj(my_objs, my_field, w_filter, val)
                )
            )
        except Exception:
            print('No mode found in data')

        print('Stdev %s: %5.3f' % 
            (
                my_field, 
                get_stdev_obj(my_objs, my_field, w_filter, val)
            )
        )
        print('Variance %s: %5.3f' % 
            (
                my_field, 
                get_variance_obj(my_objs, my_field, w_filter, val)
            )
        )
        print('Variance %s: %5.3f' % 
            (
                my_field, 
                get_variance_obj(my_objs, my_field, w_filter, val)
            )
        )

        min_time = get_min_obj(my_objs, my_field, w_filter, val)
        min_customers = get_matching_value_obj(my_objs, my_field, min_time)
        percentage = (len(min_customers) / total_cust) * 100
        print(f'Percentage of Min Value {my_field}: {percentage}')

        # TODO: Group std dev customers and display the list
    else:
        print(is_status)
        statuses = get_map_values(my_objs, my_field)

        success = 0
        failed = 0
        undefined = 0
        wait = 0

        for status in statuses:
            status = str(status)
            if status == 'SUCCESS':
                success += 1
            if status == 'RENEGED':
                failed += 1
            if status == 'UNDEFINED':
                undefined += 1
            if status == 'WAIT':
                wait += 1

        # histogram data
        print(f'success customers: {success}')
        print(f'failed customers: {failed}')
        print(f'undefined customers: {undefined}')
        print(f'wait customers: {wait}')

        # graph histogram
        plt.bar([1, 2, 3, 4], height = [undefined, success, failed, wait])
        plt.ylabel('customers')
        plt.xlabel('undefined - success - failed -- wait')
        plt.show()

        # success rate 
        print(f'success rate: {success/len(statuses)}')


def report_all_by_ts(my_ts: list, my_label: str, total_time: float) -> None:
    print('\n === Report for %s resource ===' % my_label)
    if my_ts:
        # print_ts(my_ts, my_label)
        # print('Min queue: %4.3f' % get_min_ts(my_ts))
        print('Max queue: %4.3f' % get_max_ts(my_ts))
        service_vals = get_cumulative_time_ts(my_ts, total_time)
        percent_vals = get_bin_percent_ts(service_vals, total_time, my_label)
        if CREATE_SIM_GRAPHS:
            plot_ts(my_ts, total_time, my_label)
            evolution_bar_ts(my_ts, total_time, my_label)
            cumulative_time_ts(service_vals, my_label)
            hist_bar_ts(my_ts, 'value', my_label)
    else:
        print('%s not used' % my_label)
