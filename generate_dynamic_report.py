#!/usr/bin/env python3
"""
📊 DYNAMIC TRADING REPORT GENERATOR
Generates a single HTML file with embedded data and JavaScript for interactive filtering.
"""

import pandas as pd
import glob
import json
from datetime import datetime
import os

def generate_dynamic_report():
    print("🚀 GENERATING DYNAMIC TRADING REPORT")
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
            
            # Standardize P&L column
            if 'net_pnl_after_charges' in df.columns:
                df['pnl'] = df['net_pnl_after_charges']
            elif 'pnl_after_charges' in df.columns:
                df['pnl'] = df['pnl_after_charges']
            elif 'gross_pnl' in df.columns:
                df['pnl'] = df['gross_pnl'] - 40 # Estimate
            else:
                df['pnl'] = 0
                
            # Ensure required columns exist
            if 'action' not in df.columns:
                continue
                
            # Add date from filename if timestamp missing or parse timestamp
            # Filename format: high_accuracy_trades_YYYYMMDD.csv
            date_str = file.replace("high_accuracy_trades_", "").replace(".csv", "")
            try:
                file_date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
            except ValueError:
                # Fallback if filename format is different
                file_date = datetime.now().strftime("%Y-%m-%d")

            # Convert timestamp to string for JSON serialization
            df['timestamp'] = df['timestamp'].astype(str)
            df['date'] = file_date
            
            # Fill NaN values to avoid JSON errors
            df = df.fillna(0)
            
            # Convert to records
            records = df.to_dict('records')
            all_trades.extend(records)
            
        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")

    if not all_trades:
        print("❌ No valid trades found.")
        return

    print(f"✅ Loaded {len(all_trades)} total trade records")

    # 2. Prepare JSON Data
    trades_json = json.dumps(all_trades)
    
    # 3. Generate HTML with Embedded Data and JS
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Trading Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #111; color: #eee; font-family: 'Segoe UI', sans-serif; }}
        .card {{ background-color: #1e1e1e; border: 1px solid #333; border-radius: 0.5rem; padding: 1.5rem; }}
        .metric-value {{ font-size: 1.5rem; font-weight: bold; }}
        .metric-label {{ color: #888; font-size: 0.875rem; }}
        .positive {{ color: #00E396; }}
        .negative {{ color: #FF4560; }}
        select {{ background-color: #333; color: #fff; border: 1px solid #444; padding: 0.5rem; border-radius: 0.25rem; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid #333; }}
        th {{ color: #888; font-weight: normal; }}
        tr:hover {{ background-color: #222; }}
    </style>
</head>
<body class="p-6">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold mb-2">🚀 Trading Performance Dashboard</h1>
                <p class="text-gray-400">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            <div>
                <label class="mr-2 text-gray-400">Select Period:</label>
                <select id="dateSelector" onchange="updateDashboard()">
                    <option value="all">All Time</option>
                </select>
            </div>
        </div>

        <!-- Metrics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div class="card">
                <div class="metric-label">Net P&L</div>
                <div id="metric-pnl" class="metric-value">₹0.00</div>
            </div>
            <div class="card">
                <div class="metric-label">Win Rate</div>
                <div id="metric-winrate" class="metric-value">0%</div>
            </div>
            <div class="card">
                <div class="metric-label">Profit Factor</div>
                <div id="metric-pf" class="metric-value">0.00</div>
            </div>
            <div class="card">
                <div class="metric-label">Total Trades</div>
                <div id="metric-trades" class="metric-value">0</div>
            </div>
        </div>

        <!-- Charts Row 1 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Equity Curve</h3>
                <div id="chart-equity" style="height: 350px;"></div>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Drawdown</h3>
                <div id="chart-drawdown" style="height: 350px;"></div>
            </div>
        </div>

        <!-- Charts Row 2 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Strategy Performance</h3>
                <div id="chart-strategy" style="height: 350px;"></div>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Daily P&L</h3>
                <div id="chart-daily" style="height: 350px;"></div>
            </div>
        </div>

        <!-- Charts Row 3 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Win/Loss Distribution</h3>
                <div id="chart-dist" style="height: 350px;"></div>
            </div>
        </div>

        <!-- Recent Trades Table -->
        <div class="card">
            <h3 class="text-lg font-semibold mb-4">Trade Log</h3>
            <div class="overflow-x-auto">
                <table id="trades-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Symbol</th>
                            <th>Action</th>
                            <th>Price</th>
                            <th>P&L</th>
                            <th>Strategy</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Embedded Data
        const allTrades = {trades_json};
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            populateDateSelector();
            updateDashboard();
        }});

        function populateDateSelector() {{
            const selector = document.getElementById('dateSelector');
            const dates = [...new Set(allTrades.map(t => t.date))].sort().reverse();
            
            dates.forEach(date => {{
                const option = document.createElement('option');
                option.value = date;
                option.textContent = date;
                selector.appendChild(option);
            }});
        }}

        function updateDashboard() {{
            const selectedDate = document.getElementById('dateSelector').value;
            
            // Filter trades
            let filteredTrades = allTrades;
            if (selectedDate !== 'all') {{
                filteredTrades = allTrades.filter(t => t.date === selectedDate);
            }}
            
            // Filter for EXITs only for metrics
            const exits = filteredTrades.filter(t => t.action === 'EXIT');
            
            // Calculate Metrics
            calculateMetrics(exits);
            
            // Update Charts
            updateCharts(filteredTrades, exits);
            
            // Update Table
            updateTable(filteredTrades);
        }}

        function calculateMetrics(exits) {{
            let totalPnL = 0;
            let wins = 0;
            let grossProfit = 0;
            let grossLoss = 0;
            
            exits.forEach(t => {{
                const pnl = t.pnl || 0;
                totalPnL += pnl;
                if (pnl > 0) {{
                    wins++;
                    grossProfit += pnl;
                }} else {{
                    grossLoss += Math.abs(pnl);
                }}
            }});
            
            const winRate = exits.length > 0 ? (wins / exits.length * 100) : 0;
            const profitFactor = grossLoss > 0 ? (grossProfit / grossLoss) : (grossProfit > 0 ? Infinity : 0);
            
            // Update DOM
            const pnlEl = document.getElementById('metric-pnl');
            pnlEl.textContent = `₹${{totalPnL.toLocaleString('en-IN', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}`;
            pnlEl.className = `metric-value ${{totalPnL >= 0 ? 'positive' : 'negative'}}`;
            
            document.getElementById('metric-winrate').textContent = `${{winRate.toFixed(1)}}%`;
            document.getElementById('metric-pf').textContent = profitFactor.toFixed(2);
            document.getElementById('metric-trades').textContent = exits.length;
        }}

        function updateCharts(allTrades, exits) {{
            // 1. Equity Curve
            // Sort by timestamp for correct line chart
            const sortedExits = [...exits].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            let cumulative = 0;
            const equityX = sortedExits.map(t => t.timestamp);
            const equityY = sortedExits.map(t => {{
                cumulative += (t.pnl || 0);
                return cumulative;
            }});
            
            Plotly.newPlot('chart-equity', [{{
                x: equityX,
                y: equityY,
                type: 'scatter',
                mode: 'lines',
                name: 'Equity',
                line: {{ color: '#00E396', width: 2 }},
                fill: 'tozeroy',
                fillcolor: 'rgba(0, 227, 150, 0.1)'
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{ color: '#888' }},
                margin: {{ t: 10, l: 40, r: 10, b: 40 }},
                xaxis: {{ gridcolor: '#333' }},
                yaxis: {{ gridcolor: '#333' }}
            }});

            // 2. Drawdown Chart
            let peak = -Infinity;
            const drawdownY = equityY.map(val => {{
                if (val > peak) peak = val;
                return val - peak;
            }});

            Plotly.newPlot('chart-drawdown', [{{
                x: equityX,
                y: drawdownY,
                type: 'scatter',
                mode: 'lines',
                name: 'Drawdown',
                line: {{ color: '#FF4560', width: 1 }},
                fill: 'tozeroy',
                fillcolor: 'rgba(255, 69, 96, 0.2)'
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{ color: '#888' }},
                margin: {{ t: 10, l: 40, r: 10, b: 40 }},
                xaxis: {{ gridcolor: '#333' }},
                yaxis: {{ gridcolor: '#333' }}
            }});

            // 3. Strategy Performance
            const strategies = {{}};
            exits.forEach(t => {{
                const s = t.strategy || 'Unknown';
                strategies[s] = (strategies[s] || 0) + (t.pnl || 0);
            }});
            
            const stratX = Object.keys(strategies);
            const stratY = Object.values(strategies);
            const stratColors = stratY.map(v => v >= 0 ? '#00E396' : '#FF4560');
            
            Plotly.newPlot('chart-strategy', [{{
                x: stratX,
                y: stratY,
                type: 'bar',
                marker: {{ color: stratColors }}
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{ color: '#888' }},
                margin: {{ t: 10, l: 40, r: 10, b: 40 }},
                xaxis: {{ gridcolor: '#333' }},
                yaxis: {{ gridcolor: '#333' }}
            }});

            // 4. Daily P&L (Only relevant for "All Time" really, but can show hourly for single day if needed)
            // For simplicity, we'll keep it as Daily P&L for now, or maybe Trade P&L for single day
            const isSingleDay = document.getElementById('dateSelector').value !== 'all';
            
            let barX, barY, barTitle;
            if (isSingleDay) {{
                // Show individual trade P&L
                barX = sortedExits.map((_, i) => `Trade ${{i+1}}`);
                barY = sortedExits.map(t => t.pnl);
                barTitle = 'Trade P&L';
            }} else {{
                // Show Daily P&L
                const daily = {{}};
                exits.forEach(t => {{
                    const d = t.date;
                    daily[d] = (daily[d] || 0) + (t.pnl || 0);
                }});
                barX = Object.keys(daily).sort();
                barY = barX.map(d => daily[d]);
                barTitle = 'Daily P&L';
            }}
            
            const barColors = barY.map(v => v >= 0 ? '#00E396' : '#FF4560');

            Plotly.newPlot('chart-daily', [{{
                x: barX,
                y: barY,
                type: 'bar',
                marker: {{ color: barColors }}
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{ color: '#888' }},
                margin: {{ t: 10, l: 40, r: 10, b: 40 }},
                xaxis: {{ gridcolor: '#333' }},
                yaxis: {{ gridcolor: '#333' }}
            }});
            
            // 4. Distribution
            const pnlValues = exits.map(t => t.pnl);
            Plotly.newPlot('chart-dist', [{{
                x: pnlValues,
                type: 'histogram',
                marker: {{ color: '#775DD0' }}
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{ color: '#888' }},
                margin: {{ t: 10, l: 40, r: 10, b: 40 }},
                xaxis: {{ gridcolor: '#333' }},
                yaxis: {{ gridcolor: '#333' }}
            }});
        }}

        function updateTable(trades) {{
            const tbody = document.querySelector('#trades-table tbody');
            tbody.innerHTML = '';
            
            // Show last 50 trades to avoid lag
            const displayTrades = trades.slice(-50).reverse();
            
            displayTrades.forEach(t => {{
                const row = document.createElement('tr');
                const pnlClass = t.pnl > 0 ? 'positive' : (t.pnl < 0 ? 'negative' : '');
                const pnlText = t.action === 'EXIT' ? `₹${{t.pnl.toFixed(2)}}` : '-';
                
                row.innerHTML = `
                    <td>${{t.timestamp}}</td>
                    <td>${{t.symbol}}</td>
                    <td><span class="${{t.action === 'ENTRY' ? 'text-blue-400' : 'text-purple-400'}}">${{t.action}}</span></td>
                    <td>₹${{t.entry_price || t.exit_price}}</td>
                    <td class="${{pnlClass}}">${{pnlText}}</td>
                    <td>${{t.strategy || '-'}}</td>
                `;
                tbody.appendChild(row);
            }});
        }}
    </script>
</body>
</html>
    """
    
    output_file = "trading_report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n✅ Dynamic report generated: {output_file}")

if __name__ == "__main__":
    generate_dynamic_report()
