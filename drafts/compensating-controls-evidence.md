# Compensating controls: market evidence audit

Research date: 2026-07-13

Question: Is there evidence from both buyers and sellers of advertising that they want a product shaped like a shared, auditable record joining delivery to a verified commercial outcome?

## Result

The evidence supports a narrower claim than the draft originally made.

There is strong market-level demand for *closed-loop, comparable, auditable measurement* and direct occupational evidence that advertisers are assembling exposure, purchase, lineage, and reconciliation systems internally. There is also direct supply-side evidence that retail media networks commercialize closed-loop measurement as a product and hire teams to build trusted, deterministic measurement from first-party transaction data.

The evidence does not show buyers asking for a cryptographic coupon, public ledger, or one universal source of truth. In fact, the 2026 CIMM/4As study explicitly says advertisers do not want one source of truth; they want the relationships among different records to be explainable and verifiable. The evidence validates the interface—verified exposure, verified sale, stable joining, traceability, reconciliation—not the proposed implementation.

## Market-level demand

### CIMM/4As, *The Paradox of Plenty* (March 2026)

Primary source: https://cimm-us.org/wp-content/uploads/2026/03/CIMM-4As-Advertisers-Perspectives-on-the-State-of-Measurement-Full-Report-March-2026.pdf

Sample: 197 brand-side marketers, all director level or above, all with more than eight years' experience, at B2C advertisers with annual US marketing budgets above $50 million; plus 16 executive interviews. Agencies were excluded (p. 4).

Findings relevant to the thesis:

- Attribution depends on stitched data, model assumptions, and platform-reported signals that are rarely transparent or independently validated (p. 28).
- A tech executive described reconciling and triangulating multiple sources as daily manual work (p. 17).
- A retail executive said each partner brings its own identity backbone and measurement proof, producing four or five versions of ROAS (p. 29).
- Respondents were most confident when metrics were direct, observable, and organizationally validated; confidence fell when systems had to be joined or outputs reconciled (p. 10).
- The study recommends transparency and auditability of models, including disclosed inputs, assumptions, methodology, and identity-stitching logic (p. 39).
- Important counterevidence: the report says advertisers are *not* seeking one source of truth. They want clarity about how different truths relate, and systems that make results easier to explain and validate (p. 11).

Assessment: strong evidence for the reconciliation and auditability problem across large advertisers. It supports interoperable counterparty records. It contradicts language promising one canonical truth for every measurement question.

### IAB/MRC retail-media buyer study (2023)

Primary source: https://www.iab.com/news/iab-and-mrc-releases-retail-media-measurement-guidelines/

Sample: 200 retail-media buyers at brands and agencies spending at least $5 million annually, plus more than 30 senior interviews across retailers, brands, agencies, DSPs, SSPs, and data providers.

Findings:

- Improving measurement and data collection was buyers' number-one opportunity area.
- 62% cited lack of measurement standards as a top growth challenge.
- Nearly 60% wanted greater transparency.
- The IAB concluded that cross-network standards and transparency around attribution windows, incrementality, and viewability would propel spend.

Assessment: market-level evidence that measurement comparability and transparency constrain budget allocation. It does not isolate demand for settlement receipts.

## Demand-side occupational evidence

### Keurig Dr Pepper — Media Measurement Manager

Primary employer page: https://careers.keurigdrpepper.com/es/trabajo/frisco/media-measurement-manager/42849/93272582624

Title and compensation: Media Measurement Manager, $96,800–$143,000.

Specification:

- Newly established measurement team.
- Three pillars kept distinct: closed-loop attribution, causal lift, and ROMI/MMM.
- Exact attribution rule: “verified exposure + verified sale = attributed sale,” with fair-share credit and no multi-touch modeling.
- Harmonize verified exposures and purchases from Circana, Walmart, Kroger, Amazon, KDP, Fetch, and Ibotta.
- Enforce taxonomy standards, lineage documentation, and QA.
- Reconcile inventory, spend, and outcome signals.
- Maintain freshness, accuracy, and traceability.

Assessment: strongest demand-side evidence. This is almost exactly the proposed product interface, expressed as a salaried internal operation. It also cleanly separates accounting-style attribution from causal testing.

### Conagra Brands — Director, Marketing Measurement Insights & Analytics

Primary employer page: https://conagrabrands.wd1.myworkdayjobs.com/en-US/Careers_US/job/Director--Marketing-Measurement-Insights---Analytics_Req-037354

