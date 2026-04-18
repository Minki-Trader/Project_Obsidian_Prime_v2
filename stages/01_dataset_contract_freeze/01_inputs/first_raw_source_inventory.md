# First Raw Source Inventory

## Purpose

This note records the first materialized raw `M5` source exports that support `Stage 01_dataset_contract_freeze`.

The exports remain raw source evidence only. They do not imply dataset-contract closure, parser closure, runtime parity closure, or operating promotion.

## Export Window

- requested_from_utc: `2022-08-01T00:00:00Z`
- requested_to_utc: `2026-04-13T23:55:00Z`
- exporter: `foundation/collectors/export_fpmarkets_v2_mt5_bars.py`
- local output root: `data/raw/mt5_bars/m5/`
- time basis: `MT5_PY_API_UNIX_SECONDS`
- timezone status: `UNRESOLVED_REQUIRES_MANUAL_BINDING`

## Symbol Mapping Note

- `US100`, `VIX`, `US10YR`, and `USDX` exported directly under their broker-native names
- equity contracts `NVDA`, `AAPL`, `MSFT`, `AMZN`, `AMD`, `META`, and `TSLA` were exported from broker-native `.xnas` symbols
- `GOOGL.xnas` remains the contract Google symbol

## Materialized Raw Source Identities

