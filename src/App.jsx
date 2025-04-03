import "./App.css";
import Home from "./Home/home.jsx";
import Navbar from "./Home/navbar.jsx";
import Footer from "./Footer/footer.jsx";
import SentimentChart from "./Home/sentiment.jsx";
import FakeNewsDetector from "./Home/fakeNews.jsx";

function App() {
  return (
    <>
      <Navbar />
      <Home />
      <SentimentChart />
      <FakeNewsDetector />
      <Footer />
    </>
  );
}

export default App;

