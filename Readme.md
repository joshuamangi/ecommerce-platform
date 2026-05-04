# System Design For A Distributed E-commerce Platform

## Goal

    The goal of this project is to learn system design for distributed systems.
    Being able to understand the need for
    - Scaling (Horizontal and Vertical)
    - Decoupling Tradeoffs
    - Latency, Throughput, Availability and the numbers eg P99, P95, P90 or 99.9 and latency delays in milliseconds
    - CAP theorem
    - Synchronous and Asynchronous Communication

### Technologies Used

    - Postgres(JSONB)
    - Postgres
    - Redis
    - Docker
    - Docker compose (orchestrator)
    - RabbitMQ

### Key TakeAways

    - Break down big problems into smaller problems
    - Contextualize the problem to the current problem and look for solutions
    - To be able to understand more about the system create a tradeoff table for the comparisons and weight against the business needs

#### Scaling

    For small projects always start with Vertical scaling and as performance demands increase scale to Horizontal scaling. Vertical Scaling has a cap and limit of resources but Horizontal scaling is practically unlimited resources. There is an added monetary cost of scaling horizontally. It introduces latency due to increased synchronization consistency. For horizontal scaling there is higher availability as compared to Single Points of Failures for vertical scaling scenarios

#### Latency, Throughput and Availability

    - Latency (Cost of Time) 
        . Measured in millisconds. 
        . The time taken from a request to be sent and a response to be received
        . Should be handled efficiently in distributed systems
        . Uses P90, P95, P99 and it shows how it a system affects response times for the most affected users after times are arranged in ascending order for each percentile
        *Strategies*
        - Include Edge computing and Caching
    - Throughput (Capacity of work)
        . Measured in requests per second
        *Strategies*
        - Include Batching and Asynchronous Queueing
    - Availability (Probability of Success)
        . Measured using percentages eg 99, 99.9, 99.99
        . For example for one year the 99% means 3.65 days of downtime, and 99.99% means 52.56 minutes of sowntime per year
        *Strategies*
        - Include Redundancy and Replication

#### CAP Theorem

    Mostly in distributed systems the communication within nodes experiences breakdowns

    - Consistency: Ensures a system is always in a state where for all partitions all reads should show all successful rights on all partitions. If not it would not return accurate data. Necessary for systems like banking, inventory and booking that must ensure consistent and real time updates are fundamental.

    - Availability: Ensures a system provides a response even when there are network partition failures. For example social media feeds. 

    - Partition Tolerance: In modern systems network partitions within nodes almost have issues with communication and availability

    The CAP theorem states that for distributed systems, network partitons always fail and the concern is mostly a tradeoff of Consistency or Availability in case of Partition failures

    . Consistent Partition (CP)
    . Availabilty Partition (AP)

#### Request Flow and Synchronous versus Asynchronous Communication

    For API communications
    Synchronous Communication: 
    
    Used for real time updates and immediate feedback
    Asynchronous Communication:

    - For long running tasks and requests that involve cascading events use asynchronous communication to send a 202 accepted message, add the task to a queue and have background workers handling the requests and use patterns like webhooks, websockets, pooling(status endpoint). The server sends a 202 response indicating the request has been accepted amd depending on the patterns, the fesign can use the approach of polling, webhooks and websockets/SSE. Also add a request_id or correlation_id to track requests.
    - For scenarios where the consumer may fail. For AMQP protocols like RabbitMQ, you use ACK for messages between the broker and the consumer. The message is marked as unacknowledged. If the consumer doesn't send an ACK response, the message is requeued and status put to ready again for consumption. There are techniques used to ensure messages aren't reconsumed, including using idempotency keys, dead letter exchanges and visibility timeouts for SQS

#### Decoupling

    For the ecommerce application, decoupling is crucial to allow the different services to scale separately. Eg when there is a black friday spike, the catalog service can scale separately to the inventory service that is more dependent on physical constraints.
