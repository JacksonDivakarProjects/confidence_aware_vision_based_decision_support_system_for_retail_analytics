import React from 'react';
import './GenderChart.css';

const GenderChart = ({ data }) => {
  const total = data.male + data.female;
  const malePercent = (data.male / total) * 100;
  const femalePercent = (data.female / total) * 100;

  return (
    <div className="gender-chart">
      <div className="chart-bars">
        <div className="bar-row">
          <div className="bar-label">
            <span className="label-icon">👨</span>
            <span className="label-text">Male</span>
          </div>
          <div className="bar-container">
            <div 
              className="bar bar-male" 
              style={{ width: `${malePercent}%` }}
            >
              <span className="bar-value">{data.male}%</span>
            </div>
          </div>
        </div>

        <div className="bar-row">
          <div className="bar-label">
            <span className="label-icon">👩</span>
            <span className="label-text">Female</span>
          </div>
          <div className="bar-container">
            <div 
              className="bar bar-female" 
              style={{ width: `${femalePercent}%` }}
            >
              <span className="bar-value">{data.female}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="chart-legend">
        <div className="legend-item">
          <div className="legend-dot male"></div>
          <span>Male: {data.male}%</span>
        </div>
        <div className="legend-item">
          <div className="legend-dot female"></div>
          <span>Female: {data.female}%</span>
        </div>
      </div>
    </div>
  );
};

export default GenderChart;