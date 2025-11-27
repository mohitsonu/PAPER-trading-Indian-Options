#!/usr/bin/env python3
"""
📊 VISUAL TRADING REPORT GENERATOR
Generates a comprehensive HTML dashboard with interactive charts and advanced metrics.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
from datetime import datetime
import numpy as np
import os

def generate_report():
    print("🚀 GENERATING VISUAL TRADING REPORT")
    print("=" * 60)

    # 1. Load Data
    csv_files = glob.glob("high_accuracy_trades_*.csv")
    csv_files.sort()
    
    if not csv_files:
        print("❌ No trade files found!")
        return

    all_trades = []
    
    print(f"📂 Found {len(csv_files)} daily files")
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            # Filter for EXIT trades only for P&L analysis
            exits = df[df['action'] == 'EXIT'].copy()
            
            # Standardize P&L column
            if 'net_pnl_after_charges' in exits.columns:
                exits['pnl'] = exits['net_pnl_after_charges']
            elif 'pnl_after_charges' in exits.columns:
                exits['pnl'] = exits['pnl_after_charges']
            elif 'gross_pnl' in exits.columns:
                exits['pnl'] = exits['gross_pnl'] - 40 # Estimate
            else:
                continue
                
            # Add date from filename if timestamp missing or parse timestamp
            date_str = file.replace("high_accuracy_trades_", "").replace(".csv", "")
            exits['date'] = pd.to_datetime(exits['timestamp'])
            
            all_trades.append(exits)
            
        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")

    if not all_trades:
        print("❌ No valid trades found.")
        return

    # Combine all trades
    full_df = pd.concat(all_trades, ignore_index=True)
    full_df = full_df.sort_values('timestamp')
    
    print(f"✅ Loaded {len(full_df)} total trades")

    # 2. Calculate Metrics
    
    # Win Rate
    wins = full_df[full_df['pnl'] > 0]
    losses = full_df[full_df['pnl'] <= 0]
    win_rate = len(wins) / len(full_df) * 100
    
    # P&L Stats
    total_pnl = full_df['pnl'].sum()
    avg_win = wins['pnl'].mean() if not wins.empty else 0
    avg_loss = losses['pnl'].mean() if not losses.empty else 0
    largest_win = full_df['pnl'].max()
    largest_loss = full_df['pnl'].min()
    
    # Profit Factor
    gross_profit = wins['pnl'].sum()
    gross_loss = abs(losses['pnl'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    # Expectancy
    expectancy = (win_rate/100 * avg_win) + ((1 - win_rate/100) * avg_loss)
    
    # Drawdown
    full_df['cumulative_pnl'] = full_df['pnl'].cumsum()
    full_df['peak'] = full_df['cumulative_pnl'].cummax()
    full_df['drawdown'] = full_df['cumulative_pnl'] - full_df['peak']
    max_drawdown = full_df['drawdown'].min()
    
    # Sharpe Ratio (Daily)
    daily_pnl = full_df.groupby(full_df['date'].dt.date)['pnl'].sum()
    sharpe_ratio = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252) if daily_pnl.std() > 0 else 0

    # 3. Create Visualizations
    
    fig = make_subplots(
        rows=4, cols=2,
        specs=[[{"colspan": 2}, None],
               [{"colspan": 2}, None],
               [{}, {}],
               [{"colspan": 2}, None]],
        subplot_titles=("Equity Curve (Cumulative P&L)", "Drawdown", 
                       "Win/Loss Distribution", "Strategy Performance", "Daily P&L"),
        vertical_spacing=0.08
    )

    # Chart 1: Equity Curve
    fig.add_trace(go.Scatter(
        x=full_df['timestamp'], y=full_df['cumulative_pnl'],
        mode='lines', name='Equity',
        line=dict(color='#00E396', width=2),
        fill='tozeroy', fillcolor='rgba(0, 227, 150, 0.1)'
    ), row=1, col=1)

    # Chart 2: Drawdown
    fig.add_trace(go.Scatter(
        x=full_df['timestamp'], y=full_df['drawdown'],
        mode='lines', name='Drawdown',
        line=dict(color='#FF4560', width=1),
        fill='tozeroy', fillcolor='rgba(255, 69, 96, 0.2)'
    ), row=2, col=1)

    # Chart 3: Win/Loss Distribution (Histogram)
    fig.add_trace(go.Histogram(
        x=full_df['pnl'], nbinsx=30,
        name='P&L Distribution',
        marker_color='#775DD0'
    ), row=3, col=1)

    # Chart 4: Strategy Performance
    if 'strategy' in full_df.columns:
        strat_perf = full_df.groupby('strategy')['pnl'].sum().sort_values()
        colors = ['#FF4560' if x < 0 else '#00E396' for x in strat_perf.values]
        
        fig.add_trace(go.Bar(
            x=strat_perf.index, y=strat_perf.values,
            name='Strategy P&L',
            marker_color=colors
        ), row=3, col=2)

    # Chart 5: Daily P&L
    colors_daily = ['#FF4560' if x < 0 else '#00E396' for x in daily_pnl.values]
    fig.add_trace(go.Bar(
        x=daily_pnl.index, y=daily_pnl.values,
        name='Daily P&L',
        marker_color=colors_daily
    ), row=4, col=1)

    # Layout Styling
    fig.update_layout(
        title_text="🚀 High Accuracy Trading Report",
        title_font_size=24,
        template="plotly_dark",
        height=1200,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # 4. Generate HTML
    
    html_content = f"""
    <html>
    <head>
        <title>Trading Performance Report</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #111; color: #eee; margin: 0; padding: 20px; }}
            .container {{ max_width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
            .metric-card {{ background: #222; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333; }}
            .metric-value {{ font-size: 24px; font-weight: bold; margin: 10px 0; }}
            .metric-label {{ color: #888; font-size: 14px; }}
            .positive {{ color: #00E396; }}
            .negative {{ color: #FF4560; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Trading Performance Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Net P&L</div>
                    <div class="metric-value {'positive' if total_pnl > 0 else 'negative'}">₹{total_pnl:,.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Win Rate</div>
                    <div class="metric-value">{win_rate:.1f}%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Profit Factor</div>
                    <div class="metric-value">{profit_factor:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Sharpe Ratio</div>
                    <div class="metric-value">{sharpe_ratio:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Max Drawdown</div>
                    <div class="metric-value negative">₹{max_drawdown:,.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Expectancy</div>
                    <div class="metric-value {'positive' if expectancy > 0 else 'negative'}">₹{expectancy:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Trades</div>
                    <div class="metric-value">{len(full_df)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Avg Win / Avg Loss</div>
                    <div class="metric-value">₹{avg_win:.0f} / ₹{abs(avg_loss):.0f}</div>
                </div>
            </div>
            
            <!-- Plotly Chart -->
            {fig.to_html(full_html=False, include_plotlyjs='cdn')}
            
        </div>
    </body>
    </html>
    """
    
    output_file = "trading_report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n✅ Report generated successfully: {output_file}")
    print(f"📊 Open this file in your browser to view the dashboard.")

if __name__ == "__main__":
    generate_report()
