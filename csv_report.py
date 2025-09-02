import csv

def write_csv_report(page_data: dict[str: str], filename="report.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        headers = ["page_url", "h1", "first_paragraph", "outgoing_link_urls", "image_urls"]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        not_crawled = []
        for key, page in page_data.items():
            if page is not None:
                try:
                    writer.writerow({"page_url": page["url"],
                                    "h1": "NULL" if page["h1"] == "" else page["h1"],
                                    "first_paragraph": "NULL" if page["first_paragraph"] == "" else page["first_paragraph"],
                                    "outgoing_link_urls": "NULL" if ";".join(page["outgoing_links"]) =="" else ";".join(page["outgoing_links"]),
                                    "image_urls": "NULL" if ";".join(page["image_urls"]) == "" else ";".join(page["image_urls"])})
                except KeyError as ke:
                    print(f"Key Error while attempting to write csv report! {ke}")
                except Exception as e:
                    print(f"Unknown error! {e}")
            else:
                #print(f"Page not processed: {key} {page}")
                not_crawled.append(key)
    
    unprocessed_report, extension = filename.split(".")
    unprocessed_report += "_unprocessed" + "." + extension
    with open(unprocessed_report, mode="w", newline="", encoding="utf-8") as csvfile:
        headers = ["page_url"]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for url in not_crawled:
            try:
                writer.writerow({"page_url": url})
            except Exception as e:
                print(f"Unknown error! {e}")