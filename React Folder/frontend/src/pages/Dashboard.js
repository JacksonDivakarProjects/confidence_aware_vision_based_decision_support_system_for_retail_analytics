// FILE: src/pages/Dashboard.js

import React, { useEffect, useState } from 'react';
import { fetchInsights } from '../api';
import KpiCard from '../components/KpiCard';
import GenderChart from '../components/GenderChart';
import ParetoChart from '../components/ParetoChart';
import './Dashboard.css';

console.log("DASHBOARD MOUNTED");


const Dashboard = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchInsights()
      .then((res) => setData(res))
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="error-container">
        <div className="error-icon">⚠️</div>
        <div className="error-text">Backend error: {error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <div className="loading-text">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        
        {/* Page Header */}
        <div className="page-header">
          <div className="header-content">
            <h1 className="page-title">Retail Footfall Analytics</h1>
            <p className="page-subtitle">
              Real-time insights and business intelligence for your retail operations
            </p>
          </div>
          <div className="header-badge">
            <span className="badge-icon">🔥</span>
            <span className="badge-text">Live Data</span>
          </div>
        </div>

        {/* KPI Cards */}
        <section className="kpi-section">
          <div className="kpi-grid">
            <KpiCard 
              title="Total Visitors" 
              value={data.kpis.total_visitors} 
              icon="👥"
              trend={12.5}
            />
            <KpiCard 
              title="Avg Daily Footfall" 
              value={data.kpis.avg_daily_footfall} 
              icon="📊"
              trend={8.3}
            />
            <KpiCard 
              title="Avg Session" 
              value={`${data.kpis.avg_session_seconds}s`} 
              icon="⏱️"
              trend={-3.2}
            />
            <KpiCard 
              title="Peak Hour" 
              value={`${data.kpis.peak_hour}:00`} 
              icon="🕐"
            />
          </div>
        </section>

        {/* Charts Section */}
        <section className="charts-section">
          <div className="charts-grid">
            
            {/* Gender Distribution */}
            <div className="chart-card">
              <div className="card-header">
                <div className="header-left">
                  <span className="card-icon">👥</span>
                  <h2 className="card-title">Gender Distribution</h2>
                </div>
                <span className="card-badge">Demographics</span>
              </div>
              <div className="card-body">
                <GenderChart data={data.demographics.gender_distribution_pct} />
              </div>
            </div>

            {/* Pareto Chart */}
            <div className="chart-card">
              <div className="card-header">
                <div className="header-left">
                  <span className="card-icon">⏰</span>
                  <h2 className="card-title">Time Concentration</h2>
                </div>
                <span className="card-badge">Pareto Analysis</span>
              </div>
              <div className="card-body">
                <ParetoChart percentage={data.pareto.top_hours_percentage} />
                <p className="chart-description">
                  Top <strong>{data.pareto.top_hours_percentage}%</strong> of hours contribute to{' '}
                  <strong>80%</strong> of total footfall
                </p>
              </div>
            </div>

          </div>
        </section>

        {/* Trend Analysis */}
        <section className="trend-section">
          <div className="trend-card">
            <div className="card-header">
              <div className="header-left">
                <span className="card-icon">📈</span>
                <h2 className="card-title">Demand Trend Analysis</h2>
              </div>
            </div>
            <div className="card-body">
              <div className="trend-content">
                <div className="trend-info">
                  <div className="info-item">
                    <span className="info-label">Status</span>
                    <span className={`trend-status ${data.trend.interpretation.toLowerCase()}`}>
                      {data.trend.interpretation}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Slope</span>
                    <span className="trend-value">{data.trend.slope}</span>
                  </div>
                </div>
                <div className="trend-visual">
                  <div className="trend-line">
                    <div className={`trend-arrow ${data.trend.interpretation.toLowerCase()}`}>
                      {data.trend.interpretation === 'Growing' ? '📈' : 
                       data.trend.interpretation === 'Declining' ? '📉' : '➡️'}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Insights Section */}
        <section className="insights-section">
          <div className="insights-card">
            <div className="card-header">
              <div className="header-left">
                <span className="card-icon">💡</span>
                <h2 className="card-title">Key Insights</h2>
              </div>
            </div>
            <div className="card-body">
              <div className="insights-grid">
                <div className="insight-item">
                  <div className="insight-icon success">✓</div>
                  <div className="insight-content">
                    <h4>Peak Performance</h4>
                    <p>Highest traffic recorded at {data.kpis.peak_hour}:00</p>
                  </div>
                </div>
                <div className="insight-item">
                  <div className="insight-icon warning">⚡</div>
                  <div className="insight-content">
                    <h4>Optimization Opportunity</h4>
                    <p>Consider staff adjustment during peak hours</p>
                  </div>
                </div>
                <div className="insight-item">
                  <div className="insight-icon info">ℹ️</div>
                  <div className="insight-content">
                    <h4>Trend Alert</h4>
                    <p>Footfall shows {data.trend.interpretation.toLowerCase()} pattern</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

export default Dashboard;