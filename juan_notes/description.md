# Vector Database Benchmarking: Qdrant vs Milvus

## Description
In this project, you will be asked to compare the performance of various aspects of two popular and open-source vector database systems. This entails the following aspects that must be tackled by you:

1) **Installation and setup of two specific Vector DBs**: Using local or okeanos-based resources you are asked to successfully install and setup the two systems. This also means that if any (or both) of the DBs got a cluster edition (distributed mode) that this will be also available for testing.

2) **Data generation (or discovery of real data) and loading to the two DBs**: Using either a specific data generator, online data or artificially creating data, you should identify and load a significant amount of vectors into the databases. Ideally, loaded data should be:
    
    a) big (or as big as possible), not able to fit in main memory,

    b) have varying dimensionality (vector size and type - integer, float) and
    
    c) the same data loaded in both databases.

Data loading is a process that should be monitored, namely: the time it takes to load a small, medium and the final amount of data, as well as the storage space it takes in each of the databases (i.e., how efficient data compression or possible indexing is).

3) **Query generation to measure performance**: A set of similarity queries (common to both DBs) must be compiled in order to test the performance of the vector DBs. Queries should target similar similarity metric algorithms (if implemented on both DBs, e.g., Euclidean distance (L2), Inner product, Cosine similarity, etc.) with and without filters (https://github.com/qdrant/ann-filtering-benchmark-datasets).

4) **Measurement of relevant performance metrics for direct comparison**: Client process(es) should pose the queries of the previous step and measure the DB performance (query latency, throughput, CPU load if possible, etc). Teams should be careful and compare meaningful statistics in this important step.

Teams undertaking this project can take advantage of existing benchmarking code either in principle or in whole. I suggest looking at the qdrant Benchmark Suite (https://github.com/qdrant/vector-db-benchmark), which for many of the DBs contains code for data generation, loading, queries and measurement.

Besides the aforementioned project aspects, you are free to improvise in order to best demonstrate the relative strengths and weaknesses of each system. By the end of your project, you should have a pretty good idea of what a modern vector DB is, its data and query processing model and convey their strong/weak points.
