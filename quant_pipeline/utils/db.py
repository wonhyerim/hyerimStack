from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def create_db_engine(db_url: str) -> Engine:
    return create_engine(db_url, pool_pre_ping=True, pool_recycle=3600)


def ensure_intraday_table(engine: Engine, table_name: str = "intraday_bars") -> None:
    ddl = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
      `id` BIGINT NOT NULL AUTO_INCREMENT,
      `symbol` VARCHAR(16) NOT NULL,
      `ts` DATETIME NOT NULL,
      `open` DOUBLE NULL,
      `high` DOUBLE NULL,
      `low` DOUBLE NULL,
      `close` DOUBLE NULL,
      `volume` BIGINT NULL,
      `value` BIGINT NULL,
      `foreign_value` BIGINT NULL,
      `inst_value` BIGINT NULL,
      `foreign_volume` BIGINT NULL,
      `inst_volume` BIGINT NULL,
      `foreign_net` BIGINT NULL,
      `inst_net` BIGINT NULL,
      PRIMARY KEY (`id`),
      KEY `idx_symbol_ts` (`symbol`, `ts`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))