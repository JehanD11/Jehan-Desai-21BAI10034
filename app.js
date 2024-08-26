const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
    console.log('Connected to WebSocket server');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleServerMessage(data);
};

document.getElementById('move-button').addEventListener('click', () => {
    const moveInput = document.getElementById('move-input').value.trim().toUpperCase();
    if (moveInput.match(/^[A-Z][1-5]:[A-Z][LRFB]{1,2}$/)) {
        ws.send(JSON.stringify({ type: 'move', move: moveInput }));
    } else {
        console.error('Invalid move format');
    }
});

ws.onerror = (error) => {
    console.error('WebSocket Error: ', error);
};

function handleServerMessage(data) {
    if (data.type === 'update') {
        renderBoard(data.board);
    } else if (data.type === 'error') {
        console.error('Error from server: ', data.message);
    }
}

function renderBoard(board) {
    console.log('Rendering board:', board); // Debugging: Check the board data
    const boardElement = document.getElementById('game-board');
    boardElement.innerHTML = ''; // Clear existing content
    board.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const cellElement = document.createElement('div');
            cellElement.classList.add('board-cell');
            cellElement.textContent = cell ? cell : ''; // Display character name or empty
            boardElement.appendChild(cellElement);
        });
    });
}

document.getElementById('move-button').addEventListener('click', () => {
    const moveInput = document.getElementById('move-input').value;
    ws.send(JSON.stringify({ type: 'move', move: moveInput }));
});
