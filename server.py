import asyncio
import websockets
import json
from game_logic import Game, Pawn, Hero1, Hero2

class WebSocketServer:
    def __init__(self):
        self.game = Game()
        self.players = {}  # Dictionary to store player WebSocket connections
        self.setup_game()  # Initialize the game with characters

    def setup_game(self):
        # Initialize characters for Player A
        self.game.place_character(0, 0, Pawn('A-P1', 'A'))
        self.game.place_character(0, 1, Hero1('A-H1', 'A'))
        self.game.place_character(0, 2, Hero2('A-H2', 'A'))

        # Initialize characters for Player B
        self.game.place_character(4, 0, Pawn('B-P1', 'B'))
        self.game.place_character(4, 1, Hero1('B-H1', 'B'))
        self.game.place_character(4, 2, Hero2('B-H2', 'B'))

    async def handle_connection(self, websocket, path):
        player = path.strip('/')
        if player not in ['A', 'B']:
            await websocket.send(json.dumps({'type': 'error', 'message': 'Invalid player identifier'}))
            return
        
        # Register player
        self.players[player] = websocket
        await self.send_game_state()

        try:
            async for message in websocket:
                data = json.loads(message)
                if data['type'] == 'move':
                    await self.process_move(player, data['character'], data['direction'])
                elif data['type'] == 'initialize':
                    await self.send_game_state()
        finally:
            # Unregister player on disconnection
            del self.players[player]

    async def process_message(self, data):
        if data['type'] == 'move':
            move = data['move']
            if not self.validate_move(move):
                await self.send_error("Invalid player identifier or move format.")
                return
            
            move_result = self.game.process_move(move)
            if move_result['status'] == 'valid':
                await self.send_game_state()
            else:
                await self.send_error(move_result['message'])

    def validate_move(self, move):
        # Example validation logic
        valid_moves = ['P1:L', 'P1:F', 'H2:FL', 'H2:BR']  # Define valid moves based on game rules
        return move in valid_moves

    async def send_game_state(self):
        board = self.game.grid.board
        game_state = {
            'type': 'update',
            'board': board
        }
        await self.broadcast(json.dumps(game_state))

    def broadcast(self):
        board_state = self.game.grid.board
        for client in self.clients:
            try:
                client.send(json.dumps({'type': 'update', 'board': board_state}))
            except:
                self.clients.remove(client)

async def main():
    server = WebSocketServer()
    async with websockets.serve(server.handle_connection, 'localhost', 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
