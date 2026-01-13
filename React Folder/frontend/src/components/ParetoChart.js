import React from 'react';
import './ParetoChart.css';

const ParetoChart = ({ percentage }) => {
  const circumference = 2 * Math.PI * 70;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="pareto-chart">
      <div className="circle-container">
        <svg className="circle-svg" viewBox="0 0 160 160">
          <defs>
            <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#667eea" />
              <stop offset="100%" stopColor="#764ba2" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          <circle
            className="circle-bg"
            cx="80"
            cy="80"
            r="70"
            fill="none"
            stroke="var(--bg-tertiary)"
            strokeWidth="12"
          />
          
          <circle
            className="circle-progress"
            cx="80"
            cy="80"
            r="70"
            fill="none"
            stroke="url(#circleGradient)"
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            filter="url(#glow)"
            style={{
              transform: 'rotate(-90deg)',
              transformOrigin: '50% 50%'
            }}
          />
        </svg>
        
        <div className="circle-text">
          <div className="circle-percentage">{percentage}%</div>
          <div className="circle-label">Top Hours</div>
        </div>
      </div>
    </div>
  );
};

export default ParetoChart;