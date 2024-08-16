import React from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Home.css'; // Ensure Home.css contains custom styles
import image from '../images/image2.png';

function LandingPage() {
  const navigate = useNavigate();

  const handleLoginMoverCompanyClick = () => {
    navigate('/Login'); // Navigate
  };

  const handleSignUpMoverCompanyClick = () => {
    navigate('/SignUp'); // Navigate
  };

  return (
    <div className="home-container">
      {/* Hero Section */}
      <div className="hero-section">
        <img src={image} alt="Descriptive Alt Text" className="hero-image img-fluid" />
        <div className="hero-text bg-dark text-white p-4 rounded">
          <h1 className="display-4">Welcome to Movers Solution Company</h1>
          <p className="lead">Your reliable partner for a stress-free moving experience.</p>
          <button onClick={handleLoginMoverCompanyClick} className="btn btn-primary btn-lg me-2">Login MoverCompany</button>
          <button onClick={handleSignUpMoverCompanyClick} className="btn btn-secondary btn-lg">SignUp MoverCompany</button>
        </div>
      </div>

      {/* About Us Section */}
      <div className="about-us-section text-center py-5 bg-light">
        <h2 className="display-4">About Us</h2>
        <p className="lead">
          Movers Solution Company is committed to providing top-notch moving services. Our experienced team ensures a seamless and stress-free moving experience for all our clients. We take pride in our professionalism, attention to detail, and commitment to customer satisfaction.
        </p>
        <p>
          Founded in [Year], we have helped thousands of families and businesses move efficiently and safely. Whether you are moving across town or across the country, our team is dedicated to making your move as smooth as possible.
        </p>
      </div>

      {/* Features Section */}
      <div className="features-section text-center py-5">
        <h2 className="display-4">Why Choose Us?</h2>
        <div className="row">
          <div className="col-md-4 mb-4">
            <div className="feature card p-3 shadow-sm">
              <h3 className="card-title">Experienced Professionals</h3>
              <p className="card-text">Our team consists of experienced movers who handle your belongings with care and efficiency.</p>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="feature card p-3 shadow-sm">
              <h3 className="card-title">Comprehensive Services</h3>
              <p className="card-text">From packing to transport, we offer a full range of services to meet your moving needs.</p>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="feature card p-3 shadow-sm">
              <h3 className="card-title">Affordable Pricing</h3>
              <p className="card-text">We provide transparent and competitive pricing, with no hidden fees.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="testimonials-section text-center py-5">
        <h2 className="display-4">What Our Clients Say</h2>
        <div className="row">
          <div className="col-md-6 mb-4">
            <div className="testimonial card p-3 shadow-sm">
              <p className="card-text">"Movers Solution Company made my move easy and stress-free. Highly recommended!"</p>
              <p className="font-weight-bold">- Alex J.</p>
            </div>
          </div>
          <div className="col-md-6 mb-4">
            <div className="testimonial card p-3 shadow-sm">
              <p className="card-text">"Great service and friendly staff. Everything arrived on time and in perfect condition."</p>
              <p className="font-weight-bold">- Lisa M.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action Section */}
      <div className="cta-section text-center py-5 bg-light">
        <h2 className="display-4">Ready to Move?</h2>
        <p className="lead">Contact us today to schedule your move or get a free quote!</p>
        <button className="btn btn-primary btn-lg">Contact Us 0785678989</button>
      </div>
    </div>
  );
}

export default LandingPage;
