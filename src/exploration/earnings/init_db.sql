-- Init tables required.

CREATE TABLE tickers_monthly_share_prices (
    date timestamp without time zone,
    symbol text,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    dividends double precision,
    stock_splits double precision
);

CREATE UNIQUE INDEX unique_tickers_monthly_share_prices ON tickers_monthly_share_prices (date, symbol);

CREATE TABLE tickers_earnings_history (
    earnings_date timestamp without time zone,
    symbol text,
    company text,
    eps_estimates double precision,
    eps_reported double precision,
    surprise_percent double precision
);

CREATE UNIQUE INDEX unique_tickers_earnings_history ON tickers_earnings_history (earnings_date, symbol);

CREATE TABLE snp_constituents (
    symbol text,
    company text,
    sector text
);

CREATE TABLE tickers_daily_share_prices (
    date timestamp without time zone,
    symbol text,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    dividends double precision,
    stock_splits double precision
);

CREATE UNIQUE INDEX unique_tickers_daily_share_prices ON tickers_daily_share_prices (date, symbol);