# Bash deployment - Grafana

## Type of data
#### TIME
#### CPU
#### RAM
#### Network - packets 

## How to run
```bash
# Deploy to Instance1 (Grafana + DB)
$ ./benchmark/benchmark.sh -a grafana -t bash && ./grafana.sh && ./benchmark/finished.sh

# Deploy to Instance1 and Instance2 (DB separate frome Grafana)
$ ./benchmark/benchmark.sh -a grafana -t bash && ./split_grafana.sh && ./benchmark/finished.sh

# Deploy to All instances (Grafana + DB)
$ ./benchmark/benchmark.sh -a grafana -t bash && ./multi_grafana.sh && ./benchmark/finished.sh
```

## OR
```bash
./benchmark_grafana.sh -d [ multi, single, split ] -p [ LOGS_PATH ]
```
