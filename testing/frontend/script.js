// Select DOM Elements
const chessboard = document.getElementById('chessboard');
const statusDiv = document.getElementById('status');

// Game State Variables
let selectedSquare = null;
let suggestedSquares = [];
let currentBoard = [];

// Utility Functions

/**
 * Converts a feature vector index to row and column.
 * @param {number} index - Index from 0 to 63.
 * @returns {Object} - { row, col }
 */
function indexToPosition(index) {
    const row = Math.floor(index / 8);
    const col = index % 8;
    return { row, col };
}

/**
 * Converts row and column to feature vector index.
 * @param {number} row 
 * @param {number} col 
 * @returns {number}
 */
function positionToIndex(row, col) {
    return row * 8 + col;
}

/**
 * Converts encoded piece to SVG filename.
 * @param {number} piece 
 * @returns {string}
 */
function encodedPieceToName(piece) {
    const pieceMap = {
        0: 'black-rook',
        1: 'black-knight',
        2: 'black-bishop',
        3: 'black-queen',
        4: 'black-king',
        5: 'black-pawn',
        7: 'white-pawn',
        8: 'white-rook',
        9: 'white-knight',
        10: 'white-bishop',
        11: 'white-queen',
        12: 'white-king'
    };
    return pieceMap[piece] || 'empty';
}

/**
 * Converts encoded piece to human-readable name.
 * @param {number} piece 
 * @returns {string}
 */
function pieceName(piece) {
    const nameMap = {
        0: 'Black Rook',
        1: 'Black Knight',
        2: 'Black Bishop',
        3: 'Black Queen',
        4: 'Black King',
        5: 'Black Pawn',
        6: 'Empty',
        7: 'White Pawn',
        8: 'White Rook',
        9: 'White Knight',
        10: 'White Bishop',
        11: 'White Queen',
        12: 'White King'
    };
    return nameMap[piece] || 'Unknown';
}

/**
 * Initializes and renders the chessboard based on the current board state.
 * @param {Array} board - Array of 64 elements representing the board.
 */
function initializeBoard(board) {
    chessboard.innerHTML = ''; // Clear existing board
    for (let i = 0; i < 64; i++) {
        const square = document.createElement('div');
        square.classList.add('square');

        const { row, col } = indexToPosition(i);

        // Determine square color
        if ((row + col) % 2 === 0) {
            square.classList.add('light');
        } else {
            square.classList.add('dark');
        }

        // Set data attributes
        square.dataset.row = row;
        square.dataset.col = col;

        // Add piece if present
        const piece = board[i];
        if (piece !== 6) { // EMPTY_SQUARE
            const img = document.createElement('img');
            img.classList.add('piece');
            img.src = `svgs/${encodedPieceToName(piece)}.svg`;
            img.alt = pieceName(piece);
            square.appendChild(img);
        }

        // Add click event listener
        square.addEventListener('click', onSquareClick);

        chessboard.appendChild(square);
    }
}

/**
 * Handles click events on chessboard squares.
 * @param {Event} event 
 */
function onSquareClick(event) {
    const square = event.currentTarget;
    const row = parseInt(square.dataset.row);
    const col = parseInt(square.dataset.col);
    const clickedSquare = { row, col };

    if (selectedSquare) {
        // Check if clicked square is a suggested move
        if (suggestedSquares.some(pos => pos.row === row && pos.col === col)) {
            // Execute the move by sending the 'to' square
            executeMove(clickedSquare);
        } else {
            // Select a new square if it has a piece of the current player
            // Or, deselect if clicking the same square
            if (selectedSquare.row === row && selectedSquare.col === col) {
                clearSelection();
            } else {
                const piece = getPieceAt(row, col);
                if (piece !== 6 && isCurrentPlayersPiece(piece)) {
                    selectedSquare = clickedSquare;
                    fetchSuggestedMoves();
                } else {
                    clearSelection();
                }
            }
        }
    } else {
        // Select the square if it has a piece of the current player
        const piece = getPieceAt(row, col);
        if (piece !== 6 && isCurrentPlayersPiece(piece)) {
            selectedSquare = clickedSquare;
            fetchSuggestedMoves();
        }
    }
}

