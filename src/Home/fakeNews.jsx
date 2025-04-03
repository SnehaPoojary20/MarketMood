import React, { useState } from "react";
import axios from "axios";
import "../Styling/fakeNews.css"; // Import CSS for styling

const FakeNewsDetector = () => {
  const [newsText, setNewsText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleDetectFakeNews = async () => {
    if (!newsText.trim()) {
      alert("Please enter news content to analyze.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/fake-news", { text: newsText });
      setResult(response.data.result);
    } catch (error) {
      setResult("Error detecting fake news. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="fake-news-container">
      <h2 className="title">📰 Fake News Detector</h2>
      <textarea
        className="news-input"
        value={newsText}
        onChange={(e) => setNewsText(e.target.value)}
        placeholder="Enter news article text here..."
      />
      <button className="detect-btn" onClick={handleDetectFakeNews} disabled={loading}>
        {loading ? "Analyzing..." : "Detect Fake News"}
      </button>
      {result && <p className="result">{result}</p>}
    </div>
  );
};

export default FakeNewsDetector;
