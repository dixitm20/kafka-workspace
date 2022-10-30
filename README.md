# kafka-workspace

# Follw Below Steps To Run Application
## Step 1: Create python3 venv
```
$ python3.8 -m venv .venv --prompt assignment-venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Step 2:  Initialize kafka infra
```
$ ./scripts/init-kafka.sh
```

## Step 3:  Run Producer To Load Messages Into Input Topic
```
$ ./scripts/run-producer.sh
```

## Step 4:  Run Transformer To Modify Input Messages From Input Topic & Load Them Into Output Topic
```
$ ./scripts/run-transformer.sh
```

## Step 5:  Tear down kafka infra
```
$ ./scripts/clear-kafka.sh
```