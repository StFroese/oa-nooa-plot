import argparse
import datetime

from pyalex import Works, Topics
import numpy as np
import pandas as pd


def default_year():
    """Last publication year that is complete at the time of the run."""
    return datetime.date.today().year - 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        default=default_year(),
        help="publication year to restrict the comparison to",
    )
    year = parser.parse_args().year

    domains = Topics().group_by("domain.id").get()
    domain_ids = [int(d["key"].split("/")[-1]) for d in domains]
    domain_names = [d["key_display_name"] for d in domains]

    rows = []
    for dn, did in zip(domain_names, domain_ids):
        field_topics = Topics().filter(domain={"id": did}).group_by("field.id").get()

        field_names = [f["key_display_name"] for f in field_topics]
        field_ids = [int(f["key"].split("/")[-1]) for f in field_topics]

        for fn, fid in zip(field_names, field_ids):
            works_oa = (
                Works()
                .filter(primary_topic={"field": {"id": fid}})
                .filter(publication_year=year)
                .filter(is_oa=True)
            )
            pager_oa = works_oa.group_by("cited_by_count").paginate(
                per_page=200, n_max=None
            )

            cites_oa = np.sum(
                [
                    int(bucket["key"]) * int(bucket["count"])
                    for page in pager_oa
                    for bucket in page
                ]
            )

            total_works_oa = works_oa.count()

            works_noa = (
                Works()
                .filter(primary_topic={"field": {"id": fid}})
                .filter(publication_year=year)
                .filter(is_oa=False)
            )
            pager_noa = works_noa.group_by("cited_by_count").paginate(
                per_page=200, n_max=None
            )

            cites_noa = np.sum(
                [
                    int(bucket["key"]) * int(bucket["count"])
                    for page in pager_noa
                    for bucket in page
                ]
            )

            total_works_noa = works_noa.count()

            ratio = (cites_oa / total_works_oa) / (cites_noa / total_works_noa)

            rows.append(
                dict(
                    year=year,
                    domain=dn,
                    field=fn,
                    oa_cites=cites_oa,
                    oa_works=total_works_oa,
                    noa_cites=cites_noa,
                    noa_works=total_works_noa,
                    ratio_avg_cites=ratio,
                )
            )

    df = (
        pd.DataFrame(rows)
        .sort_values("ratio_avg_cites", ascending=False)
        .reset_index(drop=True)
    )

    df.to_csv("data.csv")


if __name__ == "__main__":
    main()
