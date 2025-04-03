import React, { useState, useEffect } from "react";
import axios from "axios";
import "../Styling/home.css"; // Import styling for Home component

const Home = () => {
  const [file, setFile] = useState(null);
  const [image, setImage] = useState(null);
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // Load Tidio Chatbot Script
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "//code.tidio.co/s70jwvgerrovy7mycbdtwo18ddeo40ko.js";
    script.async = true;
    document.body.appendChild(script);
  }, []);

  const handleFileChange = (event) => setFile(event.target.files[0]);
  const handleImageChange = (event) => setImage(event.target.files[0]);

  // Upload CSV
  const handleUploadCSV = async () => {
    if (!file) return alert("Please select a CSV file.");
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/analyze/csv/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(JSON.stringify(res.data, null, 2));
    } catch (error) {
      console.error("Error processing CSV file:", error);
      alert("Error processing CSV file.");
    } finally {
      setLoading(false);
    }
  };

  // Upload Image
  const handleImageUpload = async () => {
    if (!image) {
      alert("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/analyze/image/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Server Response:", data);  // Debugging step ✅

      setResponse(data.message || "No response received");
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Error uploading image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-container">
      <h2 className="title">📊 MarketMood - Analyzing the emotional pulse of the market</h2>

      {/* CSV Upload */}
      <div className="upload-section">
        <input type="file" accept=".csv" className="file-input" onChange={handleFileChange} />
        <button className="upload-btn csv-btn" onClick={handleUploadCSV} disabled={loading}>
          {loading ? "Processing..." : "Upload CSV"}
        </button>
      </div>

      {/* Image Upload */}
      <div className="upload-section">
        <input type="file" accept="image/*" className="file-input" onChange={handleImageChange} />
        <button className="upload-btn image-btn" onClick={handleImageUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload Image"}
        </button>
      </div>

      {/* Response Box */}
      <textarea className="response-box" value={response} readOnly placeholder="Results will be displayed here..." />

      {/* Tidio Chatbot */}
      <div id="tidio-chatbot"></div>
    </div>
  );
};

export default Home;







