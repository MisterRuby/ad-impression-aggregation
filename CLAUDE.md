# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an IPTV ad impression aggregation system that processes advertising log data through a stream processing pipeline using Apache NiFi and Apache Kafka. The system generates sample IPTV advertising logs and processes them through a containerized data pipeline.

## Architecture

The system consists of three main components:

1. **Ad Log Generator** (`iptv-ad-log-generator/`): Python script that generates sample IPTV advertising impression logs as CSV files
2. **Apache NiFi** (`nifi/`): Data ingestion and processing layer that reads CSV files and transforms them
3. **Apache Kafka** (`kafka/`): Message streaming platform for real-time data processing

### Data Flow
```
Ad Log Generator → CSV Files → NiFi (GetFile → ConvertRecord) → Kafka Topics → Output Processing
```

## Common Development Commands

### Starting the Full Stack
```bash
# Start all services (from root directory)
docker-compose up -d

# Or start individual services
cd kafka && docker-compose up -d  # Kafka cluster only
cd nifi && docker-compose up -d   # NiFi only
```

### Working with the Ad Log Generator
```bash
cd iptv-ad-log-generator

# Install dependencies
pip install -r requirements.txt

# Generate logs once (10,000 records by default)
python ad_log_generator.py --once

# Generate specific number of logs
python ad_log_generator.py --once --count 500

# Run in scheduler mode (generates logs every minute)
python ad_log_generator.py
```

### Kafka Operations
```bash
cd kafka

# Create Kafka topics
./scripts/create-topics.sh

# Monitor Kafka messages
docker exec kafka-broker kafka-console-consumer --bootstrap-server localhost:9092 --topic ad-impressions --from-beginning
```

### Accessing Web UIs
- **NiFi UI**: https://localhost:8443/nifi (admin/ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB)
- **Kafka UI**: http://localhost:8090

## Configuration Files

- `iptv-ad-log-generator/config.json`: Controls ad log generation (channels, advertisers, regions, schedules)
- `kafka/config/topics.json`: Kafka topic definitions with retention and partitioning settings
- `kafka/.env.example`: Template for Kafka external deployment configuration

## Key Data Structures

### Ad Impression Log Schema
The CSV files contain these columns:
- `timestamp`: Ad broadcast time
- `channel_id`, `channel_name`: TV channel information
- `ad_id`, `ad_name`, `advertiser`: Advertisement details
- `duration`: Ad length in seconds
- `viewer_count`: Number of viewers
- `region`: Geographic region
- `device_type`: Viewing device (STB, Smart TV, Mobile, etc.)
- `ad_position`: pre-roll, mid-roll, or post-roll
- `campaign_id`: Marketing campaign identifier
- `revenue`: Revenue generated

### Kafka Topics
- `ad-impressions`: Raw IPTV ad log data (3 partitions, 7-day retention)
- `ad-analytics`: Processed analytical data (compact cleanup policy)
- `ad-alerts`: System alerts and errors (1-day retention)

## Volume Mounts and Data Directories

- `iptv-ad-log-generator/ad_logs/` → `/opt/nifi/nifi-current/data/input` (NiFi reads CSV files from here)
- `nifi/output/` → `/opt/nifi/nifi-current/data/output` (NiFi writes processed data here)

## External Deployment

For multi-server deployments, see `EXTERNAL_DEPLOYMENT_GUIDE.md` which covers:
- Kafka cluster on Server A (192.168.1.100)
- NiFi on Server B (192.168.1.200)
- Network configuration and firewall settings
- Cross-server connectivity testing

## Testing Data Pipeline

1. Generate test data: `cd iptv-ad-log-generator && python ad_log_generator.py --once --count 100`
2. Verify CSV creation in `iptv-ad-log-generator/ad_logs/`
3. Check NiFi UI for file processing
4. Monitor Kafka topics for ingested data
5. Verify output in `nifi/output/`

## Container Resource Limits

- **NiFi**: 4GB RAM limit, 2 CPU cores
- **Kafka**: 2GB RAM limit, 1.5 CPU cores
- **Schema Registry & Kafka Connect**: Included for advanced use cases