import  { useState } from 'react';
import './Terminal.css';

function Terminal() {
  const [command, setCommand] = useState('');
  const [res, setRes] = useState('');

  const handleCommandChange = (event) => {
    setCommand(event.target.value);
  };

  const handleCommandSubmit = (event) => {
    event.preventDefault();
   
        if (command === 'help') {
            setRes('pehly salad bhej');
        }
    
  };

  return (
    <div className="terminal">
      <div className="terminal-header">
        <span className="terminal-header-text">$ bash</span>
        <div className="terminal-header-icons">
          <div className="terminal-header-icon close"></div>
          <div className="terminal-header-icon maximize"></div>
          <div className="terminal-header-icon minimize"></div>
        </div>
      </div>
      <div className="terminal-body">
        {/* Display user input and output here */}
        <form onSubmit={handleCommandSubmit}>
          <div className='insideForm'>
          <span className="terminal-prompt">$</span>
          <input
            type="text"
            className="terminal-input"
            value={command}
            onChange={handleCommandChange}
            autoFocus
          />
          </div>
            <span className="terminal-promptAns">
                {res? res : ''}
            </span>
        </form>
      </div>
    </div>
  );
}

export default Terminal;