Title and compensation: Director, Marketing Measurement Insights & Analytics, $133,000–$197,000.

Specification:

- Build an end-to-end media data ecosystem with Data Science and Engineering.
- Enable a single source of truth and partner with Business Intelligence and Finance.
- Move from vendor-led measurement toward in-house or hybrid capabilities.
- Govern MMM, incrementality, attribution, experimentation, and reporting.

Assessment: supports internalization and cross-functional demand, but is less specific to a counterparty receipt. Much of the job concerns causal modeling and management reporting.

### Beam — Head of Marketing Intelligence

Corroborated listing: https://www.ziprecruiter.com/c/Beam/Job/Head-of-Marketing-Intelligence/-in-New-York%2CNY?jid=8e2cac7b68d8beba

Specification:

- Own the measurement ecosystem as the “ultimate arbiter of truth.”
- Join DTC media to Amazon and physical-retail outcomes.
- Use clean rooms to connect exposure to marketplace conversions.
- Bridge Data, Finance, and Growth.

Assessment: supports the organizational diagnosis and cross-boundary join problem. It asks for a mix of MMM, MTA, causal inference, and dashboards, not a settlement record specifically. Secondary host, so weaker provenance than KDP and Conagra.

## Supply-side occupational and product evidence

### Walmart Connect — Director, Data, Identity & Measurement Product Marketing

Primary employer page: https://careers.walmart.com/us/en/jobs/R-2517683

Title and compensation: Director, Product Marketing, Data, Identity & Measurement, $132,000–$286,000 depending on location.

Specification:

- Commercialize first-party activation, identity, attribution, incrementality, clean rooms, and measurement.
- Drive advertiser adoption and utilization.
- Show advertisers how media investment translates into business outcomes.

Assessment: direct evidence that the supply side treats closed-loop measurement as a revenue-bearing product, not merely internal plumbing.

### Sam's Club MAP — Senior Manager, Performance Measurement & Insights

Primary employer page: https://careers.walmart.com/us/en/jobs/R-2392003

Title and compensation: Senior Manager, Data Analytics — MAP Performance Measurement and Insights, $90,000–$234,000 depending on location.

Specification:

- Use first-party deterministic membership data to provide trusted advertiser measurement.
- Build transparent, reliable, decision-ready measurement products.
- Connect standardized metrics, pipelines, and validation controls.

Related supply proof: Walmart advertises closed-loop measurement directly in a Senior Partner sales role: https://careers.walmart.com/us/en/jobs/R-2379610

Assessment: strong evidence of solution supply. It also reveals the boundary: the loop closes because Walmart controls both the exposure ledger and purchase ledger. This is a walled-garden solution, not independent counterparty evidence.

### Appodeal — Financial Data Analyst

Listing with full employer-authored text: https://www.linkedin.com/jobs/view/financial-data-analyst-at-appodeal-inc-4401323962

Specification:

- Reconcile partner-reported revenue across SSPs, DSPs, and exchanges.
- Replace ad hoc fixes with repeatable reconciliation frameworks.
- Maintain a financial system of record with mapping and lineage.
- Make data auditable and traceable from source to reporting.

Assessment: direct sell-side evidence of the accounting defect, but it concerns revenue reconciliation across ad-market counterparties rather than advertiser conversion attribution.

### Accenture — Retail Media Product Manager

Full listing: https://www.linkedin.com/jobs/view/retail-media-product-manager-at-accenture-4360971357

Specification:

- Define products across proposal, order management, trafficking, serving, measurement, billing, and reconciliation.
- Partner with sales operations, ad operations, finance, and technology.
- Produce scalable, auditable, commercially sound systems.
- Advise retail-media clients on build versus buy versus partner.

Assessment: unusually explicit evidence that sellers see the entire order-to-reconciliation chain as one product surface. As a consultancy role, it is indirect evidence aggregated across clients.

## What the market has actually validated

The recurring specification is:

1. A verifiable exposure or delivery event.
2. A verified purchase or settled outcome.
3. A stable way to join the two.
4. Explicit allocation rules.
5. Lineage from event to report.
6. Reconciliation across partner, operational, and financial records.
7. Separate experiments for causal lift.

