import React, { useState } from 'react';
import RuleForm from './components/RuleForm';
import RuleOutput from './components/RuleOutput';
import './App.css';

function App() {
    const [generatedRule, setGeneratedRule] = useState('');

    return (
        <div className="App">
            <h1>YARA Rule Generator</h1>
            <RuleForm onRuleGenerated={setGeneratedRule} />
            {generatedRule && <RuleOutput rule={generatedRule} />}
        </div>
    );
}

export default App;
