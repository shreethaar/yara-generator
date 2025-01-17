import React, { useState } from 'react';
import { generateYaraRule } from '../api';

const RuleForm = ({ onRuleGenerated }) => {
    const [ruleName, setRuleName] = useState('');
    const [author, setAuthor] = useState('');
    const [description, setDescription] = useState('');
    const [strings, setStrings] = useState([]);
    const [conditions, setConditions] = useState([]);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const ruleData = {
                rule_name: ruleName,
                author,
                description,
                strings,
                conditions,
                save: true,
                filename: `${ruleName}.yar`
            };
            const response = await generateYaraRule(ruleData);
            onRuleGenerated(response.rule);
            setError('');
        } catch (err) {
            setError('Failed to generate YARA rule. Please check your input.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Rule Name:</label>
                <input
                    type="text"
                    value={ruleName}
                    onChange={(e) => setRuleName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Author:</label>
                <input
                    type="text"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Description:</label>
                <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
            </div>
            <div>
                <label>Strings:</label>
                <button type="button" onClick={() => setStrings([...strings, { identifier: '', pattern: '', type: 'text' }])}>
                    Add String
                </button>
                {strings.map((string, index) => (
                    <div key={index}>
                        <input
                            type="text"
                            placeholder="Identifier"
                            value={string.identifier}
                            onChange={(e) => {
                                const newStrings = [...strings];
                                newStrings[index].identifier = e.target.value;
                                setStrings(newStrings);
                            }}
                        />
                        <input
                            type="text"
                            placeholder="Pattern"
                            value={string.pattern}
                            onChange={(e) => {
                                const newStrings = [...strings];
                                newStrings[index].pattern = e.target.value;
                                setStrings(newStrings);
                            }}
                        />
                        <select
                            value={string.type}
                            onChange={(e) => {
                                const newStrings = [...strings];
                                newStrings[index].type = e.target.value;
                                setStrings(newStrings);
                            }}
                        >
                            <option value="text">Text</option>
                            <option value="hex">Hex</option>
                            <option value="regex">Regex</option>
                        </select>
                        <button type="button" onClick={() => setStrings(strings.filter((_, i) => i !== index))}>
                            Remove
                        </button>
                    </div>
                ))}
            </div>
            <div>
                <label>Conditions:</label>
                <button type="button" onClick={() => setConditions([...conditions, ''])}>
                    Add Condition
                </button>
                {conditions.map((condition, index) => (
                    <div key={index}>
                        <input
                            type="text"
                            value={condition}
                            onChange={(e) => {
                                const newConditions = [...conditions];
                                newConditions[index] = e.target.value;
                                setConditions(newConditions);
                            }}
                        />
                        <button type="button" onClick={() => setConditions(conditions.filter((_, i) => i !== index))}>
                            Remove
                        </button>
                    </div>
                ))}
            </div>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            <button type="submit">Generate YARA Rule</button>
        </form>
    );
};

export default RuleForm;
