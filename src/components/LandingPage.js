import React from 'react';
import './Home.css';
import image from '../images/image2.png';
import {useNavigate} from 'react-router-dom';


function LandingPage() {
  const navigate = useNavigate();

  const handleLoginMoverCompanyClick = () => {
    navigate('/Login'); // Navigate
  }
  const handleSignUpMoverCompanyClick = () => {
    navigate('/SignUp'); // Navigate
  }
  return (
    <div className="home-container">
      {/* Hero Section */}
      <div className="hero-section">
        <img src={image} alt="Descriptive Alt Text" className="hero-image" />
        <div className="hero-text">
          <h1>Welcome to Movers Solution Company</h1>
          <p>Your reliable partner for a stress-free moving experience.</p>
          <button onClick={handleLoginMoverCompanyClick} className="cta-button">Login MoverCompany</button>
          <button onClick={handleSignUpMoverCompanyClick} className="cta-button">SignUp MoverCompany</button>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <h2>Why Choose Us?</h2>
        <div className="features">
          <div className="feature">
            <h3>Experienced Professionals</h3>
            <p>Our team consists of experienced movers who handle your belongings with care and efficiency.</p>
          </div>
          <div className="feature">
            <h3>Comprehensive Services</h3>
            <p>From packing to transport, we offer a full range of services to meet your moving needs.</p>
          </div>
          <div className="feature">
            <h3>Affordable Pricing</h3>
            <p>We provide transparent and competitive pricing, with no hidden fees.</p>
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="testimonials-section">
        <h2>What Our Clients Say</h2>
        <div className="testimonials">
          <div className="testimonial">
            <p>"Movers Solution Company made my move easy and stress-free. Highly recommended!"</p>
            <p>- Alex J.</p>
          </div>
          <div className="testimonial">
            <p>"Great service and friendly staff. Everything arrived on time and in perfect condition."</p>
            <p>- Lisa M.</p>
          </div>
        </div>
      </div>

      {/* Call to Action Section */}
      <div className="cta-section">
        <h2>Ready to Move?</h2>
        <p>Contact us today to schedule your move or get a free quote!</p>
        <button className="cta-button">Contact Us 0785678989</button>
      </div>
    </div>
  );
}

export default LandingPage;