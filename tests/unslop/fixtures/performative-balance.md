# Trade-offs

Redis is fast. It requires a separate process. For most teams this is fine.

Memcached is lightweight. It loses data on restart. That's often acceptable for pure caching.

The decision is straightforward. It depends on your durability needs.
