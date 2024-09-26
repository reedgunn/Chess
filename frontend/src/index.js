import './index.css';
import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';

function App() {

  const pieceToSVG = {
    '1': '/svgs/white-pawn.svg',
    '2': '/svgs/white-rook.svg',
    '3': '/svgs/white-knight.svg',
    '4': '/svgs/white-bishop.svg',
    '5': '/svgs/white-queen.svg',
    '6': '/svgs/white-king.svg',
    '-1': '/svgs/black-pawn.svg',
    '-2': '/svgs/black-rook.svg',
    '-3': '/svgs/black-knight.svg',
    '-4': '/svgs/black-bishop.svg',
    '-5': '/svgs/black-queen.svg',
    '-6': '/svgs/black-king.svg',
  };

  const [boardMatrix, setBoardMatrix] = useState([]);
  const [selectedSquare, setSelectedSquare] = useState([]);
  const [squareSuggestions, setSquareSuggestions] = useState([]);
  const [status, setStatus] = useState([]);

  const fetchBoardMatrix = async () => {
    const response = await axios.get('http://localhost:5000/api/get-board-state');
    console.log("Received board state:", response.data);
    setBoardMatrix(response.data['board-matrix']);
    setSelectedSquare(response.data['selected-square']);
    setSquareSuggestions(response.data['square-suggestions']);
    setStatus(response.data['status']);
  };
  
  const squareClicked = async (row_index, col_index) => {
    const response = await axios.post('http://localhost:5000/api/square-clicked', { row_index, col_index });
    setBoardMatrix(response.data['board-matrix']);
    setSelectedSquare(response.data['selected-square']);
    setSquareSuggestions(response.data['square-suggestions']);
    setStatus(response.data['status']);
  };
  
  useEffect(() => {
    fetchBoardMatrix();
  }, []);

  if (boardMatrix.length == 0) {
    return <div>Loading...</div>;
  }

  else if (status[0] != 'live') {
    return <div>{status[0]}</div>;
  }


  const squares = [];

  for (let row_index = 0; row_index < 8; row_index++) {
    for (let col_index = 0; col_index < 8; col_index++) {
      const isLight = (row_index + col_index) % 2 === 0;
      const isSelected = selectedSquare && selectedSquare[0] === row_index && selectedSquare[1] === col_index;
      const isSuggested = squareSuggestions && squareSuggestions.some(value => value[0] === row_index && value[1] === col_index);
  
      squares.push(
        <div 
          key={`${row_index}${col_index}`}
          className={`square ${isLight ? 'light' : 'dark'}${isSuggested ? ' suggestion' : ''}${isSelected ? ' selected' : ''}`}
          onClick={() => squareClicked(row_index, col_index)}
        >
          {boardMatrix[row_index][col_index] !== 0 && (
            <img className='piece' src={pieceToSVG[boardMatrix[row_index][col_index]]}/>
          )}
        </div>
      );
    }
  }  

  return <div className='board'>{squares}</div>;
  
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
