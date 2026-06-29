# Tech Journal

- It is finding and building solutions to problems.
- It is important to note System Design is a continuous thing.
- It is a matter of understanding tradeoffs.
- For scaling it is very crucial to know the time and space complexities of data structures and algorithms

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

- [ ] Modelling a database involves transitioning from EAV model(Entity-Attribute-Value) model and flat tables to having a hybrid to circumvent the cost of joins and having large flat tables

- [ ] Creating indexes involves monitoring the database, analyzing it and knowing what to index. Use  GIN index that maps key value pair attributtes to rows

- [ ] Stored Procedures adds atomicity and helps to reduce latency and adds logic inside the database. In the example of an ecommerce platform, it can allow you to check if inventory stock exists or not before reducing the stock quantity or making an order, hence ensuring atomicity and reduces the number of requests for multiple tables. It should however not be overused since it will make it hard to perform tests since logic exists inside the db

## Redis

- [ ] For busy systems opening and closing transactions per requests gets expensive due to TCP handshakes, authentication and socket handling which makes processes expensive, hence the implementation of connection pooling. So connection are pooled, kept alive, borrowed
- [ ] Redis does not resolve underlying issues with the database, it only serves as a performance upgrade.

## Data Structures and Algorithms

It is important in Computer science to be aware of the impact of loops, algorithms and their time and space complexities. Commonly approximated using Big O notation : which evaluates the worst case scenarios. Big theta notation which checks the mean time and Big Omega notation which looks at the best case scenario.
In computer science the aim is to always optimize the operation. Time complexity is measured in operations instead of time because of difference in hardware.

- [ ] Runtimes
      - Constant runtimes: denoted using O(1). Which means regardless of the size of the data it will take the same operation for example retrieving an item from an array, mathematical operations, fetching an item from a hashmap, Poppring and pushing from a stack. Constant runtimes are the best runtimes.
      - Logarithmic runtimes: denoted using O(Log(n)): Usually the base is to base 2 since computer science uses binary. The logarithmic runtime of an algorithm halves the size of the data and discards the rest. A common example is to use the Binary search of sorted data. If you have sorted data, use binary search.
      - Linear runtimes: denoted as O(n). This means it grows with the size of the data. A good example of this is for loops which looks through all the data. To optimize this, if you already have sorted data, use binary search. Also if you encounter a for loop and you have sorted data, use a for loop
      - Quadratic runtimes: denoted as O(n^2): Just like Linear runtime, Audratic runtimes are polynomial runtimes and are manageable to some extent.
      - Cubic runtimes: denoted as (n^3). They include triple for loops and matrix operations
      - Polynomial runtimes: denoted as O(n^k). This includes linear runtime, quadratic and cubic runtime. They are considered manageable and are tractable problems. intractable problems include exponentials. When designing algortihms, the goal is to come up with polinomial solutions and if exponential solutions show up, one should think of Dynamic Programming or Divide and Conquer.
      - Exponential runtimes: denoted as O{2^n}. These are considerred redflags in computer science

## Nginx

## FastAPI

## Message Queues

## Observability
