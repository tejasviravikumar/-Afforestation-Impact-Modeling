import bonsai from './assets/bonsai.jpg';

function Firstpage({ onGetStarted }) {
  const handleGetStarted = () => {
    console.log('Getting started with Bonsai!');
    if (onGetStarted) {
      onGetStarted();
    }
  };

  return (
    <div className="firstpage">
      <div className="content-section">
        <div className="text-content">
          <div className="subtitle">Afforestation Impact</div>
          <h1 className="title">Bonsai</h1>
          <p className="text">
            Welcome to <b>Bonsai</b> – a revolutionary afforestation impact model that empowers you 
            to understand tree growth rates, carbon sequestration potential, and environmental 
            restoration through data-driven insights.
          </p>
          <div className="button-container">
            <button onClick={handleGetStarted} aria-label="Get started with Bonsai">
              Get Started
            </button>
          </div>
        </div>
      </div>

      <div className="image-section">
        <div className="image-container">
          <img
            className="Bonsai"
            src={bonsai}
            alt="Beautiful Bonsai tree representing sustainable growth and environmental harmony"
            loading="lazy"
          />
        </div>
      </div>

      <div className="stats-overlay">
        <div className="stat-item">
          <span className="stat-number">85%</span>
          <span className="stat-label">CO₂ Absorption</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">34</span>
          <span className="stat-label">Trees Analyzed</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">98%</span>
          <span className="stat-label">Accuracy Rate</span>
        </div>
      </div>
    </div>
  );
}

export default Firstpage;