from crawler import crawl_jobs
from supabase_client import upsert_jobs, export_json
import json
import os
from datetime import datetime

SYNC_FILE = "last_sync.json"


def already_synced_today():
    if not os.path.exists(SYNC_FILE):
        return False
    with open(SYNC_FILE, "r") as f:
        data = json.load(f)
        return data.get("lastSync") == datetime.now().strftime("%Y-%m-%d")


def mark_synced_today():
    with open(SYNC_FILE, "w") as f:
        json.dump({"lastSync": datetime.now().strftime("%Y-%m-%d")}, f)


def main():
    # if already_synced_today():
    #     print("已同步過，跳過")
    #     return

    jobs = crawl_jobs()
    if jobs:
        try:
            upsert_jobs(jobs)
            export_json()
            mark_synced_today()
            print(f"同步 {len(jobs)} 筆職缺完成")
        except Exception as e:
            print(f"同步失敗: {e}")
    else:
        print("未抓到職缺")


if __name__ == "__main__":
    main()
