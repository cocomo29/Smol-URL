import { useState } from 'react';
import './Terminal.css';

function Terminal() {
  const [command, setCommand] = useState('');
  const [prevCommands, setPrevCommands] = useState([]);

  const handleCommandChange = (event) => {
    setCommand(event.target.value);
  };

  const handleCommandSubmit = (event) => {
    event.preventDefault();
    if (command === 'help') {
      setPrevCommands([...prevCommands, { command, output: 'Usage: shortner -L [url]' }]);
    } else if (command === 'whoami') {
      setPrevCommands([...prevCommands, { command, output: 'I am a URL Shortener, made by @notwld and @cocomo with <3' }]);
    } else if (command === '' || command === 'clear') {
      setPrevCommands([]);
    } else if (command.startsWith('shortner -L')) {
      const getUrl = async () => {
        await fetch('http://127.0.0.1:8000/shorten', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: command.split(' ')[-1] }),
        })
          .then((res) => res.json())
          .then((data) => {
            const output = (
              <span>
                Your short url is{" "}
                <a href={`http://127.0.0.1:8000${data.short_url}`} target='_blank' style={{ color: "green" }} rel="noreferrer">
                  {data.short_url}
                </a>
              </span>
            );
            setPrevCommands([...prevCommands, { command, output }]);
          })
          .catch((err) =>
            setPrevCommands([...prevCommands, { command, output: err }])
          );
      };
      
      getUrl();
    } else {
      setPrevCommands([...prevCommands, { command, output: 'Invalid Command' }]);
    }
    setCommand('');
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
        {/* Display previous commands and outputs */}
        {prevCommands.map(({ command, output }, index) => (
          <div key={index}>
            <span className="terminal-prompt">$ {command}</span> <br />
            <span className="terminal-promptAns">{output}</span>
          </div>
        ))}
        {/* Display current input prompt */}
        <form onSubmit={handleCommandSubmit}>
          <div className="insideForm">
            <span className="terminal-prompt">$</span>
            <input
              type="text"
              className="terminal-input"
              value={command}
              onChange={handleCommandChange}
              autoFocus
            />
          </div>
        </form>
      </div>
    </div>
  );
}

export default Terminal;
