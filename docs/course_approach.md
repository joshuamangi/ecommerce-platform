# Approach

Build incrementally. Developing the entire system at once will lead to "integration hell," where you cannot pinpoint whether a failure stems from your Nginx configuration, a service communication bug, or a database connection issue.

Follow these stages to learn effectively:

1. The "Vertical Slice" Prototype (Module 1-2)
Start with one service (Catalog) and its database. Get the full stack—Dockerfile, Compose configuration, and FastAPI endpoint—working. Verify that you can perform a CRUD operation from your machine to the containerized service. This validates your environment setup.

2. Service Expansion (Module 3)
Once the Catalog service is stable, add the Pricing service. Focus on inter-service communication. Have the Catalog service perform a synchronous HTTP call to the Pricing service to fetch a price when a product is requested. This is where you learn about service discovery and why <http://pricing-service> works inside Docker.

3. Asynchronous Decoupling (Module 4)
Introduce the message queue. Instead of the Catalog service directly asking Pricing for a calculation, have the services communicate via events. This is the transition from a "distributed monolith" to a true event-driven architecture. If you wait until the end, you will struggle to debug the asynchronous flow because you won't have the baseline of synchronous success to compare it against.

4. Observability and Scaling (Module 5-6)
Only after you have multiple services communicating should you add the Prometheus/Grafana stack or Nginx load balancing. It is impossible to observe or scale a system that isn't functionally complete.

Why this approach works:
Isolate Failures: If you add one service at a time, you know exactly which change introduced a bug.
Mental Model: You will understand the "why" behind API Gateways and Message Queues because you will have felt the pain of trying to manage services without them.
Iterative Refinement: You will likely realize your initial database schema or API design is flawed. It is significantly cheaper to refactor one or two services as you go than to rewrite a seven-module system at the end.
Treat the modules as building blocks. Build, test, and break the previous module's work before moving to the next. By the time you reach Module 7, you will not just have a project; you will have a deep, practical understanding of why each architectural decision was necessary.
