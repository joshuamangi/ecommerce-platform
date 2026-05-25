# TradeOffs

- [ ] The cost of performing insertions with indexes is wild!! It takes a very long time to write 100,000 rows. Below is how fast inserting 100,000 records without an index is

``` log
python3 -m scripts.populate_catalogue
Dropping indexes...
Generating 100000 records...
Inserting data...
Recreating indexes...
Done in 2.51 seconds.
```

- [ ] Request coalescing occurs when ttl expires and it forces the edge computers to query the originating servers with massive requests. Instead of having all these requests hitting the main server, one request is tagged with fetching, the rest are put to wait. Once the response is sent it updates the other caches.

- [ ] In scenarios of edge caching or content delivery network, if the geo-dns fails. It provides a single point of failure where there will be cascading faults, and total unavailability. it is therefore important to implement Multiple DNS eg Route53 and Cloudflared with a hybrid management for failover. Or AnyCast or ensuring it defualts to management at a lower level

- [ ] Edge POP should embrace using AnyCast since it removes the need for having a central Geo-DNS to having a shared IP for all Edge POPs and using nearest routes to direct traffic.

- [ ] Use NoSQL DBs when you don't required the overhead of joins, when you have high volume and high write data operations since the requirements for indexing in relational data slows writes down. Situations where the schema regularly changes, high throughput operations