| Contract symbol | Broker symbol | Rows | First open unix | Last open unix | CSV path | CSV sha256 | Manifest path | Manifest sha256 |
|---|---:|---:|---:|---:|---|---|---|---|
| `US100` | `US100` | `261345` | `1659315600` | `1776124500` | `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv` | `2ab1cb8214182ff9063a64c10ce4ac6a142a8bf660e2476a60842d3452c6d784` | `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.manifest.json` | `86a772a2b73dc2d7684f37ba41243596bad54749ef1461db17c6957600787cde` |
| `VIX` | `VIX` | `158415` | `1659315600` | `1776124500` | `data/raw/mt5_bars/m5/VIX/bars_vix_m5_mt5api_raw.csv` | `29b0ea35acba3da3dc50cc1a42034d782949c9ee42494387d9be21fa731db9b2` | `data/raw/mt5_bars/m5/VIX/bars_vix_m5_mt5api_raw.manifest.json` | `0d4e2d8dc90e3ee32e12061e10f3446ca4d05f46b314ae380e8c6e23e478511a` |
| `US10YR` | `US10YR` | `223363` | `1659315600` | `1776124500` | `data/raw/mt5_bars/m5/US10YR/bars_us10yr_m5_mt5api_raw.csv` | `3628169dbede3f1dc8ddea5c32b34872fb9d70addb961c7a04a121c93c2f72cb` | `data/raw/mt5_bars/m5/US10YR/bars_us10yr_m5_mt5api_raw.manifest.json` | `e7f33a4f15aa3c7c17cd00d19d88b4ae01c68089cc23970b28548a83833b85f3` |
| `USDX` | `USDX` | `238993` | `1659322800` | `1776124500` | `data/raw/mt5_bars/m5/USDX/bars_usdx_m5_mt5api_raw.csv` | `9646370bfe9915aff915011f736e9a35177b81703e8a626b6dd77a5f14ecb0c3` | `data/raw/mt5_bars/m5/USDX/bars_usdx_m5_mt5api_raw.manifest.json` | `d31b8611a443c0ac859179d1d2bfd30f97c2198e4ede5b95be9716cc30e542bf` |
| `NVDA` | `NVDA.xnas` | `71046` | `1659371700` | `1776120900` | `data/raw/mt5_bars/m5/NVDA/bars_nvda_xnas_m5_mt5api_raw.csv` | `0ca43d90e41e727a65937f1bf0def6e8721cd7894c02b6b7a718f26d03a0f251` | `data/raw/mt5_bars/m5/NVDA/bars_nvda_xnas_m5_mt5api_raw.manifest.json` | `c93bd064196220df4beda11de234fd207320ec52ed4f30b6ee4322e5d5263de1` |
| `AAPL` | `AAPL.xnas` | `71935` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/AAPL/bars_aapl_xnas_m5_mt5api_raw.csv` | `00145aae5d2528c3b1c7f5444080d4a0dd6002a5992509dcea977bb1cafe8763` | `data/raw/mt5_bars/m5/AAPL/bars_aapl_xnas_m5_mt5api_raw.manifest.json` | `57d4aab69f003cb6f9e29abc15bb8822c671a6ed703bb139a946d75e486b03ea` |
| `MSFT` | `MSFT.xnas` | `71910` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/MSFT/bars_msft_xnas_m5_mt5api_raw.csv` | `6bc740c555671ad800456cc654a1b7815c7ed3d9b25de85a1b1e3cdd9d9b39a5` | `data/raw/mt5_bars/m5/MSFT/bars_msft_xnas_m5_mt5api_raw.manifest.json` | `a67c6ea4105313232f90743e6842446ed49d2d61cbcf927da4163a8c80fda44b` |
| `AMZN` | `AMZN.xnas` | `71933` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/AMZN/bars_amzn_xnas_m5_mt5api_raw.csv` | `71f26096cff63480265b2a37ca2a234881bb22f9b729099a36a66af7991abc5d` | `data/raw/mt5_bars/m5/AMZN/bars_amzn_xnas_m5_mt5api_raw.manifest.json` | `2c0c1e233fcb028085757ec5263871d15deecb264c20a451cbb934fdc31eaee1` |
| `AMD` | `AMD.xnas` | `71932` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/AMD/bars_amd_xnas_m5_mt5api_raw.csv` | `66c2c1f3210628a65429fd0dab97d4f8f153f2f52265ae4dd5db3d17a26197f2` | `data/raw/mt5_bars/m5/AMD/bars_amd_xnas_m5_mt5api_raw.manifest.json` | `0772dd402f3a4868d271710f90ea139ccb8bc5c26d0e4ef8ca27bc919f97d589` |
| `GOOGL.xnas` | `GOOGL.xnas` | `71917` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/GOOGL.xnas/bars_googl_xnas_m5_mt5api_raw.csv` | `f2df284fd4947afb6b8f7165c1a4b8652c05a555e0d52ba7217c896d1abfbf09` | `data/raw/mt5_bars/m5/GOOGL.xnas/bars_googl_xnas_m5_mt5api_raw.manifest.json` | `496fdbf91a1e7481669053d407067fa9e9f3123e4ee2b24cf8ead5626c43f742` |
| `META` | `META.xnas` | `71916` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/META/bars_meta_xnas_m5_mt5api_raw.csv` | `90bf2e0abfb76f939643f604c973c51ce4f73b8c45b16dc0fb570fc2ed16336e` | `data/raw/mt5_bars/m5/META/bars_meta_xnas_m5_mt5api_raw.manifest.json` | `0f6fb9911dd9d61cfd3395bf1ec89cf3d0d972daba9cd37de0acd333acc18363` |
| `TSLA` | `TSLA.xnas` | `71916` | `1659371400` | `1776120900` | `data/raw/mt5_bars/m5/TSLA/bars_tsla_xnas_m5_mt5api_raw.csv` | `93a8c1a64477e37724cc6e278aa73af52212a4001961fbbf8307aaf67eee98c7` | `data/raw/mt5_bars/m5/TSLA/bars_tsla_xnas_m5_mt5api_raw.manifest.json` | `d52015d56b3df2d1afeb4d958f2b4e7093064f8f2f0244d9481575efeb3c475b` |

## Operational Meaning

- the first raw source roots now exist inside the v2 workspace under `data/raw/mt5_bars/m5/`
- this inventory satisfies raw-source identity capture for Stage 01
- this inventory does not satisfy the remaining Stage 01 requirements for `row summary`, `invalid_reason_breakdown`, or processed dataset output hashes
