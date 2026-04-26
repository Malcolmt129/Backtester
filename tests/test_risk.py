import pytest

from src.backtester.risk import (
    Account,
    calculate_total_capital,
    calculate_annualized_cash_vol_target,
)


def test_total_capital_sums_multiple_accounts():
    accounts = [Account(cash=10000, positions=[]), Account(cash=20000, positions=[]), Account(cash=5000, positions=[])]
    assert calculate_total_capital(accounts) == 35000


def test_total_capital_single_account():
    assert calculate_total_capital([Account(cash=50000, positions=[])]) == 50000


def test_total_capital_empty_list():
    assert calculate_total_capital([]) == 0


def test_annualized_cash_vol_target():
    # config/dev.toml has cash_vol_pct = 25
    assert calculate_annualized_cash_vol_target(100000) == pytest.approx(25000.0)


def test_annualized_cash_vol_target_scales_with_capital():
   assert calculate_annualized_cash_vol_target(200000) == pytest.approx(50000.0)
