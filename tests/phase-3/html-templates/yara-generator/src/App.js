import React, { useState } from 'react';

const YaraRuleGenerator = () => {
  // State to store form data
  const [ruleName, setRuleName] = useState('');
  const [description, setDescription] = useState('');
  const [conditions, setConditions] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission (you can integrate API calls here)
    console.log({ ruleName, description, conditions });
  };

  return (
    <div className="container mt-5">
      <div className="text-center">
        <h1 className="display-4">YARA Rule Generator</h1>
        <p className="lead">Easily create powerful YARA rules for malware analysis and threat detection.</p>
      </div>

      <div className="card mt-4">
        <div className="card-body">
          <h5 className="card-title">Generate a New Rule</h5>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="ruleName" className="form-label">Rule Name</label>
              <input
                type="text"
                className="form-control"
                id="ruleName"
                name="ruleName"
                placeholder="Enter rule name"
                value={ruleName}
                onChange={(e) => setRuleName(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="description" className="form-label">Description</label>
              <textarea
                className="form-control"
                id="description"
                name="description"
                rows="3"
                placeholder="Provide a description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="conditions" className="form-label">Conditions</label>
              <textarea
                className="form-control"
                id="conditions"
                name="conditions"
                rows="5"
                placeholder="Define your YARA rule conditions"
                value={conditions}
                onChange={(e) => setConditions(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">Generate Rule</button>
          </form>
        </div>
      </div>

      <footer className="text-center mt-5">
        <p>&copy; 2024 YARA Rule Generator. Built with React.</p>
      </footer>
    </div>
  );
};

export default YaraRuleGenerator;

