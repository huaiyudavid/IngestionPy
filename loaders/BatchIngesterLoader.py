import sys
import traceback
from ingestion.BatchIngester import BatchIngester

if len(sys.argv) == 0:
    print "Must specify directory from which to ingest!"
    sys.exit()

ingester = BatchIngester()

try:
    ingester.ingestDirectories(sys.argv)
except:
    traceback.print_stack()