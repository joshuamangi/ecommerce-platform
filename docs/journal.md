# Tech Journal

## API

- [ ] When you run for example docker compose stop db: Observe how the application behaves

 ``` yaml
 services:
  api:
    restart: on-failure
 ```

- [ ] To ensure the application reloads changes to files add the --reload to the command field

 ``` yaml
 command: >
      sh -c "
      python wait_for_db.py &&
      alembic upgrade head &&
      uvicorn main:app --host 0.0.0.0 --port 8000 --reload" # Importatnt to have this
 ```

 and also adding the api volume to refresh whenever changes are saved

 ``` yaml
 volumes:
      - .:/app
 ```

## DB

- [ ] To ensure migrations run when **docker compose down -v** is run add the section below

``` yaml
command: >
      sh -c "
      python wait_for_db.py && 
      alembic upgrade head && #Critical section
      uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
```

- [ ] To check if database service is up before api connects to db
Add the **wait_for_db.py**

``` yaml
command: >
      sh -c "
      python wait_for_db.py && #Critical section
      alembic upgrade head &&
      uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
```

- [ ] For transactional consistency implement WAL. It is implemented using BEGIN and COMMIT

``` sql
BEGIN
COMMIT
```

- [ ] **Deadlock Detected** Deadlocks occur when a resource wants to access a row held by another resource. To ensure
resource locks are kept safe, use SELECT ... FOR UPDATE to lock resources as shown in the logs below. This implies always locking in alphabetical or numerical order to prevent deadlocks. This makes it numerically improbable {eg. always lock SKU: A before locking SKU: B}. This is referred to as lock ordering.

``` log
db-1           | 2026-05-09 15:14:57.368 UTC [695] ERROR:  deadlock detected
db-1           | 2026-05-09 15:14:57.368 UTC [695] DETAIL:  Process 695 waits for ShareLock on transaction 743; blocked by process 694.
db-1           |        Process 694 waits for ShareLock on transaction 744; blocked by process 695.
```

- [ ] **Lock COntention** There is a huge cost of how long processes run with consistency enforced by locking. If you have a popular product, it will lead to slower processing and delays. Locking has massive performance implications! The database is mostly the bottleneck.

``` log
./scripts/run_test.sh
Lock acquired for A
Transaction completed in 2.0770 seconds
Lock acquired for A
Transaction completed in 4.0946 seconds
Lock acquired for A
Transaction completed in 6.1129 seconds
Lock acquired for A
Transaction completed in 8.1295 seconds
Lock acquired for A
Transaction completed in 10.1484 seconds
```

- [ ] Serialization is the highest level of isolation in the system, and it provides the effect of operations being executed sequentially, even though they are concurrent. It usually has very high performance effects. It was designed to mitigatte cases of dirty reads, phantom reads, write skews, non-repeatable reads

## Redis

- [ ] For busy systems opening and closing transactions per requests gets expensive due to TCP handshakes, authentication and socket handling which makes processes expensive, hence the implementation of connection pooling. So connection are pooled, kept alive, borrowed
