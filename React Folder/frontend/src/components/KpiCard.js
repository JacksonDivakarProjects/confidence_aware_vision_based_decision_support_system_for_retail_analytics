// FILE: src/components/KpiCard.js

import React from 'react';
import './KpiCard.css';

const KpiCard = ({ title, value, icon, subtitle }) => {
  return (
    <div className="kpi-card">
      <div className="kpi-icon-wrapper">
        <span className="kpi-icon">{icon}</span>
      </div>
      
      <div className="kpi-content">
        <h3 className="kpi-title">{title}</h3>
        {subtitle && <span className="kpi-subtitle">{subtitle}</span>}
        <div className="kpi-value">{value}</div>
      </div>
    </div>
  );
};

export default KpiCard;