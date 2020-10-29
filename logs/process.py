from collections import defaultdict
import csv

# 3- site version or checkout page
# 4- page load time
# 5- button click time if applicable
# 6- button id if applicable
# 7- user id

user_logs = defaultdict(list)

# SPECIAL CASE: ztfsdvdw
# visited both versions of site

# SPECIAL CASE: xcbiydf
# log got cut off, or visit was too short

# SPECIAL CASE: hnbbuja
# first loaded page was checkout, likely means log was cut off

# SPECIAL CASE: fvakaxva
# only loaded first page and did nothing else

SPECIAL_CASE = True

with open("filtered_log.csv") as csvfile:
    reader = csv.reader(csvfile, dialect="excel-tab")
    for row in reader:
        user_id = row[7]
        user_logs[user_id].append(row)

if SPECIAL_CASE:
    visit_1 = user_logs["ztfsdvdw"][:7]
    visit_2 = user_logs["ztfsdvdw"][7:14]
    visit_3 = user_logs["ztfsdvdw"][14:]
    del user_logs["ztfsdvdw"]
    user_logs["ztfsdvdw+1"] = visit_1
    user_logs["ztfsdvdw+2"] = visit_2
    user_logs["ztfsdvdw+3"] = visit_3

    del user_logs["xcbiydf"]
    del user_logs["hnbbuja"]
    del user_logs["fvakaxva"]

# getting return rates
def user_returned(logs):
    clicked_checkout = False
    for log in logs:
        if log[3] == "C":
            clicked_checkout = True
        if clicked_checkout and log[3] != "C":
            return True
    return False

# return_rate = [returns, no_returns]
return_a = [0, 0]
return_b = [0, 0]

for logs in user_logs.values():
    did_return = user_returned(logs)

    if logs[0][3] == "A":
        if did_return:
            return_a[0] += 1
        else:
            return_a[1] += 1
    elif logs[0][3] == "B":
        if did_return:
            return_b[0] += 1
        else:
            return_b[1] += 1
    else:
        print("ERROR!")

# getting times to completion
completion_a = []
completion_b = []

for logs in user_logs.values():
    start_time = int(logs[0][4])
    end_time = None
    if logs[-1][3] == "C":
        end_time = int(logs[-1][4])
    else:
        if logs[-1][5] == "0":
            end_time = int(logs[-1][4])
        else:
            end_time = int(logs[-1][5])
    assert end_time != None
    
    if logs[0][3] == "A":
        completion_a.append(end_time-start_time)
    elif logs[0][3] == "B":
        completion_b.append(end_time-start_time)
    else:
        print("ERROR!")

print(completion_a)
print(completion_b)
