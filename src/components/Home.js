import React from 'react';
import './Home.css'; // Ensure this path is correct
import image3 from '../images/image3.png';

const Home = () => {
  return (
    <div className="home-container">
      {/* Hero Section */}
      <div className="hero-section">
        <img src={image3} alt="View of our services" className="hero-image" />
        <div className="hero-text">
          <h1>MOVERS SOLUTION COMPANY</h1>
          
          <p>Your reliable partner for a stress-free moving experience.</p>
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
    </div>
  );
}

export default Home;
