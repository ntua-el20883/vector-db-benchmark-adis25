# Instructions to replicate Juan's methodology

## venv creation
Create venv in root directory with
```python
python -m venv venv
```

Then, go to:
```powershell
cd venv\Lib\site-packages\
```

And create a file named ```sitecustomize.py```. Type:
```python
import warnings
warnings.filterwarnings("ignore", "pkg_resources is deprecated", category=UserWarning)
```

This will ignore the ```pkg_resources``` package warning, which will stop being available at 30/11/25.

Remember to **always activate your venv** before doing anything, to prevent errors with global enviroment packages and variables. To activate the venv:
```powershell
venv/scripts/activate
```

Now you should see a ```(venv)``` at the begining of your directory like so:
```powershell
(venv) PS C:\Users\juant\Documents\Coding\vector-db-benchmark>
```

Install ```poetry``` package and activate it. In your root directory:
```powershell
pip install poetry
install poetry
```


## Qdrant configuration
Go to:
```powershell
cd engine\servers\qdrant-single-node\docker-compose.yaml
```

And change the version from ```1.11.0``` to ```1.14.0``` in this line:
```yaml
image: ${CONTAINER_REGISTRY:-docker.io}/qdrant/qdrant:${QDRANT_VERSION:-v1.11.0}
```

This is to prevent a certain warning regarding client and local versions incompatibility.


## Test on single-node servers

This is workflow for:

* Dataset: `glove-100-angular`
* Qdrant config: `qdrant-on-disk-default`
* Milvus config: `milvus-on-disk-default`
* Results directory: `.\results\`

---

**Step 1:** Getting started

First, check that not one server is running through Docker Desktop. You can either stop them from there or go to their directory, e.g.:

```powershell
cd engine\servers\milvus-single-node
docker compose down
```

---

**Step 2:** Start Qdrant.

```powershell
cd ..\qdrant-single-node
docker compose up -d
```

---

**Step 3:** Full run (upload + search).

```powershell
cd ..\..\..
python run.py --engines "qdrant-on-disk-default" --datasets "glove-100-angular"
```

The benchmark auto-downloads datasets defined in ```datasets/datasets.json``` into the repo’s ```datasets/``` folder and reuses them across runs; it does not re-download unless you delete them.

If it's your first time using the dataset, it may take a few minutes downloading it, only the first time.

Pipeline stages are: configure → upload → search. ```--skip-upload``` disables only the upload stage (see **Step 4**). Use it after your first successful run on a given engine+dataset to avoid re-uploading and to time search only.

Running the same command twice without --skip-upload will reuse the already-downloaded files but will perform another upload into the database and then search.

After running the command, you should get something like this:

```powershell
(venv) PS C:\Users\juant\Documents\Coding\vector-db-benchmark> python run.py --engines "qdrant-on-disk-default" --datasets "glove-100-angular"
Running experiment: qdrant-on-disk-default - glove-100-angular
C:\Users\juant\Documents\Coding\vector-db-benchmark\datasets\glove-100-angular\glove-100-angular.hdf5 already exists
Experiment stage: Configure
C:\Users\juant\Documents\Coding\vector-db-benchmark\engine\clients\qdrant\configure.py:78: DeprecationWarning: `recreate_collection` method is deprecated and will be removed in the future. Use `collection_exists` to check collection existence and `create_collection` instead.
  self.client.recreate_collection(
  self.client.recreate_collection(
Experiment stage: Upload
1183514it [03:49, 5152.95it/s]
Upload time: 230.19622150000032
Total import time: 305.24523559999943
Experiment stage: Search
10000it [00:11, 869.91it/s]
Experiment stage: Done
Results saved to:  C:\Users\juant\Documents\Coding\vector-db-benchmark\results
```

As the terminal says, the results are stored in:
```powershell
./results/qdrant-on-disk-default-glove-100-angular-search-0-2025-08-24-15-50-49.json
./results/qdrant-on-disk-default-glove-100-angular-upload-2025-08-24-15-50-37.json
```

Go to section **Results Explanation** for further details.

---

**Step 4:** Search-only repeat (optional, for cleaner latency/QPS).

```powershell
python run.py --engines "qdrant-on-disk-default" --datasets "glove-100-angular" --skip-upload
```

---

**Step 5:** Disk footprint.

```powershell
cd engine\servers\qdrant-single-node
docker compose exec qdrant_bench sh -lc "du -sh /qdrant/storage || du -sh /var/lib/qdrant || true"
```

You should get something like:
```powershell
599M    /qdrant/storage
```

Which means the on-disk footprint of the collection after indexing. Compare this number across engines; it’s independent of `--skip-upload` reruns.

---

**Step 6:** Wraping up

Stop qdrant and repeat process for ```milvus-single-node```.

For **Step 4: Disk footprint** in the case of milvus you can run:

```powershell
cd engine\servers\milvus-single-node
docker compose exec minio sh -lc "du -sh /data || du -sh /minio/data || true"
docker compose exec standalone sh -lc "du -sh /var/lib/milvus || true"
```
---

### Notes
* Use the exact engine names shown; do not use `qdrant-*` or `milvus-*` wildcards.
* Do not run both engines simultaneously for benchmarks.





## Results Explanation

### Search JSON
The ```search``` file should be something like this:
```json
{
  "params": {
    "dataset": "glove-100-angular",
    "experiment": "qdrant-on-disk-default",
    "engine": "qdrant",
    "parallel": 8,
    "config": {
      "hnsw_ef": 128
    }
  },
  "results": {
    "total_time": 11.532516400000532,
    "mean_time": 0.005708089239998662,
    "mean_precisions": 0.8557279999999999,
    "std_time": 0.00484112716654536,
    "min_time": 0.0032488999986526323,
    "max_time": 0.1625781000002462,
    "rps": 867.1134428215111,
    "p95_time": 0.007279240001025754,
    "p99_time": 0.01044472999972641
  }
}
```
What the search JSON means (query performance):

* `params.parallel`: client query concurrency (number of parallel query workers).
* `params.config.hnsw_ef`: search-time `ef` used for HNSW.
* `results.total_time`: wall time to execute the full query set under the given concurrency.
* `results.mean_time/std_time/min_time/max_time`: per-query latency stats in seconds.
* `results.p95_time/p99_time`: 95th/99th percentile per-query latency in seconds.
* `results.rps`: achieved queries per second (throughput).
* `results.mean_precisions`: average recall\@k versus ground-truth neighbors (higher = more accurate).

### Upload JSON
The ```upload``` file should be something like this:
```json
{
  "params": {
    "experiment": "qdrant-on-disk-default",
    "engine": "qdrant",
    "dataset": "glove-100-angular",
    "parallel": 4,
    "optimizers_config": {
      "memmap_threshold": 10000,
      "max_optimization_threads": 0
    },
    "hnsw_config": {
      "on_disk": true
    }
  },
  "results": {
    "post_upload": {},
    "upload_time": 230.19622150000032,
    "total_time": 305.24523559999943
  }
}
```

What the upload JSON means (ingest + index build):

* `params.experiment/engine/dataset`: identifiers only.
* `params.parallel`: client upload concurrency (number of parallel upload workers).
* `params.optimizers_config`: Qdrant optimizer knobs used during/after ingest (e.g., `memmap_threshold`, `max_optimization_threads`).
* `params.hnsw_config.on_disk: true`: HNSW index stored on disk.
* `results.upload_time`: pure data upload time in seconds.
* `results.total_time`: end-to-end time for the whole ingest phase (collection create/configure + upload + index build/optimize).
* `results.post_upload`: placeholder for any post-ingest stats (often empty).