/**
 * Determines if the selected piece belongs to the current player.
 * @param {number} piece 
 * @returns {boolean}
 */
function isCurrentPlayersPiece(piece) {
    // Assuming the player is WHITE and the engine is BLACK
    // 7-12 are white pieces
    return piece >= 7 && piece <= 12;
}

/**
 * Clears the current selection and suggested moves.
 */
function clearSelection() {
    selectedSquare = null;
    suggestedSquares = [];
    updateBoard();
}

/**
 * Retrieves the piece at a given position.
 * @param {number} row 
 * @param {number} col 
 * @returns {number}
 */
function getPieceAt(row, col) {
    return currentBoard[positionToIndex(row, col)];
}

/**
 * Sends a move to the backend by clicking a suggested square.
 * @param {Object} to - { row, col }
 */
function executeMove(to) {
    if (!selectedSquare) return;
    fetch('http://localhost:5000/api/squareClicked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            rowIndex: to.row,
            columnIndex: to.col
        })
    })
    .then(response => response.json())
    .then(data => {
        // Move has been executed and engine move
        currentBoard = data.board;
        initializeBoard(currentBoard);
        selectedSquare = null;
        suggestedSquares = [];
        statusDiv.textContent = `Status: ${data.status}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

/**
 * Fetches suggested moves for the currently selected square.
 */
function fetchSuggestedMoves() {
    fetch('http://localhost:5000/api/squareClicked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            rowIndex: selectedSquare.row,
            columnIndex: selectedSquare.col
        })
    })
    .then(response => response.json())
    .then(data => {
        currentBoard = data.board;
        suggestedSquares = data.suggestedSquares.map(pos => ({ row: pos[0], col: pos[1] }));
        updateBoardWithData(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

/**
 * Updates the board UI based on data received from the backend.
 * @param {Object} data 
 */
function updateBoardWithData(data) {
    currentBoard = data.board;
    initializeBoard(currentBoard);
    highlightSelectionAndSuggestions(data.selectedSquare, data.suggestedSquares);
    statusDiv.textContent = `Status: ${data.status}`;
}

/**
 * Highlights the selected square and suggested move squares.
 * @param {Array} selected - [row, col]
 * @param {Array} suggested - Array of [row, col]
 */
function highlightSelectionAndSuggestions(selected, suggested) {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        square.classList.remove('selected');
        square.classList.remove('suggested');
    });

    if (selected && selected.length === 2 && selected[0] >=0 && selected[1] >=0) {
        const selectedIndex = positionToIndex(selected[0], selected[1]);
        const selectedSquareDiv = chessboard.children[selectedIndex];
        selectedSquareDiv.classList.add('selected');
    }

    if (suggested) {
        suggested.forEach(pos => {
            if (pos.length === 2 && pos[0] >=0 && pos[1] >=0) {
                const index = positionToIndex(pos[0], pos[1]);
                const squareDiv = chessboard.children[index];
                squareDiv.classList.add('suggested');
            }
        });
    }
}

/**
 * Re-renders the board without highlights.
 */
function updateBoard() {
    initializeBoard(currentBoard);
    highlightSelectionAndSuggestions(selectedSquare, suggestedSquares);
    // Status may not have changed
}

/**
 * Fetches the initial game state from the backend.
 */
function fetchInitialBoard() {
    // Send a dummy POST to get the initial state
    fetch('http://localhost:5000/api/squareClicked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            rowIndex: -1, // Dummy value to get the initial state
            columnIndex: -1
        })
    })
    .then(response => response.json())
    .then(data => {
        currentBoard = data.board;
        initializeBoard(currentBoard);
        statusDiv.textContent = `Status: ${data.status}`;
        // No selection initially
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Initialize the board on page load
fetchInitialBoard();