Retail media supplies this bundle where one firm owns exposure identity and purchase identity. Open-web advertisers hire teams and vendors to reconstruct it across organizational boundaries. That contrast supports a more precise diagnosis: *the market has validated closed-loop measurement; what remains missing is a neutral closed loop that crosses counterparties without requiring either common ownership or shared identity.*

## Remaining falsifiers and research gaps

- No evidence yet that advertisers will pay specifically for independent or cryptographic settlement rather than accept retailer/platform first-party measurement.
- No evidence yet that publishers will accept outcome-based settlement at terms attractive to advertisers.
- No quantified total addressable market for reconciliation labor; job postings show existence, not prevalence.
- Current job postings are a convenience sample and cannot establish hiring frequency without a reproducible corpus and denominator.
- Retail media may be a substitute that weakens the neutral-ledger thesis: advertisers may prefer vertically integrated measurement despite its conflict of interest because it is operationally convenient.
- The strongest next test is buyer discovery with people holding the observed titles: Media Measurement Manager, Director of Marketing Measurement, Retail Media Product Manager, and advertising-finance/revenue-operations roles.

## Round two: inbound-specific evidence

Research scope: paid search, paid social, B2B SaaS demand generation, consumer acquisition, lead generation, and supplier products connecting ads to CRM, billing, calls, or transactions. Retail-media roles were excluded from this round. Searches were purposive rather than exhaustive, so the results establish existence and repeated specification, not prevalence.

### Strong demand-side matches

#### Tradeify — Marketing Data Engineering Lead

Primary employer posting: https://jobs.ashbyhq.com/tradeify/ad7d2d2d-de25-4a21-aa76-403e21576799

Compensation: US $100,000–$120,000; Canada CA$136,000–CA$163,000.

The role owns a warehouse-first system joining Google and Meta spend, GA4 behavior, product events, and checkout transactions. Its required controls include identity stitching, event taxonomies, stable conversion definitions, revenue-event standards for purchases, refunds, and chargebacks, server-side ingestion, deduplication, idempotency, automated monitoring, and explicit data contracts.

Assessment: the strongest evidence for demand for analysis-ready rows rather than dashboards. It asks for most of the data-engineering substrate required by advertising science. It still relies on platform-supplied exposure and click records.

#### Standard Bots — Performance Marketing Lead

Primary employer posting: https://jobs.ashbyhq.com/standardbots/ae201278-1885-492d-b907-a9c810645e01

The role owns paid search and paid social plus the integration among advertising platforms, HubSpot, and analytics. The posting explicitly says conversion signals should train platforms on real business outcomes rather than form fills, and the measured funnel should run from impression to closed-won.

Assessment: direct evidence that an inbound buyer distinguishes instrument events from business outcomes and wants the latter joined to acquisition data. Its immediate use is optimization, not reproducible causal research.

#### Viktor — Founding Head of Search Acquisition

Primary employer posting: https://jobs.ashbyhq.com/viktor/5956d1bf-9159-4fc9-9a02-a710c334b84b

The role requires offline conversion uploads tied to closed-won rather than lead volume, raw-data access through SQL, and accountability for SQL pipeline and closed-won outcomes rather than clicks.

Assessment: exceptionally direct paid-search evidence that proxy conversions are considered inadequate. It asks for better outcome labels, but not lineage or experimental controls.

#### Katana — Senior Acquisition Manager

Primary employer posting: https://jobs.ashbyhq.com/katana/51b7810d-d7ab-4ee2-b25e-923271f75f1a

The role covers Google, LinkedIn, Meta, and Reddit. It must connect low-level attribution events to SQL and closed-won records to determine which programs are real, and connect acquisition activity to revenue rather than proxy metrics.

Assessment: direct multi-channel B2B evidence for joined downstream outcomes. The language is decision-oriented rather than method-oriented.

#### 1Password — Senior SEM Manager

Primary employer posting: https://jobs.ashbyhq.com/1password/e02238ae-1bb1-41d2-9c9c-14b38f8d38fa

The role requires accurate attribution across both product-led trial-to-paid and sales-led MQL-to-opportunity-to-closed-won funnels, Salesforce-integrated reporting, LTV signals, and a continuous experimentation program.

Assessment: useful evidence that the demand spans both direct checkout and long B2B sales cycles.

#### Upside — Senior Marketing Analytics Manager

Primary employer posting: https://jobs.ashbyhq.com/upside/59da723c-f8b9-4463-8808-6f957154bb78

