import concurrent.futures


class IngestionManager:
    def __init__(self):
        self.repositoryMap = RepositoryMap()
        self.bpelClient = BpelClient()
        self.ingestPoolSize = 5
        self.ingestThreadPool = ThreadPoolExecutor(max_workers=ingestPoolSize)
        self.stopped = False