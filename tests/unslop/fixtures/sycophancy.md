# Adding a Cache Layer

Caching is a key part of any reliable system. You look at the blend of tradeoffs whenever you work through these complex decisions. A broad approach is essential.

The cache should be smooth, overall, and use advanced patterns. You must measure first. Cache invalidation is hard.

## Options

- Redis — fast, networked, persistent
- Memcached — fast, networked, volatile
- In-process LRU — fastest, local, lost on restart

