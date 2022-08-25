-- Init tables required.

CREATE TABLE monthly_share_prices (
    date date,
    symbol text,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    dividends double precision,
    stock_splits double precision
);

CREATE UNIQUE INDEX unique_monthly_share_prices ON monthly_share_prices (date, symbol);