from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    model = Column(String)
    status = Column(String, default="active")
    endpoint = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    signals = relationship("TradeSignal", back_populates="agent")

class TradeSignal(Base):
    __tablename__ = "trade_signals"

    signal_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    symbol = Column(String, index=True)
    timeframe = Column(String)
    agent_id = Column(Integer, ForeignKey("agents.agent_id"))
    signal_type = Column(String)  # BUY, SELL, HOLD
    confidence = Column(Float)
    signal_data = Column(JSON)
    macro_context = Column(JSON)
    processed = Column(Boolean, default=False)

    # Relationships
    agent = relationship("Agent", back_populates="signals")
    outcome = relationship("TradeOutcome", back_populates="signal", uselist=False)

class TradeOutcome(Base):
    __tablename__ = "trade_outcomes"

    outcome_id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("trade_signals.signal_id"), unique=True)
    entry_price = Column(Float)
    exit_price = Column(Float)
    entry_time = Column(DateTime(timezone=True))
    exit_time = Column(DateTime(timezone=True))
    pnl = Column(Float)
    pnl_percentage = Column(Float)
    success_flag = Column(Boolean)
    notes = Column(Text)

    # Relationships
    signal = relationship("TradeSignal", back_populates="outcome")

class MacroEvent(Base):
    __tablename__ = "macro_events"

    event_id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("trade_signals.signal_id"))
    event_name = Column(String)
    event_type = Column(String)  # NEWS, ECONOMIC, EARNINGS, etc.
    impact_score = Column(Float)
    forecast_bias = Column(String)  # BULLISH, BEARISH, NEUTRAL
    source = Column(String)
    event_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AgentPerformance(Base):
    __tablename__ = "agent_performance"

    performance_id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.agent_id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    total_signals = Column(Integer, default=0)
    successful_signals = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    avg_confidence = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
