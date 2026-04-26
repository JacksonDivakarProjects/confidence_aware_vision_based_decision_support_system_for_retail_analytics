// FILE: src/pages/Dashboard.js

import React, { useEffect, useState } from 'react';
import { fetchInsights } from '../api';
import KpiCard from '../components/KpiCard';
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

  // ✅ NEW DATA CONTRACT
  
  const baselineKpis = data.baseline;
  const confidenceKpis = data.confidence_aware;
  const trend = data.trend;


  return (
    <div className="dashboard">
      <div className="dashboard-container">

        {/* Page Header */}
        <div className="page-header">
          <div className="header-content">
            <h1 className="page-title">Retail Footfall Analytics</h1>
            <p className="page-subtitle">
              Confidence-aware decision support for retail operations
            </p>
          </div>
          <div className="header-badge">
            <span className="badge-icon">🛡️</span>
            <span className="badge-text">Stability Mode</span>
          </div>
        </div>

        {/* KPI Cards — CONFIDENCE AWARE */}
        <section className="kpi-section">
          <div className="section-header">
            <h2 className="section-title">Confidence-Aware KPIs</h2>
            <p className="section-description">Enhanced metrics with confidence weighting applied</p>
          </div>
          
          <div className="kpi-grid">
            <KpiCard
              title="Total Footfall"
              value={confidenceKpis.total_footfall_weighted.toLocaleString()}
              icon="👥"
              subtitle="Weighted"
            />

            <KpiCard
              title="Daily Average"
              value={Math.round(confidenceKpis.avg_daily_footfall_weighted).toLocaleString()}
              icon="📊"
              subtitle="Footfall"
            />

            <KpiCard
              title="Session Duration"
              value={`${confidenceKpis.avg_session_seconds}s`}
              icon="⏱️"
              subtitle="Average"
            />

            <KpiCard
              title="Stability Score"
              value={confidenceKpis.stability_score}
              icon="🛡️"
              subtitle="High Confidence"
            />
          </div>
        </section>

        {/* KPI Cards — BASELINE */}
        <section className="kpi-section baseline">
          <div className="section-header">
            <h2 className="section-title">Baseline KPIs</h2>
            <p className="section-description">Standard metrics without confidence adjustment</p>
          </div>
          
          <div className="kpi-grid">
            <KpiCard
              title="Total Footfall"
              value={baselineKpis.total_footfall.toLocaleString()}
              icon="👥"
              subtitle="Unweighted"
            />

            <KpiCard
              title="Daily Average"
              value={Math.round(baselineKpis.avg_daily_footfall).toLocaleString()}
              icon="📊"
              subtitle="Footfall"
            />

            <KpiCard
              title="Session Duration"
              value={`${baselineKpis.avg_session_seconds}s`}
              icon="⏱️"
              subtitle="Average"
            />

            <KpiCard
              title="Stability Score"
              value={baselineKpis.stability_score}
              icon="⚠️"
              subtitle="Standard"
            />
          </div>
        </section>

        {/* Bottom Grid: Trend + Insights */}
        <div className="bottom-grid">
          
          {/* Trend Analysis */}
          <section className="trend-section">
            <div className="trend-card">
              <div className="card-header">
                <span className="card-icon">📈</span>
                <h2 className="card-title">Demand Trend</h2>
              </div>

              <div className="card-body">
                <div className="trend-metric">
                  <span className="metric-label">Status</span>
                  <span className="metric-value status">{trend.interpretation}</span>
                </div>

                <div className="trend-metric">
                  <span className="metric-label">Slope</span>
                  <span className="metric-value slope">{trend.slope}</span>
                </div>
              </div>
            </div>
          </section>

          {/* Key Insights */}
          <section className="insights-section">
            <div className="insights-card">
              <div className="card-header">
                <span className="card-icon">💡</span>
                <h2 className="card-title">Key Insights</h2>
              </div>

              <div className="card-body">
                <div className="insight-item">
                  <span className="insight-bullet">•</span>
                  <p>
                    Stability improved from <strong>{baselineKpis.stability_score}</strong> to{" "}
                    <strong>{confidenceKpis.stability_score}</strong> with confidence weighting
                  </p>
                </div>
                
                
                
                <div className="insight-item">
                  <span className="insight-bullet">•</span>
                  <p>
                    Trend indicates <strong>{trend.interpretation}</strong> demand pattern
                  </p>
                </div>
              </div>
            </div>
          </section>

        </div>

      </div>
    </div>
  );
};

export default Dashboard;