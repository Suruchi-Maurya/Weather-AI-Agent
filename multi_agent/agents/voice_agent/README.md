# Voice Agent
The Voice Agent serves as the primary interface for voice interactions, integrating both Speech-to-Text (STT) and Text-to-Speech (TTS) capabilities.

**Future Responsibilities:**
- Managing the end-to-end voice session lifecycle.
- Direct integration with STT and TTS API endpoints.
- Handling audio stream inputs and outputs.
- Coordinating with the Multi-Agent Orchestrator for text processing.

**Implementation Detail:**
STT and TTS are implemented as internal methods within the Voice Agent to reduce architectural complexity.

TODO: Replace dummy endpoints with production-grade STT/TTS services.