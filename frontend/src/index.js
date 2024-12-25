import './index.css';
import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';

function App() {

  const pieceToSVG = {
    '0': '/svgs/black-rook.svg',
    '1': '/svgs/black-knight.svg',
    '2': '/svgs/black-bishop.svg',
    '3': '/svgs/black-queen.svg',
    '4': '/svgs/black-king.svg',
    '5': '/svgs/black-pawn.svg',
    '7': '/svgs/white-pawn.svg',
    '8': '/svgs/white-rook.svg',
    '9': '/svgs/white-knight.svg',
    '10': '/svgs/white-bishop.svg',
    '11': '/svgs/white-queen.svg',
    '12': '/svgs/white-king.svg',
  };

  const [board, setBoard] = useState(null);
  const [selectedSquare, setSelectedSquare] = useState([]);
  const [suggestedSquares, setSuggestedSquares] = useState([]);
  const [status, setStatus] = useState([]);

  const squareClicked = async (rowIndex, columnIndex) => {
    const response = await axios.post('http://localhost:5000/api/squareClicked', { rowIndex, columnIndex });
    setBoard(response.data['board']);
    setSelectedSquare(response.data['selectedSquare']);
    setSuggestedSquares(response.data['suggestedSquares']);
    setStatus(response.data['status']);
  };
  
  useEffect(() => {
    squareClicked(3, 4);
  }, []);

  if (!board || board.length === 0) {
    return <div>Loading...</div>;
  }

  else if (status != 'live') {
    return <div>{status}</div>;
  }

  const squares = [];

  for (let i = 0; i < 64; i++) {
    const isLight = (Math.floor(i / 8) + i % 8) % 2 == 0;
    const isSelected = selectedSquare && selectedSquare[0] == Math.floor(i / 8) && selectedSquare[1] == i % 8;
    const isSuggested = suggestedSquares && suggestedSquares.some(value => value[0] == Math.floor(i / 8) && value[1] == i % 8);

    squares.push(
      <div 
        key={`${i}`}
        className={`square${isLight ? ' light' : ' dark'}${isSuggested ? ' suggestion' : ''}${isSelected ? ' selected' : ''}`}
        onClick={() => squareClicked(Math.floor(i / 8), i % 8)}
      >
        {board[i] != 6 && (
          <img className='piece' src={pieceToSVG[board[i]]}/>
        )}
      </div>
    );
  }

  return <div className='board'>{squares}</div>;
  
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
