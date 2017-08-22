import json
import csv
import json
import os
import matplotlib.pyplot as plt

filename = "record.son"
with open(filename) as f:
    record = json.load(f)
for post_id in record:
    test_post = record[post_id]
    record_time = test_post["record_time"]
    record_data = test_post["record_data"]
    ax = plt.subplot(111)
    plt.plot(record_time, record_data[1],'b-', label = "total", linewidth = 2.0)
    plt.plot(record_time, record_data[2],"g-", label = "fans" , linewidth = 2.0)
    plt.title(post_id)
    plt.xlim(0, 96)
    plt.xlabel("hour")
    plt.ylabel("impression")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(post_id, bbox_inches='tight', dpi= 300)
    plt.clf()



