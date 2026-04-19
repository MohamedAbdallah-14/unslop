# Adding a Cache Layer

Caching is a key part of any solid system. You look at the mix of tradeoffs whenever you work through these complex decisions. A complete approach is essential.

The cache should be smooth, complete, and use modern patterns. You must measure first. Cache invalidation is hard.

## Options

- Redis — fast, networked, persistent
- Memcached — fast, networked, volatile
- In-process LRU — fastest, local, lost on restart

