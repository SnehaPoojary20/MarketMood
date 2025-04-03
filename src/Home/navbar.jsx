import React from "react";
import Logo from "../assets/logo.png";
import "../Styling/navbar.css"; // Import styling for Navbar

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="container">
        <img src={Logo} alt="MarketMood Logo" className="logo" />
        <h1 className="navbar-title">MarketMood</h1>
      </div>
    </nav>
  );
};

export default Navbar;
