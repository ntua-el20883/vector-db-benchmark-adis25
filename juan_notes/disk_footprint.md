To make it bullet-proof for replication, add three small pieces:

1. **Docker service name used** (so they know what container to exec into).
2. **Command you ran** (so they can copy-paste).
3. **Units** (MiB/GiB not MB/GB; `du -sh` outputs human-friendly IEC).

---

### Disk footprint — glove-100-angular

**Qdrant (single-node)**

* Service: `qdrant_bench`
* Command: `docker compose exec qdrant_bench sh -lc "du -sh /qdrant/storage"`
* Result: `599M /qdrant/storage`

**Milvus (single-node)**

* Service: `minio`

* Command: `docker compose exec minio sh -lc "du -sh /data || du -sh /minio/data || true"`

* Result: `4.0K /data`

* Service: `standalone`

* Command: `docker compose exec standalone sh -lc "du -sh /var/lib/milvus || true"`

* Result: `1.5G /var/lib/milvus`

---
