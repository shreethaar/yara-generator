import React from 'react';

const RuleOutput = ({ rule }) => {
    return (
        <div>
            <h2>Generated YARA Rule:</h2>
            <pre>{rule}</pre>
        </div>
    );
};

export default RuleOutput;
