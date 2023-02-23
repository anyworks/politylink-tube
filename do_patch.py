import argparse
import logging
from typing import List

import time

from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video
from mylib.utils.path import PathHelper
from mylib.workflow.models import StatusCode
from mylib.workflow.patch import PatchRequest, PatchJobScheduler

LOGGER = logging.getLogger(__name__)

LOG_DATE_FORMAT = "%Y-%m-%d %I:%M:%S"
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'


def build_requests() -> List[PatchRequest]:
    requests = []
    client = SqliteClient(host='mini')
    videos = client.select_all(Video)
    for video in videos:
        requests.append(PatchRequest(
            video_id=video.id,
            datetime=video.datetime
        ))
    return requests


def main():
    path_helper = PathHelper(host='mini')
    scheduler = PatchJobScheduler(path_helper)
    while True:
        requests = build_requests()
        jobs = scheduler.schedule_batch(requests)
        if not jobs:
            time.sleep(300)
            continue

        LOGGER.info(f'found {len(jobs)} jobs')
        job = jobs[0]
        LOGGER.info(f'run {job}')
        result = job.run()

        if result != StatusCode.SUCCESS:
            LOGGER.error(f'failed to execute {job}')
            scheduler.record_failed_job(job)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        datefmt=LOG_DATE_FORMAT, format=LOG_FORMAT)
    main()
