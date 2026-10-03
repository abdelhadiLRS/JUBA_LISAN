"""Only delivered user/assistant turns with audio make a billable voice session."""
class VoiceDelivery:
    def __init__(self, websocket):
        self.websocket = websocket
        self.current_turn = None
        self.user_turns = set()
        self.assistant_turns = set()
        self.audio_turns = set()
        self.successful_turns = set()

    def __getattr__(self, name):
        return getattr(self.websocket, name)

    async def send_json(self, data, *args, **kwargs):
        await self.websocket.send_json(data, *args, **kwargs)
        turn = data.get("turn_id")
        if turn is not None:
            self.current_turn = turn
        if data.get("type") == "transcript" and data.get("final") and str(data.get("text", "")).strip():
            if data.get("role") == "user":
                self.user_turns.add(turn)
            elif data.get("role") == "assistant":
                self.assistant_turns.add(turn)
        if data.get("type") == "turn_complete" and turn in self.user_turns and turn in self.assistant_turns and turn in self.audio_turns:
            self.successful_turns.add(turn)

    async def send_bytes(self, data):
        await self.websocket.send_bytes(data)
        if data and self.current_turn is not None:
            self.audio_turns.add(self.current_turn)
