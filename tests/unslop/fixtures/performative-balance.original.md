# Trade-offs

Redis is fast, however, it requires a separate process. However, for most teams this is fine.

Memcached is lightweight, however, it loses data on restart. However, that's often acceptable for pure caching.

The decision is straightforward, however, it depends on your durability needs.
