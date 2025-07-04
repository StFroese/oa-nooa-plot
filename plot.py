from pyalex import Works, Topics
import matplotlib.pyplot as plt
import numpy as np


field_topics = Topics().group_by("field.id").get()

field_names = [f["key_display_name"] for f in field_topics]
field_ids = [int(f["key"].split("/")[-1]) for f in field_topics]

ratios = {}
for fn, fid in zip(field_names, field_ids):
    works_oa = Works().filter(primary_topic={"field": {"id": fid}}).filter(is_oa=True)
    pager_oa = works_oa.group_by("cited_by_count").paginate(per_page=200, n_max=None)

    cites_oa = np.sum(
        [
            int(bucket["key"]) * int(bucket["count"])
            for page in pager_oa
            for bucket in page
        ]
    )

    total_works_oa = works_oa.count()

    works_noa = Works().filter(primary_topic={"field": {"id": fid}}).filter(is_oa=False)
    pager_noa = works_noa.group_by("cited_by_count").paginate(per_page=200, n_max=None)

    cites_noa = np.sum(
        [
            int(bucket["key"]) * int(bucket["count"])
            for page in pager_noa
            for bucket in page
        ]
    )

    total_works_noa = works_noa.count()

    ratios[fn] = (cites_oa / total_works_oa) / (cites_noa / total_works_noa)
    print(ratios)

print(ratios)

fields, values = zip(*sorted(ratios.items(), key=lambda kv: kv[1], reverse=True))

# map each field to a y-coordinate
y = range(len(fields))

plt.figure(figsize=(10, 7))
plt.scatter(values, y)  # points, not bars
plt.yticks(y, fields)
plt.gca().invert_yaxis()  # biggest ratio at the top
plt.xlabel("OA / non-OA mean-citation ratio")
plt.title("Citation advantage of OA vs non-OA by field")
plt.tight_layout()
plt.show()
