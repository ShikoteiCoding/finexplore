# Earning Strategy

Standalone root folder for exploration purposes. Once the protocol have been tested and results are obtained, this folder might be moved to a distinct repository (will need to finish the bot package grr...).
If results are not considered good enough to continue, results will be added below.

# Improvement points

1. Switch to SQL storing

Motivation is that pandas is not flexible enough and complex queries feel unnatural to implement with this index paradagm.
Let's switch to a postgres database and add some SQL Mapper to make the translation.

2. Finish the first protocol

**Hypothesis** - Stocks goes up after a positive earning report (with different stock behavior in the preceding days)

**Definition** - Positive earning indicates that the report is better than expected. Negative earning indicates that the report is less than expected.

**Protocol** - Select some companies and their previous earning dates. Compute the trailing tendency for each earnings. Take the few minutes of opening following the report (Can be next day, current day or after week end / off day. This one might be tricky to do properly). Confirm the upward trend following positive earnigns and the (either volatile or downward trend) following negative earnings.

3. Scale up the protocol if hypothesis is confirmed.

# TODO
1. Add upsert metadata (no information)
2. Link ingestions (need to find a solution - they have a DAG dependency)
3. Deal with timezones for utc / market data. Find a market calendar datasource.
4. Build views in protocol