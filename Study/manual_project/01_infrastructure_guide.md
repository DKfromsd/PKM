# Step 1: Data Infrastructure & Semantic Model Foundation

This guide explains the core infrastructure components for building an MCP-enabled analysis agent that understands and responds to business logic using LLMs.

## 1. Apache Kafka (The Real-time Event Heartbeat)

Kafka acts as the central nervous system, handling high-volume event streams from mobile terminals.

### Structure & Data Flow
- **Producer**: Mobile devices or apps sending JSON events.
- **Topic**: Named after the event type (e.g., `call_events`).
- **Consumer**: Systems like Snowflake (via Snowpipe Streaming) or GCP Buckets.

### Event Format (Example)
```json
{
  "eventtype": "call_start",
  "imei": "3587XXXXXXXXXXX",
  "callresult": "success",
  "timestamp": "2026-03-31T14:30:00Z"
}
```

### Metadata & Control
- **Topic Name**: Represents the semantic event type.
- **Key**: Often used as the target table name in the destination DW.
- **Headers**: Contains `schema_version`, `app_version` for schema enforcement.
- **Auto-generated**: Kafka automatically adds `partition`, `offset`, and `createtime` to every message for ordering and traceability.

### Why Kafka?
1. **Asynchronous**: Decouples producers from consumers, preventing system bottlenecks.
2. **Persistence (Lossless)**: Distributed replication ensures no data is lost even if consumers are offline.
3. **Fan-out**: Multiple systems (DW, Spark, OpenSearch) can consume the same data simultaneously.

---

## 2. PostgreSQL (Metadata & Semantic Master)
- **Role**: Stores the Data Dictionary, User Permissions, and the Master Semantic Models.
- **Agent Integration**: Used by the agent to look up business definitions before querying the warehouse.

## 3. Apache Iceberg (Lakehouse Table Format)
- **Role**: Manages massive JSON event data efficiently in object storage.
- **Key Features**: Schema Evolution (handles changing JSON structures), Time Travel (querying data as it was at a specific point in time), and Hidden Partitioning.

## 4. Apache Spark (Distributed Processing Engine)
- **Role**: Performs ETL (Extract, Transform, Load) operations, cleaning and refining raw Kafka streams into Iceberg tables.
- **Capabilities**: High-performance distributed computing and Structured Streaming.

## 5. OpenSearch (Search & Semantic Search Engine)
- **Role**: Provides fast log analysis and vector search capabilities.
- **Agent Integration**: Helps the agent perform semantic mapping (e.g., "Show me call failures" -> mapping "failures" to specific `callresult` codes).

---

## Next Step: Semantic Model Design
In Step 2, we will define how the Agentic AI maps these technical components to business-level questions using a Data Dictionary and LLM prompts.
