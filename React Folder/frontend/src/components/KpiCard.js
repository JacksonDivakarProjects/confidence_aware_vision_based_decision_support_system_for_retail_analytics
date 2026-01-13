// ==================================
// FILE 1: src/components/KpiCard.js
// ==================================

import React from 'react';
import './KpiCard.css';

const KpiCard = ({ title, value, icon, trend, color = 'primary' }) => {
  return (
    <div className={`kpi-card kpi-card-${color}`}>
      <div className="kpi-background"></div>
      <div className="kpi-content">
        <div className="kpi-header">
          <span className="kpi-icon">{icon || '📊'}</span>
          <span className="kpi-label">{title}</span>
        </div>
        <div className="kpi-value">{typeof value === 'number' ? value.toLocaleString() : value}</div>
        {trend && (
          <div className={`kpi-trend ${trend > 0 ? 'positive' : 'negative'}`}>
            <span className="trend-icon">{trend > 0 ? '↗' : '↘'}</span>
            <span>{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
      <div className="kpi-shine"></div>
    </div>
  );
};

export default KpiCard;


// ==================================
// FILE 2: src/components/KpiCard.css
// ==================================

/* Copy this content to src/components/KpiCard.css */