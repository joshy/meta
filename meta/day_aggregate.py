from collections import Counter
from datetime import datetime, timezone
from collections import OrderedDict


def agg(docs):
    counts = []
    for i in docs["groups"]:
        for acc in i["doclist"]["docs"]:

            counts.append(acc["StudyDate"])
    print("length = ", len(counts))
    c = Counter(counts)
    print(c)
    r = {
        int(
            datetime.strptime(str(k), "%Y%m%d").replace(tzinfo=timezone.utc).timestamp()
        ): v
        for k, v in c.items()
    }
    keys = sorted(r.keys())
    min = keys[0]
    max = keys[-1]

    return r, min, max
