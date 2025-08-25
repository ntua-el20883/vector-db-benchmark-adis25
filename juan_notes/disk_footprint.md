To make it bullet-proof for replication, add three small pieces:

1. **Docker service name used** (so they know what container to exec into).
2. **Command you ran** (so they can copy-paste).
3. **Units** (MiB/GiB not MB/GB; `du -sh` outputs human-friendly IEC).

---

### Disk footprint

**Qdrant (single-node)**

* Service: `qdrant_bench`
* Command: `docker compose exec qdrant_bench sh -lc "du -sh /qdrant/storage"`
* Result: `599M /qdrant/storage`

**Milvus (single-node)**

* Service: `minio`

* Command: docker compose exec minio sh -lc "du -sh /data || du -sh /minio/data || true"

* Result: `4.0K /data`

* Service: `standalone`

* Command: docker compose exec standalone sh -lc "du -sh /var/lib/milvus || true"

* Result: `1.5G /var/lib/milvus`

---

| Dataset | Qdrant | Milvus-Minio | Milvus-Standalone |
|:--------|:------:|:------------:|:-----------------:|
| glove-100-angular                         | 599M | 4.0K | 1.5G |
| random-match-int-100-angular-filters      | 783M | 4.0K | 1.3G |
| random-match-int-100-angular-no-filters   | 514M | 4.0K | 1.3G |
| arxiv-titles-384-angular-filters          | 6.5G | | |
| arxiv-titles-384-angular-no-filters       | 3.3G | 4.0K | 12G |
| dbpedia-openai-100K-1536-angular          | 658M | 4.0K | 1.6G |
| dbpedia-openai-1M-1536-angular            | 5.7G | 4.0K | 17G |
| gist-960-euclidean                        | 3.7G | 4.0K | 8.5G |

The dataset arxiv-titles-384-angular-filters could not be ingested into Milvus because its filter schema defines duplicate field names, which Milvus rejects at collection creation. Qdrant’s schemaless payload system tolerates this inconsistency. All other datasets, including those with filters, ran successfully on both engines.