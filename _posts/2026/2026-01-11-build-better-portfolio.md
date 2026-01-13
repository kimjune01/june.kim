---
layout: post
title: AI Engineering at BuildBetter.ai
tags: coding
---

As an AI Engineer at BuildBetter, I worked on integrations, sync infrastructure, CI/CD tooling, and internal developer workflows. BuildBetter is a customer intelligence platform that ingests company data (calls, recordings, interviews, feedback) and turns it into actionable product-ops signals.

---

## Impact

- **844+ commits** to the main repository
- **Expanded data connectivity** by building 4 third-party integrations, enabling customers to import data from additional platforms
- **Reduced manual work** for data imports with AI-powered field classification that automatically maps columns
- **Improved engineering velocity** through Claude Code skills and slash commands used daily by the team
- **Increased CI reliability** by enabling previously-skipped E2E tests and adding automated code review checks
- **Established integration standards** with documentation and checklists that streamlined future integration development

---

## Areas of Contribution

| Area | Summary |
|------|---------|
| **Integrations** | Built 4 third-party integrations (Circle, Notion, Front, Attio) + fixes for existing ones |
| **AI Features** | Built draft iteration of Custom AI Agents feature, AI-powered field classification for imports |
| **Developer Tooling** | Created Claude Code skills and slash commands for the engineering team |
| **CI/CD & Testing** | Automated code review checks, E2E testing infrastructure, quality gates |
| **Infrastructure** | Queue reliability improvements, monitoring, database migration work |
| **Documentation** | Integration pattern guides, acceptance criteria, tech stack standards |

---

## Third-Party Integrations

I built several integrations following OAuth2 and incremental sync patterns, enabling customers to automatically import and analyze data from their existing tools.

### Circle.so Integration

Built a complete integration for community platform data.

**Challenges solved:**
- Worked around API limitations that didn't support date filtering by implementing client-side early termination optimization
- Implemented per-space incremental sync with database-backed cursor tracking (unlike single-cursor integrations)
- Added cancellation checkpoints for graceful shutdown without losing progress
- Implemented flexible backfill options (none, time windows, or full history)

### Notion Integration

Built OAuth2 integration for importing Notion workspace pages as searchable documents.

**Features:**
- OAuth2 flow with automatic token refresh
- Incremental sync that skips unchanged pages
- Title extraction handling various Notion page structures
- Duplicate detection for workspace re-authentication
- Settings UI for workspace management and import toggles

### Front Integration

Built the Front (customer communication platform) integration from scratch.

**Features:**
- Full OAuth2 implementation with token refresh
- Conversation sync with message threading
- Correct author attribution for inbound vs outbound messages
- Incremental sync using timestamp-based filtering

### Attio Integration

Built CRM sync for importing contacts and companies.

**Features:**
- Sync service with pagination
- Error handling with comprehensive test coverage
- Author resolution with fallback chain

### Integration Fixes

- **Gong:** Fixed category filter that incorrectly rejected calls without optional metadata fields
- **HubSpot & Zendesk:** Fixed ticket sync to handle tickets without authors gracefully

---

## AI Features

### Custom AI Agents (Draft Iteration)

Built an early draft iteration of the Custom AI Agents feature, which enables AI-powered conversations for analyzing customer signals. This exploratory work helped inform the direction of the feature before it was rebuilt by another engineer.

### AI-Powered Field Classification

Built an LLM-powered system for automatically classifying and mapping fields during data imports.

**Features:**
- Analyzes column names and sample data to determine field types
- Matches against existing organization fields for consistent naming
- Returns confidence scores for each classification
- Fallback UX for edge cases where AI classification is uncertain
- Auto-accept for high-confidence mappings

**UI/UX work:**
- Column name truncation for long headers
- Sample row preview
- Persisted user mappings through async processing

---

## Developer Tooling

Created tools and documentation to standardize how the engineering team builds features and debugs issues.

### Claude Code Skills

Built reusable AI-powered development tools:

- Development environment startup
- CloudWatch log querying for staging/production
- Database querying via GraphQL
- Migration generation
- REST endpoint scaffolding
- Permission configuration
- Circular dependency diagnosis
- Admin UI scaffolding
- CI failure analysis

### Slash Commands

Created workflow automation commands including:

- **Integration planning** - Interactive command that researches provider APIs and generates planning documents with authentication strategy, entity mappings, sync strategy, and implementation checklists
- **Implementation planning** - Research-driven planning workflows
- **Feature specifications** - Spec documents with user journeys
- **Error review** - Periodic error analysis and recommendations

### Integration Pattern Documentation

Created documentation for building integrations:
- Architecture patterns and tech stack requirements
- Implementation checklists covering infrastructure, migrations, services, workers, and frontend
- Acceptance criteria standards with unit test and telemetry requirements

---

## CI/CD & Testing

### Automated Code Review

Analyzed historical PRs to extract actionable heuristics that run automatically in CI:

- Architecture migration rules (ORM migration, API patterns)
- Type safety rules
- Security checks (permissions, authentication)

**Benefits:**
- Instant feedback without LLM latency for obvious issues
- Consistent enforcement of codebase standards
- Reduced review cycles

### E2E Testing Infrastructure

Built infrastructure to run previously-skipped E2E tests in CI:

- Testcontainers pattern for database isolation
- Dynamic test context (no hardcoded IDs)
- Proper external service mocking
- Dedicated E2E configuration and CI job

### Additional CI Improvements

- Pre-flight validation before expensive tests
- Timeout and concurrency controls
- Job summaries and annotations
- Draft PR skipping
- Quality gates for architecture patterns

### Test Coverage

Added unit tests for integrations including error handling, sync services, and auth decorators.

---

## Infrastructure Work

### Queue Reliability

- Built monitoring for failed message detection with appropriate alert thresholds
- Improved visibility management with graceful handling of expired messages
- Structured logging with job context for debugging

### Database Migration

- Contributed to ORM migration initiative with integration tests
- Extracted database queries to repositories for testability
- Type-safe SQL expressions

### Observability

- Improved telemetry consistency across services
- Added error tracking for previously unmonitored failures
- Structured error logging

---

## Technologies Used

- **Languages:** TypeScript
- **Frameworks:** NestJS
- **Databases:** PostgreSQL, Kysely
- **Message Queues:** AWS SQS
- **Infrastructure:** AWS CloudWatch
- **Testing:** Jest, Testcontainers
- **CI/CD:** GitHub Actions

---