Compensation: $145,000–$165,000.

The role must improve upstream event tracking, attribution signals, identity stitching, and channel taxonomies; interpret attribution, MMM, and incrementality together; and run A/B, multivariate, and lift tests with statistical rigor across paid social, paid search, and app acquisition.

Assessment: strong evidence for the combined data-and-method specification. Unlike several acquisition roles, it explicitly asks for trustworthy upstream assets as well as experiments.

#### Orbital — Revenue Operations Manager, Marketing

Primary employer posting: https://jobs.ashbyhq.com/orbital/eea32313-5bba-4652-a293-db25b83a6376

Compensation: US $150,000–$165,000; UK £90,000–£110,000.

The role owns UTM standards, source tracking, campaign attribution, enrichment and deduplication, and reporting from traffic through lead, MQL, SQL, opportunity, and closed-won. The stated output is reliable, well-instrumented data for marketing investment decisions.

Assessment: corroborates the operational market around maintaining the joins. It is less scientifically explicit than Tradeify or Upside.

### Supply-side matches

#### Attribution — raw marketing-data export

Primary product page: https://www.attributionapp.com/data-export-tool/

The product exports nine SQL-queryable raw tables covering timestamped events, visits, identity-resolved visitors, internal user IDs, ad costs, UTM parameters, and channel definitions, with no attribution model pre-applied. It advertises joins to Stripe billing and Salesforce CRM, custom modeling, geo holdouts, synthetic controls, and financial reconciliation.

Assessment: the closest solution-shaped commercial product found in this round. Its value proposition is precisely that the customer receives inputs and can recompute the analysis. Vendor claims still need customer validation, pricing, and adoption evidence.

#### Call-tracking suppliers

Primary examples:

- CallRail: https://www.callrail.com/
- Nimbata: https://www.nimbata.com/call-tracking
- LeadCall: https://www.leadcall.tech/

These products capture ad-originated phone events, join them to campaigns, qualify whether calls are actual leads, sync them into CRM, and in some cases connect closed-deal revenue back to the campaign. Their product language explicitly contrasts calls, qualified leads, and revenue with clicks or unqualified form fills.

Assessment: a mature solution-shaped category for one important inbound outcome. Call capture is observable, but lead-quality labels may be manual or model-generated, and causal exposure remains unresolved.

#### LeadMetrics

Primary product page: https://www.lead-metrics.com/

The product displays the entire progression from ad to lead, qualification, call, proposal, close, and revenue and uses CRM signals to optimize advertising toward purchase-ready leads.

Assessment: direct commercial supply matching the B2B demand-side postings. The page emphasizes feeding algorithms and multi-touch attribution, not raw-data reproducibility.

### What this round changes

The inbound-specific evidence supports a stronger existence claim than the first round:

*Across paid search, paid social, SaaS, ecommerce, and lead generation, employers repeatedly ask for acquisition events joined to qualified, closed, paid, refunded, or charged-back outcomes. The most technically explicit roles also ask for identity rules, event taxonomies, stable definitions, deduplication, idempotency, monitoring, and experimental rigor. Suppliers sell raw event exports, CRM-to-revenue attribution, offline conversion plumbing, and call-to-revenue joins.*

This is evidence that the market asks for higher-quality inputs to advertising science. It is not yet evidence that the inputs are sufficient for advertising science.

The remaining defect is now sharper: most systems improve the *outcome label* and the *join*, but leave the treatment record under platform control. A click ID proves a click was assigned an identifier; it does not provide a complete exposure log, randomized assignment record, non-exposure population, or contamination audit. Most demand-side postings also send improved labels back into platform optimizers. Only the warehouse-first and raw-export examples clearly demand a recomputable dataset outside the reporting interface.

### Revised evidentiary status

- Demand for downstream business outcomes instead of proxy conversions: strongly supported by repeated current postings across inbound categories.
- Demand for stable joins, definitions, and data-quality controls: supported by several technically explicit roles.
- Demand for experiment-ready data and causal rigor: supported, but less broadly; strongest in KDP, Upside, and dedicated marketing-science roles.
- Commercial supply of the outcome and join layer: supported by attribution, offline-conversion, and call-tracking products.
- Availability of complete, independently recomputable treatment and outcome data: not established and likely absent in the dominant paid platforms.
- Market prevalence and willingness to pay: not established by this convenience sample.
