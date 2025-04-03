import React, { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend } from "recharts";
import "../Styling/sentiment.css"; // Import styling for SentimentChart

const COLORS = ["#0088FE", "#00C49F", "#FFBB28"];

const SentimentChart = () => {
  const [sentimentData, setSentimentData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/get-sentiment")
      .then(response => {
        setSentimentData(response.data);
      })
      .catch(error => console.error("Error fetching sentiment data:", error));
  }, []);
  

  if (!sentimentData) return <p>Loading sentiment data...</p>;

  const barChartData = Object.entries(sentimentData).map(([sentiment, count]) => ({
    sentiment,
    count,
  }));

  const pieChartData = Object.entries(sentimentData).map(([sentiment, count], index) => ({
    name: sentiment,
    value: count,
    color: COLORS[index % COLORS.length],
  }));

  return (
    <div className="chart-container">
      <h2>Sentiment Analysis Results</h2>

      <BarChart width={500} height={300} data={barChartData}>
        <XAxis dataKey="sentiment" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="#8884d8" />
      </BarChart>

      <PieChart width={400} height={400}>
        <Pie data={pieChartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={120} label>
          {pieChartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default SentimentChart;

